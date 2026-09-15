# Autor: Carlos Velásquez
Carpetas creadas:
- data-generation: Scripts de generación de datos dummy y archivo de configuración
- pipelines: Código de transformaciones para las tres capas del pipeline
- orchestacion: Definición del DAG o pipeline del orquestador elegido 
- docs: Diagrama de arquitectura, catálogo de datos y diagrama ER

Nota: Las evidencias de los procesos ejecutados que se mencionan a continuación, se encuentran almacenadas en la ruta: /orchestacion y el nombre del archivo es PRUEBA TECNICA DK.doc

### 1. Descripción del proyecto
Este proyecto corresponde a una prueba técnica de ingeniería de datos orientado a la capacidad de análisis, interpretación de requerimientos y habilidades técnicas para diseñar y desarrollar un proceso que contemple el ciclo completo de los datos a lo largo de la solución propuesta.


Se selecciona este escenario debido a que el sector bancario esta altamente orientado a los datos, así mismo como la disponibilidad, calidad y seguridad de estos, son factores clave para la toma de decisiones en el día a día. Estas soluciones deben ser confiables y escalables, debido a la alta cantidad de generación de los datos y una correcta y oportuna integración puede resolver muchos factores críticos como por ejemplo las conciliaciones bancarias y reportes regulatorios.

Así mismo, se selecciona la plataforma Azure ya que integra servicios que, con una correcta y oportuna implementación puede ser un poco más económico en comparación con otras plataformas. Una de sus grandes ventajas es que sus servicios son independientes y no están en un solo ecosistema, como por ejemplo fabric si lo hace. Otra ventaja es que la suscripción tiene servicios independientes y en caso de que haya cambios de políticas, términos y condiciones en consumo y facturación poco convenientes para la compañía, se van a poder tomar decisiones en cuanto a uso de aplicaciones.  Otro ejemplo claro, es que en caso de que haya una incidencia con algún servicio, los otros servicios no se vean afectados.


### Justificación
Se selecciona este escenario debido a que el sector bancario esta altamente orientado a los datos, así mismo como la disponibilidad, calidad y seguridad de estos, son factores clave para la toma de decisiones en el día a día. Estas soluciones deben ser confiables y escalables, debido a la alta cantidad de generación de los datos y una correcta y oportuna integración puede resolver muchos factores críticos como por ejemplo las conciliaciones bancarias y reportes regulatorios.
Así mismo, se selecciona la plataforma Azure ya que integra servicios que, con una correcta y oportuna implementación puede ser un poco más económico en comparación con otras plataformas. Una de sus grandes ventajas es que sus servicios son independientes y no están en un solo ecosistema, como por ejemplo fabric si lo hace. Otra ventaja es que la suscripción tiene servicios independientes y en caso de que haya cambios de políticas, términos y condiciones en consumo y facturación poco convenientes para la compañía, se van a poder tomar decisiones en cuanto a uso de aplicaciones. Otro ejemplo claro, es que en caso de que haya una incidencia con algún servicio, los otros servicios no se vean afectados.




### 2. Objetivo
Diseñar e implementar una solución de ingeniería de datos que permita:

- Crear datos sintéticos representativos de un entorno financiero.
- Mantener integridad referencial entre las diferentes entidades.
- Parametrizar la generación de datos.
- Generar información en diferentes formatos.
- Cargar los datos inicialmente en SQL Server.
- Preparar la información para su posterior procesamiento en Azure.
- Implementar una arquitectura de datos basada en capas Bronze, Silver y Gold.
- Aplicar técnicas de seguridad
- Facilitar el procesamiento posterior para analítica y consumo de información.


### 3. Arquitectura
La arquitectura propuesta es la siguiente, ya que no se cuenta con mucho tiempo para desarrollar la solución:

python --> datos sinteticos --> SQL Server --> Azure Data Factory --> Arquitectura medallon --> Azure SQL Database --> BI

Adicional a lo anterior, utilizando servicios para garantizar la gobernanza de los datos y seguridad de los datos como Azure Key Vault


