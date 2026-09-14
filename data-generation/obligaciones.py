from pathlib import Path

import numpy as np
import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parent

CONFIG_FILE = PROJECT_ROOT / "data_generation" / "param_config.yaml"

CLIENTES_FILE = PROJECT_ROOT / "data" / "csv" / "TB_CLIENTES_CORE.csv"
PRODUCTOS_FILE = PROJECT_ROOT / "data" / "csv" / "TB_PRODUCTOS_CAT.csv"

CSV_DIR = PROJECT_ROOT / "data" / "csv"
PARQUET_DIR = PROJECT_ROOT / "data" / "parquet"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def generate_obligaciones(config):
    seed = config["seed"]
    volume = config["tables"]["TB_OBLIGACIONES"]["volume"]

    rng = np.random.default_rng(seed)

    clientes = pd.read_csv(CLIENTES_FILE)
    productos = pd.read_csv(PRODUCTOS_FILE)

    ids_clientes = clientes["id_cli"].values

    productos_credito = productos[productos["tip_prod"].isin(["CREDITO_CONSUMO","CREDITO_LIBRANZA","CREDITO_VEHICULO","CREDITO_VIVIENDA"])].copy()

    if productos_credito.empty:
        raise ValueError("No existen productos de crédito en TB_PRODUCTOS_CAT")

    codigos_productos = productos_credito["cod_prod"].astype(str).values
    tipos_productos = productos_credito["tip_prod"].values

    fecha_inicio = pd.Timestamp(config["global"]["start_date"])
    fecha_fin = pd.Timestamp(config["global"]["end_date"])

    id_cli = rng.choice(
        ids_clientes, size=volume)

    posiciones_producto = rng.integers(
        0,
        len(productos_credito),
        size=volume)

    cod_prod = codigos_productos[posiciones_producto]
    tip_prod = tipos_productos[posiciones_producto]

    vr_aprobado = rng.lognormal(
        mean=np.log(20000000),
        sigma=0.8,
        size=volume)

    vr_aprobado = np.round(
        np.clip(vr_aprobado, 500000, 500000000),
        2)

    porcentaje_desembolso = rng.uniform(
        0.85, 1.00,
        size=volume)

    vr_desembolsado = np.round(
        vr_aprobado * porcentaje_desembolso,
        2)

    porcentaje_saldo = rng.uniform(
        0.05, 0.90,
        size=volume)

    sdo_capital = np.round(
        vr_desembolsado * porcentaje_saldo,
        2)

    fec_desembolso = pd.to_datetime(
        rng.choice(
            pd.date_range(
                fecha_inicio,
                fecha_fin,
                freq="D"),
            size=volume))

    plazo_meses = np.zeros(volume, dtype=int)

    for i, tipo in enumerate(tip_prod):

        if tipo == "CREDITO_CONSUMO":
            plazo_meses[i] = rng.choice([12, 24, 36, 48, 60])
        elif tipo == "CREDITO_LIBRANZA":
            plazo_meses[i] = rng.choice([12, 24, 36, 48, 60, 72])
        elif tipo == "CREDITO_VEHICULO":
            plazo_meses[i] = rng.choice([24, 36, 48, 60, 72, 84])
        elif tipo == "CREDITO_VIVIENDA":
            plazo_meses[i] = rng.choice([60, 120, 180, 240, 300])

    fec_venc = (
        pd.Series(fec_desembolso)
        + pd.to_timedelta(plazo_meses * 30, unit="D"))

    num_cuotas_pend = np.where(
        sdo_capital > 0,
        rng.integers(
            1,
            np.maximum(plazo_meses, 2),
            size=volume),
        0)

    vr_cuota = np.round(
        sdo_capital / np.maximum(num_cuotas_pend, 1),
        2)

    # Distribución de días de mora
    rangos_mora = [0,15,45,75,120]

    probabilidades_mora = [0.75,0.12,0.06,0.04,0.03]

    categorias_mora = rng.choice(
        rangos_mora,
        size=volume,
        p=probabilidades_mora)

    dias_mora_act = categorias_mora.copy()

    dias_mora_act[categorias_mora == 15] = rng.integers(
        1,
        31,
        size=(categorias_mora == 15).sum())

    dias_mora_act[categorias_mora == 45] = rng.integers(
        31,
        61,
        size=(categorias_mora == 45).sum())

    dias_mora_act[categorias_mora == 75] = rng.integers(
        61,
        91,
        size=(categorias_mora == 75).sum())

    dias_mora_act[categorias_mora == 120] = rng.integers(
        91,
        181,
        size=(categorias_mora == 120).sum())

    calif_riesgo = []

    for dias in dias_mora_act:

        if dias == 0:
            calif_riesgo.append(rng.choice(["A", "B"], p=[0.90, 0.10]))
        elif dias <= 30:
            calif_riesgo.append(rng.choice(["B", "C"], p=[0.70, 0.30]))
        elif dias <= 60:
            calif_riesgo.append(rng.choice(["C", "D"], p=[0.60, 0.40]))
        elif dias <= 90:
            calif_riesgo.append(rng.choice(["D", "E"], p=[0.40, 0.60]))
        else:
            calif_riesgo.append("E")

    df_obligaciones = pd.DataFrame({
        "id_oblig": np.arange(1, volume + 1),
        "id_cli": id_cli,
        "cod_prod": cod_prod,
        "vr_aprobado": vr_aprobado,
        "vr_desembolsado": vr_desembolsado,
        "sdo_capital": sdo_capital,
        "vr_cuota": vr_cuota,
        "fec_desembolso": fec_desembolso,
        "fec_venc": fec_venc,
        "dias_mora_act": dias_mora_act,
        "num_cuotas_pend": num_cuotas_pend,
        "calif_riesgo": calif_riesgo })

    return df_obligaciones

  #  print(df_obligaciones)

def save_files(df_obligaciones):
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)

    csv_file = CSV_DIR / "TB_OBLIGACIONES.csv"
    parquet_file = PARQUET_DIR / "TB_OBLIGACIONES.parquet"

    df_obligaciones.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig" )

    df_obligaciones.to_parquet(
        parquet_file,
        index=False)



def main():
    config = load_config()

    df_obligaciones = generate_obligaciones(config)

    save_files(df_obligaciones)

 #   print("Cantidad de registros:", len(df_obligaciones))
  #  print(df_obligaciones["calif_riesgo"].value_counts())



if __name__ == "__main__":
    main()