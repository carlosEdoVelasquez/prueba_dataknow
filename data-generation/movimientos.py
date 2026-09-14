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


def generate_movimientos(config):
    seed = config["seed"]
    volume = config["tables"]["TB_MOV_FINANCIEROS"]["volume"]

    rng = np.random.default_rng(seed)

    clientes = pd.read_csv(CLIENTES_FILE)
    productos = pd.read_csv(PRODUCTOS_FILE)

    ids_clientes = clientes["id_cli"].values
    codigos_productos = productos["cod_prod"].astype(str).values

    tipos_movimiento = ["DEBITO","CREDITO","PAGO","RETIRO"]
    prob_tipos = [0.45,0.30,0.20,0.05]

    canales = ["APP BANCARIA","SUCURSAL VIRTUAL","SUCURSAL FISICA", "ATM", "CALL_CENTER", "CORRESPONSAL"]
    prob_canales = [0.35,0.25,0.15,0.15,0.05,0.05]

    estados = ["APROBADO","RECHAZADO","PENDIENTE" ]
    prob_estados = [0.95,0.03,0.02]

    fechas = pd.date_range(
        start=config["global"]["start_date"],
        end=config["global"]["end_date"],
        freq="D")

    id_cli = rng.choice(ids_clientes, size=volume)
    cod_prod = rng.choice(codigos_productos, size=volume)

    fec_mov = rng.choice(fechas, size=volume)

    tip_mov = rng.choice(
        tipos_movimiento,
        size=volume,
        p=prob_tipos)

    cod_canal = rng.choice(
        canales,
        size=volume,
        p=prob_canales)

    cod_estado_mov = rng.choice(
        estados,
        size=volume,
        p=prob_estados)

    vr_mov = rng.lognormal(
        mean=np.log(150000),
        sigma=1.0,
        size=volume)

    vr_mov = np.round(vr_mov, 2)

    vr_mov = np.clip(
        vr_mov,
        5000,
        12540000)

    horas = rng.integers(0, 24, size=volume)
    minutos = rng.integers(0, 60, size=volume)
    segundos = rng.integers(0, 60, size=volume)

    hora_mov = [f"{h:02d}:{m:02d}:{s:02d}"
        for h, m, s in zip(horas, minutos, segundos)]

    numero_cuenta = [f"{cliente:010d}{cuenta:04d}"
        for cliente, cuenta in zip( id_cli, rng.integers(1, 10, size=volume))]

    ciudades = ["BOGOTA","MEDELLIN","CALI","BARRANQUILLA","CARTAGENA","BUCARAMANGA","PEREIRA","MANIZALES"]

    cod_ciudad = rng.choice(
        ciudades,
        size=volume,
        p=[0.30,0.20,0.15,0.10,0.08,0.07,0.05,0.05])

    id_dispositivo = [
        f"DEV{numero:08d}"
        for numero in rng.integers(
            1,
            50001,
            size=volume)]

    df_movimientos = pd.DataFrame({
        "id_mov": np.arange(1, volume + 1),
        "id_cli": id_cli,
        "cod_prod": cod_prod,
        "num_cuenta": numero_cuenta,
        "fec_mov": fec_mov,
        "hra_mov": hora_mov,
        "vr_mov": vr_mov,
        "tip_mov": tip_mov,
        "cod_canal": cod_canal,
        "cod_ciudad": cod_ciudad,
        "cod_estado_mov": cod_estado_mov,
        "id_dispositivo": id_dispositivo
    })

    return df_movimientos


def save_files(df_movimientos):

    csv_file = CSV_DIR / "TB_MOV_FINANCIEROS.csv"
    parquet_file = PARQUET_DIR / "TB_MOV_FINANCIEROS.parquet"

    df_movimientos.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig")

    df_movimientos.to_parquet(
        parquet_file,
        index=False)


def main():
    config = load_config()

    df_movimientos = generate_movimientos(config)

    save_files(df_movimientos)

# print("Cantidad de registros:", len(df))


if __name__ == "__main__":
    main()