### 4. Tecnologías utilizadas

### Desarrollo equipo local

- Python
- Pandas
- NumPy
- Faker
- PyYAML
- PyArrow

### Base de datos equipo local

- Microsoft SQL Server 

### Plataforma Cloud

- Azure Data Lake Storage Gen2
- Azure SQL Database
- Azure Data Factory
- Azure Key Vault
- Azure Databricks

### Control de versiones

- Git
- GitHub



### 5. Generación de datos sinteticos

Los datos utilizados en la solución son sintéticos o dummy y se generan mediante Python. Se debe disponibilizar la información suficientemente representativa para simular un escenario financiero sin utilizar información real o sensible.

La generación utiliza:

- Datos estadisticos.
- Relaciones entre entidades.
- Fechas dentro del período definido.
- Identificadores únicos.
- Semillas aleatorias reproducibles.

Las entidades generadas inicialmente son:

- TB_CLIENTES_CORE
- TB_PRODUCTOS_CAT
- TB_MOV_FINANCIEROS
- TB_OBLIGACIONES
- TB_SUCURSALES_RED
- TB_COMISIONES_LOG



### 6. Configuración parametrizada

Los parametrizacion del archivo .yaml que se va a leer desde Python es la siguiente:

Nombre lde archivo: param_config.yaml

Actualmente el archivo contiene la semilla de generación, configuración general y volumen esperado por tabla.

Ejemplo:

yaml
seed: 20260909

global:
  country: "CO"
  reference_date: "2025-12-31"
  start_date: "2025-01-01"
  end_date: "2025-12-31"

tables:

  TB_CLIENTES_CORE:

    volume: 10000

    null_rates:
      score_buro: 0.05
      ciudad_res: 0.05


    anomalies:
      duplicate_documents: 20
      future_birth_dates: 10



  TB_PRODUCTOS_CAT:
    volume: 50

    anomalies:
      invalid_interest_rates: 2



  TB_MOV_FINANCIEROS:
    volume: 500000


  TB_OBLIGACIONES:
    volume: 30000

  TB_SUCURSALES_RED:
    volume: 200

  TB_COMISIONES_LOG :
    volume: 80000



El uso de una semilla permite reproducir la generación de datos bajo las mismas condiciones.
La parametrización de volúmenes permite modificar la cantidad de registros sin necesidad de modificar la lógica principal de generación. Se pueden realizar mas parametrizaciones, pero por tema de tiempo solo se deja este ejemplo.


### 7. Modelo de datos actual

El modelo está compuesto por entidades de clientes, productos, movimientos, obligaciones, sucursales y comisiones. Las principales relaciones son:

- movimientos se relaciona con clientes y productos
- Obligaciones se relaciona con clientes y productos
- Comisiones se relaciona con clientes y productos


### 8. Formatos de datos

La solución contempla el uso de diferentes formatos de almacenamiento.

Actualmente se generan archivos:

- CSV
- Parquet
- txt

Los archivos CSV son utilizados durante la etapa inicial de carga hacia SQL Server.


### 9. Base de datos y carga masiva

Para este caso se utiliza SQL Server para que haga la funcion de fuente de informacion, la cual almacena los datos de los archivos a traves de carga masiva.
Ejemplo:

BULK INSERT dbo.TB_CLIENTES_CORE
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_CLIENTES_CORE.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK
);


### 10. Validación de la carga

Después de realizar la carga se verifica el número de registros almacenados en cada tabla.

Ejemplo:

