from pathlib import Path

import numpy as np
import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parent

CONFIG_FILE = PROJECT_ROOT / "data_generation" / "param_config.yaml"

CSV_DIR = PROJECT_ROOT / "data" / "csv"
PARQUET_DIR = PROJECT_ROOT / "data" / "parquet"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def generate_sucursales(config):
    seed = config["seed"]
    volume = config["tables"]["TB_SUCURSALES_RED"]["volume"]

    rng = np.random.default_rng(seed)

    ubicaciones = [
        {
            "ciudad": "Bogota D.C.",
            "depto": "Bogota D.C.",
            "latitud": 4.7110,
            "longitud": -74.0721
        },
        {
            "ciudad": "Medellin",
            "depto": "Antioquia",
            "latitud": 6.2442,
            "longitud": -75.5812
        },
        {
            "ciudad": "Cali",
            "depto": "Valle del Cauca",
            "latitud": 3.4516,
            "longitud": -76.5320
        },
        {
            "ciudad": "Barranquilla",
            "depto": "Atlantico",
            "latitud": 10.9685,
            "longitud": -74.7813
        },
        {
            "ciudad": "Cartagena",
            "depto": "Bolívar",
            "latitud": 10.3910,
            "longitud": -75.4794
        },
        {
            "ciudad": "Bucaramanga",
            "depto": "Santander",
            "latitud": 7.1193,
            "longitud": -73.1227
        },
        {
            "ciudad": "Pereira",
            "depto": "Risaralda",
            "latitud": 4.8143,
            "longitud": -75.6946
        },
        {
            "ciudad": "Manizales",
            "depto": "Caldas",
            "latitud": 5.0703,
            "longitud": -75.5138
        },
        {
            "ciudad": "Armenia",
            "depto": "Quindio",
            "latitud": 4.5339,
            "longitud": -75.6811
        },
        {
            "ciudad": "Ibague",
            "depto": "Tolima",
            "latitud": 4.4389,
            "longitud": -75.2322
        },
        {
            "ciudad": "Santa Marta",
            "depto": "Magdalena",
            "latitud": 11.2408,
            "longitud": -74.1990
        },
        {
            "ciudad": "Villavicencio",
            "depto": "Meta",
            "latitud": 4.1420,
            "longitud": -73.6266
        },
        {
            "ciudad": "Pasto",
            "depto": "Narino",
            "latitud": 1.2136,
            "longitud": -77.2811
        },
        {
            "ciudad": "Cucuta",
            "depto": "Norte de Santander",
            "latitud": 7.8891,
            "longitud": -72.4967
        }
    ]

    tipos_punto = ["SUCURSAL", "CORRESPONSAL", "CENTRO_SERVICIO"]
    probabilidades_tipo = [0.60, 0.25, 0.15]

    filas = []

    for i in range(1, volume + 1):

        ubicacion = rng.choice(ubicaciones)

        # variación para que las coordenadas no sean exactamente iguales para todas las sucursales.
        latitud = ubicacion["latitud"] + rng.uniform(-0.03, 0.03)
        longitud = ubicacion["longitud"] + rng.uniform(-0.03, 0.03)

        tipo_punto = rng.choice(
            tipos_punto,
            p=probabilidades_tipo)

        activo = rng.choice(
            [1, 0],
            p=[0.90, 0.10])

        filas.append({
            "cod_suc": f"{i:04d}",
            "nom_suc": f"{tipo_punto.title()} {ubicacion['ciudad']} {i:03d}",
            "tip_punto": tipo_punto,
            "ciudad": ubicacion["ciudad"],
            "depto": ubicacion["depto"],
            "latitud": round(latitud, 7),
            "longitud": round(longitud, 7),
            "activo": activo
        })

    return pd.DataFrame(filas)


def save_files(df_sucursales):

    csv_file = CSV_DIR / "TB_SUCURSALES_RED.csv"
    parquet_file = PARQUET_DIR / "TB_SUCURSALES_RED.parquet"

    df_sucursales.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig")

    df_sucursales.to_parquet(
        parquet_file,
        index=False)

def main():
    config = load_config()

    df_sucursales = generate_sucursales(config)

    save_files(df_sucursales)

    print("\nCantidad de registros:", len(df_sucursales))



if __name__ == "__main__":
    main()