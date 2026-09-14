use db_FinBank;

-- Insercion de registros desde los archivos

BULK INSERT dbo.TB_CLIENTES_CORE
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_CLIENTES_CORE.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);


BULK INSERT dbo.TB_COMISIONES_LOG
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_COMISIONES_LOG.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);


BULK INSERT dbo.TB_MOV_FINANCIEROS
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_MOV_FINANCIEROS.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);


BULK INSERT dbo.TB_OBLIGACIONES
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_OBLIGACIONES.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);


BULK INSERT dbo.TB_PRODUCTOS_CAT
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_PRODUCTOS_CAT.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);


BULK INSERT dbo.TB_SUCURSALES_RED
FROM 'C:\Users\carli\PycharmProjects\PythonProject\data\csv\TB_SUCURSALES_RED.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);


--- Validación carga de datos

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