SELECT 'TB_CLIENTES_CORE' as nombre_tabla,COUNT(1) as cantidad_registros  FROM  dbo.TB_CLIENTES_CORE
UNION ALL
SELECT 'TB_PRODUCTOS_CAT' as nombre_tabla,COUNT(1) as cantidad_registros  FROM  dbo.TB_PRODUCTOS_CAT
UNION ALL
SELECT 'TB_SUCURSALES_RED' as nombre_tabla,COUNT(1) as cantidad_registros  FROM  dbo.TB_SUCURSALES_RED
UNION ALL
SELECT 'TB_MOV_FINANCIEROS' as nombre_tabla,COUNT(1) as cantidad_registros  FROM  dbo.TB_MOV_FINANCIEROS
UNION ALL
SELECT 'TB_OBLIGACIONES' as nombre_tabla,COUNT(1) as cantidad_registros  FROM  dbo.TB_OBLIGACIONES
UNION ALL
SELECT 'TB_COMISIONES_LOG' as nombre_tabla,COUNT(1) as cantidad_registros  FROM  dbo.TB_COMISIONES_LOG


### 11. Ejecucion del proceso

### 11.1 Generación de datos

Los scripts Python generan los archivos sintéticos correspondientes a cada entidad.

Ejemplo:

- python clientes.py
- python productos.py
- python movimientos.py
- python obligaciones.py
- python sucursales.py
- python comisiones.py

Los archivos generados son almacenados en:

data/csv/
data/parquet/


### 11.2 Creación de tablas

Ejecutar en SQL Server:
01_create_tables.sql

### 11.3 Carga de datos

Ejecutar:
02_insert_records.sql


### 12 Implementacion servicios cloud

para la implementacion de los servicios de Azure, es necesario creauna cuenta gratuita desde el pportal azure (descrito en el manual de cuentas) y una vez ya contemos con dicho manual, se debe crear un grupo de recursos.

### 12.1 Azure Data Lake Storage Gen2
La separación por zonas permite establecer diferentes niveles de procesamiento y facilita la trazabilidad de los datos durante el ciclo de transformación. Para lo anetrior se utilizara arquitectura medallon, para lo cual, es necesario crear una cuenta storage de Azure de tipo Data Lake Gen2 y alli diseñar la arquitectura en capas:

- Zona bronce: llega la data cruda, sin transformaciones
- zona silver: Se realizan algunas transformaciones a los datos
- zona gold: se crean los modelos de datos que van a ser consumidos para analitica
- zona refine: se publica datos de tipo privado y sensible.
- zona Landing: se cargan datos de forma manual.

La siguiente etapa consiste en realizar la ingesta de los archivos de origen hacia la capa Bronze del Data Lake.


### 12.2 Azure Data Factory
Se debe crear un servicio, el cual corresponde a Azure Data Factory para la ingesta y orquestación de los procesos. Esto se realiza desde Azure Portal.


### 12.3 Azure SQL Database
Se debe crear un servicio, el cual corresponde a Azure SQL Database para el almacenamiento de tablas de control. Esto se realiza desde Azure Portal.


### 12.4 Databricks
Se debe crear un servicio, el cual corresponde a Azure databricks para el almacenamiento de tablas de control. Esto se realiza desde Azure Portal. Allí se debe configurar el metastore, los catálogos, el workspace, etc. En ete caso, se debe crear en otro grupo de recursos ya que así lo recomienda Microsoft.

En Databricks es necesario configurar las ubicaciones externas o espacio de almacenamiento  ya que allí es donde se van a almacenar los datos físicos de los objetos creados en formato .parquet en Azure Data Lake Storage 

se deben crear los catalogos en donde se va a realizar el proceso de limpieza y modelos dimensionales


### 12.4 Azure Key Vault
Se debe crear un servicio, el cual corresponde a Azure Key Vault para la administracion de contraseñas que se van a utilizan en los diferentes servicios. Esto se realiza desde Azure Portal.

una vez ya tengamos el servicio creado, allí mismo se procede a crear y configurar los secretos. Hay que tener en cuenta que antes de crear el secreto, hay que dar asignar permisos de administrador de valores clave al usuario, esto se realiza en la opción control de acceso (IAM).

Luego se realiza la configuración y asignación del key vault en data factory, para lo cual también antes de configurar el secreto, es necesario asignar rol de administrador de key vault a Azure Data Factory.




### 13 proceso control cargas
Se diseña un proceso genérico el cual consiste en que se deja un archivo de Excel parametrizado en contenedor zona landing con las tablas que se van a procesar y desde allí, Azure data Factory carga la información a través de un upsert.

