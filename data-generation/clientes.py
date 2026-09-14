from pathlib import Path
from datetime import datetime, timedelta

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

# Se crean las carpetas si no existen
CSV_DIR.mkdir(parents=True, exist_ok=True)
PARQUET_DIR.mkdir(parents=True, exist_ok=True)
TXT_DIR.mkdir(parents=True, exist_ok=True)



# 2. CARGAR CONFIGURACION DE .YALM

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

SEED = config["seed"]
TABLE_CONFIG = config["tables"]["TB_CLIENTES_CORE"]
NUM_CLIENTES = TABLE_CONFIG["volume"]

START_DATE = pd.to_datetime(
    config["global"]["start_date"])

END_DATE = pd.to_datetime(
    config["global"]["end_date"])


# 3. SE UTILIZA LA SEMILLA PARA GARANTIZAR QUE LOS DATOS SEAN LOS MISMOS Y SE DEFINE QUE LOS DATOS DEBEN SER DE COLOMBIA

np.random.seed(SEED)
fake = Faker("es_CO")
fake.seed_instance(SEED)


# 4. DEFINICION DE LISTAS DE VALORES Y SU PORCENTAJE DE PARTICIPACION

SEGMENTOS = ["MASIVO","PREFERENCIAL","PRIVADA","EMPRESARIAL","INSTITUCIONAL"]
SEGMENTOS_PESO = [0.45,0.23,0.12,0.13,0.07]

ESTADOS = ["ACTIVO","INACTIVO","BLOQUEADO"]
ESTADOS_PESO = [0.85,0.10,0.05]

CANALES_ADQUISICION = ["APP BANCARIA","SUCURSAL VIRTUAL","SUCURSAL FISICA","CALL_CENTER","ASESOR"]
CANALES_PESO = [ 0.30,0.25,0.20,0.15,0.10]

TIPOS_DOCUMENTO = ["CC","CE","PAS"]
TIPOS_DOCUMENTO_PESO = [0.90,0.08,0.02]

UBICACIONES = {
    "Bogota D.C.": "Bogota D.C.",
    "Medellin": "Antioquia",
    "Cali": "Valle del Cauca",
    "Barranquilla": "Atlantico",
    "Cartagena": "Bolívar",
    "Bucaramanga": "Santander",
    "Pereira": "Risaralda",
    "Manizales": "Caldas",
    "Armenia": "Quindio",
    "Ibague": "Tolima",
    "Santa Marta": "Magdalena",
    "Villavicencio": "Meta",
    "Pasto": "Narino",
    "Cucuta": "Norte de Santander"
}


# 5. FUNCIONES AUXILIARES PARA GENERAR DATOS ALEATORIOS / SINTETICOS

def random_date(start_date, end_date, size):

    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()

    random_timestamps = np.random.uniform(
        start_timestamp,
        end_timestamp,
        size)

    return pd.to_datetime(
        random_timestamps,
        unit="s"
    ).normalize()


def generate_birth_dates(size):

    ages = np.random.normal(
        loc=37,
        scale=14,
        size=size)

    ages = np.clip(
        np.round(ages),
        18,
        90
    ).astype(int)

    today = pd.Timestamp.today().normalize()

    birth_dates = []

    for age in ages:

        days = int(age * 365.25)
        birth_date = (today - pd.Timedelta(days=days))
        birth_dates.append(birth_date)

    return pd.to_datetime(birth_dates)


def generate_credit_scores(size):

    scores = np.random.normal(
        loc=680,
        scale=100,
        size=size)

    scores = np.clip(
        np.round(scores),
        300,
        950)

    return scores.astype(int)


def generate_document_number(size):

    documents = np.random.randint(
        1050000000,
        1060999999,
        size=size)

    return documents.astype(str)


def apply_nulls(series, rate):

    result = series.copy()
    number_of_nulls = int(
        len(result) * rate)

    if number_of_nulls == 0:
        return result

    indexes = np.random.choice(
        result.index,
        size=number_of_nulls,
        replace=False)

    result.loc[indexes] = None

    return result


# 6. GENERACION DE DATOS SINTETICOS CON LOS PARAMETROS ANTERI


def generate_clientes():

