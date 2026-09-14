from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from faker import Faker


# 1. RUTAS EN DONDE SE VAN A TOMAR LOS PARAMETROS Y ALMACENAR LOS ARCHIVOS CON DATA SINTETICOS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "PythonProject" / "data_generation" / "param_config.yaml"

CSV_DIR = PROJECT_ROOT / "PythonProject" / "data" / "csv"
PARQUET_DIR = PROJECT_ROOT / "PythonProject" / "data" / "parquet"
TXT_DIR = PROJECT_ROOT / "PythonProject" / "data" / "txt"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)



def generate_products(config):
    seed = config["seed"]
    volume = config["tables"]["TB_PRODUCTOS_CAT"]["volume"]

    rng = np.random.default_rng(seed)

    productos = []

    tipos_productos = ["CUENTA","TARJETA","CREDITO_CONSUMO","CREDITO_LIBRANZA","CREDITO_VEHICULO","CREDITO_VIVIENDA"]

    for i in range(1, volume + 1):
        tipo = rng.choice(tipos_productos)

        if tipo == "CUENTA":
            descripcion = f"Cuenta de Ahorros {i:03d}"
            tasa = round(rng.uniform(0.5, 6.0), 4)
            plazo = 0
            cuota = round(rng.uniform(0, 50000), 2)
            comision = round(rng.uniform(0, 25000), 2)
        elif tipo == "TARJETA":
            descripcion = f"Tarjeta de Credito {i:03d}"
            tasa = round(rng.uniform(18.0, 35.0), 4)
            plazo = int(rng.choice([12, 24, 36, 48]))
            cuota = round(rng.uniform(20000, 80000), 2)
            comision = round(rng.uniform(0, 150000), 2)
        elif tipo == "CREDITO_CONSUMO":
            descripcion = f"Credito de Consumo {i:03d}"
            tasa = round(rng.uniform(12.0, 28.0), 4)
            plazo = int(rng.choice([12, 24, 36, 48, 60]))
            cuota = round(rng.uniform(100000, 800000), 2)
            comision = round(rng.uniform(0, 100000), 2)
        elif tipo == "CREDITO_LIBRANZA":
            descripcion = f"Credito de Libranza {i:03d}"
            tasa = round(rng.uniform(10.0, 22.0), 4)
            plazo = int(rng.choice([12, 24, 36, 48, 60, 72]))
            cuota = round(rng.uniform(100000, 700000), 2)
            comision = round(rng.uniform(0, 80000), 2)
        elif tipo == "CREDITO_VEHICULO":
            descripcion = f"Credito de Vehiculo {i:03d}"
            tasa = round(rng.uniform(9.0, 20.0), 4)
            plazo = int(rng.choice([24, 36, 48, 60, 72, 84]))
            cuota = round(rng.uniform(300000, 1500000), 2)
            comision = round(rng.uniform(0, 200000), 2)
        else:
            descripcion = f"Credito de Vivienda {i:03d}"
            tasa = round(rng.uniform(7.0, 15.0), 4)
            plazo = int(rng.choice([60, 120, 180, 240, 300]))
            cuota = round(rng.uniform(500000, 3000000), 2)
            comision = round(rng.uniform(0, 500000), 2)

        estado = rng.choice(
            ["ACTIVO", "INACTIVO"],
            p=[0.90, 0.10]
        )

        productos.append({
            "cod_prod": f"{i:03d}",
            "desc_prod": descripcion,
            "tip_prod": tipo,
            "tasa_ea": tasa,
            "plazo_max_meses": plazo,
            "cuota_min": cuota,
            "comision_admin": comision,
            "estado_prod": estado
        })

    return pd.DataFrame(productos)


def add_anomalies(df, config):
    anomalies = config["tables"]["TB_PRODUCTOS_CAT"]["anomalies"]

    # Se inserta registros intencionales de Tasa de interes invalida
    cantidad_tasas = anomalies["invalid_interest_rates"]
    if cantidad_tasas > 0:
        indices = df.index[:cantidad_tasas]
        df.loc[indices, "tasa_ea"] = -2.50

    return df


def save_files(df):
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)

    csv_file = CSV_DIR / "TB_PRODUCTOS_CAT.csv"
    parquet_file = PARQUET_DIR / "TB_PRODUCTOS_CAT.parquet"

    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    df.to_parquet(parquet_file, index=False)

    print(f"Archivo CSV generado: {csv_file}")
    print(f"Archivo Parquet generado: {parquet_file}")


def main():
    config = load_config()

    df = generate_products(config)
    df = add_anomalies(df, config)

    save_files(df)


if __name__ == "__main__":
    main()