Para lograr lo anterior, se debe realizar una comparación de la información publicada vs la información que se ingesta, y para esto, se crea un esquema tipo stage para almacenar los datos en tablas temporales y luego realizar la comparación y actualización entre los datos.

Se genera un pipeline que permita extraer realizar la comparación e inserción de datos de forma automática. Se debe configurar un componente de copiar y datos que lleva la informacion de Landing a la tabla temporal y un script que realiza el upsert.

Finalmente, se diseña un proceso genérico el cual consiste en que se deja un archivo de Excel parametrizado en contenedor zona landing con las tablas que se van a procesar y desde allí, Azure data Factory carga la información a través de un upsert, donde recorre toda la información, valida que datos son nuevos y los inserta y los que han cambiado, los actualiza.

A continuacion se comparte la estructura de la tabla final.

--- sql

CREATE TABLE dbo.TablaControlCarga (
    id INT IDENTITY(1,1) PRIMARY KEY,
    esquema_origen NVARCHAR(100) NOT NULL,
    nombre_tabla_origen NVARCHAR(150) NOT NULL,
    ruta_destino NVARCHAR(1000) NOT NULL,
    carpeta_destino NVARCHAR(1000) NOT NULL,
    nombre_archivo_destino NVARCHAR(200) NOT NULL,
	  cantidad_registros INTEGER NOT NULL,
    estado_proceso NVARCHAR(50) NOT NULL,
    fecha_registros DATETIME NOT NULL,
    fecha_actualizacion DATETIME NOT NULL
);

---

script para realizar el upsert sobre los objetos en base de datos que se van a procesar.

--- 
MERGE dbo.TablaControlCarga AS T
USING stage.Tbl_tmp_ControlCarga AS S
ON T.esquema_origen = S.esquema_origen
   AND T.nombre_tabla_origen = S.nombre_tabla_origen

 when matched AND (
 T.ruta_destino <> S.ruta_destino or
 T.carpeta_destino <> S.carpeta_destino or
 T.nombre_archivo_destino <> S.nombre_archivo_destino
 ) then

  update set    
      ruta_destino = S.ruta_destino
      ,carpeta_destino = S.carpeta_destino
      ,nombre_archivo_destino = S.nombre_archivo_destino
      ,fecha_actualizacion = getdate()

WHEN NOT MATCHED BY TARGET THEN
    INSERT (esquema_origen,
            nombre_tabla_origen,
            ruta_destino,
            carpeta_destino,
            nombre_archivo_destino,
            estado_proceso,
            consulta,
            fecha_actualizacion)
    VALUES (S.esquema_origen,
            S.nombre_tabla_origen,
            S.ruta_destino,
            S.carpeta_destino,
            S.nombre_archivo_destino,
            'activo',
            'select * from',
            GETDATE());
---

Se debe configurar el linked service y en este caso, se debe configurar un integration runtime que debe ser hospedado, ya que la base de datos se encuentra en el equipo local.


### 14. capa de ingesta de datos 

Arquitectura medallon sencilla, en donde bronze conserva los datos tal cual como esta en la fuente, silver realiza estnadarizacion y limpieza y gold contiene modelos enriquecios.

### Zona bronze
La ingesta de datos en bronze es necesario desarrollar un pipeline, el cual permita consultar los datos en la base de datos origen y almacenarlos en el data lake de Azure. Para lo anterior se debe configurar inicialmente un lookup el cual va a consultar la tabla de control.

--- sql
select * from [dbo].[TablaControlCarga]
---

Luego se configura otro lookup, el cual va a buscar las tablas del sistema.

--- sql
select TABLE_SCHEMA, TABLE_NAME
from INFORMATION_SCHEMA.TABLES
---


Y se configuran 2 variables, la primera para calcular la fecha actual, que se va anexar al nombre del archivo que se va a generar y otra variable que va a guardar la lista de tablas que se van a procesar.

---
Variable1
@formatDateTime(utcNow(), 'yyyyMMdd')

