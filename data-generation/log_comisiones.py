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


def generate_comisiones(config):
    seed = config["seed"]
    volume = config["tables"]["TB_COMISIONES_LOG"]["volume"]

    rng = np.random.default_rng(seed)

    clientes = pd.read_csv(CLIENTES_FILE)
    productos = pd.read_csv(PRODUCTOS_FILE)

    ids_clientes = clientes["id_cli"].values
    codigos_productos = productos["cod_prod"].astype(str).values

    fechas = pd.date_range(
        start=config["global"]["start_date"],
        end=config["global"]["end_date"],
        freq="D")

    tipos_comision = ["MANTENIMIENTO","TRANSFERENCIA","RETIRO","MANEJO_CUENTA","TARJETA","ESTUDIO_CREDITO" ]
    probabilidades_tipo = [0.25,0.25,0.15,0.15,0.15,0.05]

    estados = ["COBRADA","PENDIENTE","REVERSADA"]
    probabilidades_estado = [ 0.90, 0.07, 0.03 ]

    id_cli = rng.choice(
        ids_clientes, size=volume)

    cod_prod = rng.choice(
        codigos_productos, size=volume)

    fec_cobro = rng.choice(
        fechas, size=volume)

    tip_comision = rng.choice(
        tipos_comision,
        size=volume,
        p=probabilidades_tipo)

    estado_cobro = rng.choice(
        estados,
        size=volume,
        p=probabilidades_estado)

    vr_comision = rng.lognormal(
        mean=np.log(25000),
        sigma=0.7,
        size=volume)

    vr_comision = np.round(
        np.clip(
            vr_comision,
            1000,
            500000),
        2)

    df_comisiones = pd.DataFrame({
        "id_comision": np.arange(1, volume + 1),
        "id_cli": id_cli,
        "cod_prod": cod_prod,
        "fec_cobro": fec_cobro,
        "vr_comision": vr_comision,
        "tip_comision": tip_comision,
        "estado_cobro": estado_cobro
    })

    return df_comisiones


def save_files(df_comisiones):

    csv_file = CSV_DIR / "TB_COMISIONES_LOG.csv"
    parquet_file = PARQUET_DIR / "TB_COMISIONES_LOG.parquet"

    df_comisiones.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig")

    df_comisiones.to_parquet(
        parquet_file,
        index=False)


def main():
    config = load_config()

    df_comisiones = generate_comisiones(config)

    save_files(df_comisiones)

    print("\nCantidad de registros:", len(df_comisiones))


if __name__ == "__main__":
    main()