##    print(f"Semilla: {SEED}")
##    print(f"Volumen: {NUM_CLIENTES:,}")

    id_cli = np.arange(
        1,
        NUM_CLIENTES + 1)


    nombres = [fake.first_name()
        for _ in range(NUM_CLIENTES)]

    apellidos = [fake.last_name()
        for _ in range(NUM_CLIENTES)]

    tipos_documento = np.random.choice(
        TIPOS_DOCUMENTO,
        size=NUM_CLIENTES,
        p=TIPOS_DOCUMENTO_PESO)

    documentos = generate_document_number(NUM_CLIENTES)

    fechas_nacimiento = generate_birth_dates(NUM_CLIENTES)

    fechas_alta = random_date(
        START_DATE,
        END_DATE,
        NUM_CLIENTES)

    segmentos = np.random.choice(
        SEGMENTOS,
        size=NUM_CLIENTES,
        p=SEGMENTOS_PESO)

    scores = generate_credit_scores(
        NUM_CLIENTES)

    ciudades = np.random.choice(
        list(UBICACIONES.keys()),
        size=NUM_CLIENTES)

    departamentos = [UBICACIONES[ciudad]
        for ciudad in ciudades]

    estados = np.random.choice(
        ESTADOS,
        size=NUM_CLIENTES,
        p=ESTADOS_PESO)

    canales = np.random.choice(
        CANALES_ADQUISICION,
        size=NUM_CLIENTES,
        p=CANALES_PESO)

# SE GENERA EL DATAFRAME


    df_clientes = pd.DataFrame({
        "id_cli": id_cli,
        "nomb_cli": nombres,
        "apell_cli": apellidos,
        "tip_doc": tipos_documento,
        "num_doc": documentos,
        "fec_nac": fechas_nacimiento,
        "fec_alta": fechas_alta,
        "cod_segmento": segmentos,
        "score_buro": scores,
        "ciudad_res": ciudades,
        "depto_res": departamentos,
        "estado_cli": estados,
        "canal_adquis": canales
    })

    print(df_clientes)


# 7. DATA CON ERRORES PARA VALIDACION DE CALIDAD DE LOS ADTOS


    null_rates = TABLE_CONFIG["null_rates"]

    for column, rate in null_rates.items():

        df_clientes[column] = apply_nulls(
            df_clientes[column], rate)

# Anomalias

    anomalies = TABLE_CONFIG["anomalies"]

# Anomalía 1= documentos duplicados ingresadas intencionalmente para validar calidad de los datos

    duplicate_count = anomalies[
        "duplicate_documents"]

    duplicate_indexes = np.random.choice(
        df_clientes.index,
        size=duplicate_count,
        replace=False)

    source_indexes = np.random.choice(
        df_clientes.index,
        size=duplicate_count,
        replace=False)

    for target, source in zip(
        duplicate_indexes,
        source_indexes):
        df_clientes.loc[target, "num_doc"] = (
            df_clientes.loc[source, "num_doc"])

# Anomalía 2= fechas de nacimiento futuras ingresadas intencionalmente para validar calidad de los datos

    future_count = anomalies[
        "future_birth_dates"]

    future_indexes = np.random.choice(
        df_clientes.index,
        size=future_count,
        replace=False)

    for index in future_indexes:

        df_clientes.loc[index, "fec_nac"] = (
            pd.Timestamp.today()
            + pd.Timedelta(days=365))


# 9. GENERAR Y GUARDAR ARCHIVOS CON LA DATA YA GENERADA


    csv_file = (CSV_DIR /
        "TB_CLIENTES_CORE.csv")

    parquet_file = (PARQUET_DIR /
        "TB_CLIENTES_CORE.parquet")

    txt_file = (TXT_DIR /
        "TB_CLIENTES_CORE.txt")

    # ARCHIVO CSV
    df_clientes.to_csv(
        csv_file,
        index=False,
        encoding="utf-8")

    # ARCHIVO Parquet
    df_clientes.to_parquet(
        parquet_file,
        index=False)

    # ARCHIVO TXT
    df_clientes.to_csv(
        txt_file,
        index=False,
        sep="|",
        encoding="utf-8")



   # print(f"Registros: {len(df_clientes):,}")
    # print("\nArchivos generados:")

    # print(csv_file)
    # print(parquet_file)
    # print(txt_file)

    # print("\nNulos:")
    # print(df_clientes.isnull().sum())

    return df_clientes


if __name__ == "__main__":

    generate_clientes()