Variable2
@concat(last(activity('LookupListarTablas').output.value).TABLE_SCHEMA,'.',last(activity('LookupListarTablas').output.value).TABLE_NAME)
---


Una vez ya se tenga todo configurado, se utiliza un for each para que recorra la lista que se configuró en el lookup que consulta la tabla de control de carga y se especifica que se necesitan consultar los valores de ese dataset.

---
@activity('Lookup control cargas').output.value

---

Dentro del for each, se configura un componente que se utiliza para copiar datos en donde el origen es una consulta select sobre las tablas del sistema (lookup 2) y el destino es la configuración de la ruta destino, el nombre del archivo concatenado con la variable de fecha (como el archivo debe quedar en formato parquet, se debe configurar el linked services apuntando a adls)

---
### Origen
@concat(item().consulta,' ',variables('listarTablas'))



### Destino
Nombre archivo
@concat(item().nombre_archivo_destino,'_',variables('fecha_actual'))

ruta_destino
@item().ruta_destino

carpeta_destino
@item().carpeta_destino

---


### Zona silver
Para llevar la información desde bronce hasta silver, primero es necesario crear los esquemas ya que los catálogos ya estaban definidos.
Para este ejercicio, se definieron 2 esquemas, uno para negocio en donde se van almacenar las tablas que corresponden al negocio (información de bronze) y otro esquema de calidad de datos, en donde se van almacenar los resultados de la calidad de datos.
Inicialmente se genera un notebook para definir la estructura de la solución.

Para más detalle, validar la carpeta /pipelines, alli se encuentra el notebook que generó el proceso.
Se genera un archivo que corresponde al diccionario de datos, que como tal, hace parte como artefacto de la solución desde allí se encuentra todo el detalle de cada tabla relacionada en el ejericico. Este archivo también se puede encontrar en la carpeta /pipelines.
Con el notebook de definición de estructura, se crea la tabla delta de calidad de los datos.


### Notebook 00_creacion_estructura
Se define la estructura de las tablas que se van a crear tanto las de negocio como las de calidad de datos.
-	Creación de tablas de calidad de datos
-	Creación de tablas de negocio
- Tabla de definición de reglas de calidad

### Notebook 01_calidad_bronze
Realiza las validaciones de calidad sobre los datos que llegan a Bronze, aplicando las reglas definidas y registrando los resultados y errores encontrados.
-	Creación de reglas de calidad de datos
-	Ejecución de proceso de calidad de datos
-	Log de datos con errores
-	Log tabla de resultados
 
### Notebook 02_bronze_to_silver
Toma los datos de Bronze, realiza la limpieza, transformación y estandarización de la información y los deja disponibles en Silver. También calcula algunas reglas de negocio necesarias para las siguientes etapas. Se diseña un proceso genérico que ejecuta las reglas de calidad, el cual valida que registros se encuentran en el log de errores de calidad y compara cuales no están, y estos son los que se cargan en las tablas de silver. Muy importante mencionar que, hay que renombrar las tablas, ay que las reglas de calidad están configuradas con los nombres de los campos nuevos y el proceso lee los archivos en bronce, por lo cual, llos nombres de los campos quedan tal cual como esta en el origen, lo que dificulta ejecutar las reglas de calidad.


### Notebook 03_silver_to_gold
Toma la información de Silver y construye las dimensiones y tablas de hechos requeridos en Gold, dejando los datos preparados para su consumo analítico.

Todos los procesos anteriores corresponden a tablas delta, los cuales se actualizan con merge.


### Datos enmascarados
Para los datos enmascarados en necesario crear una función en databricks para realizar dicha acción. Lo anterior se realiza a traves de consultas SQL.

--- 
sql

CREATE OR REPLACE FUNCTION silver.gobierno.mask_texto(valor STRING)
RETURN concat('**********', right(valor, 3));
---

Por ultimo se realiza la inclusión de los notebooks en nuestro flujo de datos en Azure Data Factory, en donde solamente se van a ejecutar los notebooks anteriormente mencionados 


