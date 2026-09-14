---- Se debe crear la base de datos correspondiente al banco
create database db_FinBank;
use db_FinBank;

-- Elimina las tablas si existen:
drop table if exists dbo.TB_CLIENTES_CORE;
drop table if exists dbo.TB_PRODUCTOS_CAT;
drop table if exists dbo.TB_SUCURSALES_RED;
drop table if exists dbo.TB_MOV_FINANCIEROS;
drop table if exists dbo.TB_OBLIGACIONES;
drop table if exists dbo.TB_COMISIONES_LOG;

-- DDL para crear las tablas
-- En este caso no se asignan llaves primarias y/o foraneas ya que 
-- no permitiria que se realizara la prueba en calidad de datos con data duplicada.

CREATE TABLE dbo.TB_CLIENTES_CORE
(
    id_cli INTEGER NOT NULL,
    nomb_cli VARCHAR(100) NOT NULL,
    apell_cli VARCHAR(100) NOT NULL,
    tip_doc VARCHAR(10) NOT NULL,
    num_doc VARCHAR(30) NOT NULL,
    fec_nac DATE NOT NULL,
    fec_alta DATE NOT NULL,
    cod_segmento VARCHAR(30) NOT NULL,
    score_buro VARCHAR(30) NULL,
    ciudad_res VARCHAR(50) NULL,
    depto_res VARCHAR(50) NULL,
    estado_cli VARCHAR(20) NOT NULL,
    canal_adquis VARCHAR(30) NULL
);


CREATE TABLE dbo.TB_PRODUCTOS_CAT
(
    cod_prod VARCHAR(3) NOT NULL,
    desc_prod VARCHAR(100) NOT NULL,
    tip_prod VARCHAR(30) NOT NULL,
    tasa_ea DECIMAL(8,4) NOT NULL,
    plazo_max_meses INTEGER NOT NULL,
    cuota_min DECIMAL(18,2) NOT NULL,
    comision_admin DECIMAL(18,2) NOT NULL,
    estado_prod VARCHAR(20) NOT NULL
);


CREATE TABLE dbo.TB_SUCURSALES_RED
(
    cod_suc VARCHAR(10) NOT NULL,
    nom_suc VARCHAR(100) NOT NULL,
    tip_punto VARCHAR(30) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    depto VARCHAR(50) NOT NULL,
    latitud DECIMAL(10,7) NOT NULL,
    longitud DECIMAL(10,7) NOT NULL,
    activo CHAR(7) NOT NULL
);


CREATE TABLE dbo.TB_MOV_FINANCIEROS
(
    id_mov BIGINT NOT NULL,
    id_cli INTEGER NOT NULL,
    cod_prod VARCHAR(3) NOT NULL,
    num_cuenta VARCHAR(20) NOT NULL,
    fec_mov DATE NOT NULL,
    hra_mov TIME NOT NULL,
    vr_mov DECIMAL(18,2) NOT NULL,
    tip_mov VARCHAR(20) NOT NULL,
    cod_canal VARCHAR(20) NOT NULL,
    cod_ciudad VARCHAR(50) NOT NULL,
    cod_estado_mov VARCHAR(20) NOT NULL,
    id_dispositivo VARCHAR(30) NOT NULL
);


CREATE TABLE dbo.TB_OBLIGACIONES
(
    id_oblig BIGINT NOT NULL,
    id_cli INTEGER NOT NULL,
    cod_prod VARCHAR(3) NOT NULL,
    vr_aprobado DECIMAL(18,2) NOT NULL,
    vr_desembolsado DECIMAL(18,2) NOT NULL,
    sdo_capital DECIMAL(18,2) NOT NULL,
    vr_cuota DECIMAL(18,2) NOT NULL,
    fec_desembolso DATE NOT NULL,
    fec_venc DATE NOT NULL,
    dias_mora_act INTEGER NOT NULL,
    num_cuotas_pend INTEGER NOT NULL,
    calif_riesgo VARCHAR(5) NOT NULL
);

CREATE TABLE dbo.TB_COMISIONES_LOG
(
    id_comision BIGINT NOT NULL,
    id_cli INTEGER NOT NULL,
    cod_prod VARCHAR(3) NOT NULL,
    fec_cobro DATE NOT NULL,
    vr_comision DECIMAL(18,2) NOT NULL,
    tip_comision VARCHAR(30) NOT NULL,
    estado_cobro VARCHAR(20) NOT NULL
);


