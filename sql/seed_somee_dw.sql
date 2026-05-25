-- Seed del DW basado en el modelo operacional real del proyecto.

SET NOCOUNT ON;

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'dw')
BEGIN
    EXEC('CREATE SCHEMA dw');
END;

IF OBJECT_ID(N'dw.DimUbicacion', N'U') IS NULL
BEGIN
    CREATE TABLE dw.DimUbicacion (
        UbicacionKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        IdUbicacionOrigen INT NOT NULL,
        CodigoUbicacion NVARCHAR(30) NOT NULL,
        NombreUbicacion NVARCHAR(150) NOT NULL,
        TipoEspacio NVARCHAR(50) NOT NULL,
        NombreZona NVARCHAR(150) NOT NULL,
        TipoZona NVARCHAR(50) NOT NULL,
        Municipio NVARCHAR(100) NOT NULL,
        Departamento NVARCHAR(100) NOT NULL,
        Latitud DECIMAL(10, 7) NOT NULL,
        Longitud DECIMAL(10, 7) NOT NULL,
        Direccion NVARCHAR(255) NULL,
        Referencia NVARCHAR(255) NULL,
        Activo BIT NOT NULL
    );
END;

IF OBJECT_ID(N'dw.DimDispositivo', N'U') IS NULL
BEGIN
    CREATE TABLE dw.DimDispositivo (
        DispositivoKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        IdDispositivoOrigen INT NOT NULL,
        CodigoDispositivo NVARCHAR(50) NOT NULL,
        Modelo NVARCHAR(100) NOT NULL,
        Fabricante NVARCHAR(100) NULL,
        VersionFirmware NVARCHAR(50) NULL,
        Protocolo NVARCHAR(50) NOT NULL,
        Estado NVARCHAR(50) NOT NULL,
        FechaInstalacion DATE NULL,
        UltimoReporte DATETIME2 NULL
    );
END;

IF OBJECT_ID(N'dw.DimSensor', N'U') IS NULL
BEGIN
    CREATE TABLE dw.DimSensor (
        SensorKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        IdSensorOrigen INT NOT NULL,
        CodigoSensor NVARCHAR(50) NOT NULL,
        NombreSensor NVARCHAR(100) NOT NULL,
        ModeloHardware NVARCHAR(100) NULL,
        UnidadMedida NVARCHAR(50) NOT NULL,
        ValorMinimo DECIMAL(18, 4) NULL,
        ValorMaximo DECIMAL(18, 4) NULL,
        Estado NVARCHAR(50) NOT NULL,
        IntervaloLecturaSeg INT NOT NULL
    );
END;

IF OBJECT_ID(N'dw.DimEstado', N'U') IS NULL
BEGIN
    CREATE TABLE dw.DimEstado (
        EstadoKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        CodigoEstado NVARCHAR(40) NOT NULL,
        TipoEstado NVARCHAR(40) NOT NULL,
        Descripcion NVARCHAR(200) NULL
    );
END;

IF OBJECT_ID(N'dw.DimUsuario', N'U') IS NULL
BEGIN
    CREATE TABLE dw.DimUsuario (
        UsuarioKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        IdUsuarioOrigen INT NOT NULL,
        Nombres NVARCHAR(100) NOT NULL,
        Apellidos NVARCHAR(100) NOT NULL,
        Correo NVARCHAR(150) NOT NULL,
        Rol NVARCHAR(50) NOT NULL,
        Estado NVARCHAR(50) NOT NULL
    );
END;

IF OBJECT_ID(N'dw.DimTiempo', N'U') IS NULL
BEGIN
    CREATE TABLE dw.DimTiempo (
        TiempoKey INT NOT NULL PRIMARY KEY,
        Fecha DATE NOT NULL,
        Anio SMALLINT NOT NULL,
        Semestre TINYINT NOT NULL,
        Trimestre TINYINT NOT NULL,
        Mes TINYINT NOT NULL,
        NombreMes NVARCHAR(20) NOT NULL,
        NombreDia NVARCHAR(20) NOT NULL,
        Dia SMALLINT NOT NULL,
        SemanaAnio SMALLINT NOT NULL,
        EsFinDeSemana BIT NOT NULL,
        EsFestivo BIT NOT NULL,
        Hora TINYINT NOT NULL,
        Minuto TINYINT NOT NULL,
        FechaHora DATETIME2 NULL
    );
END;

IF OBJECT_ID(N'dw.FactMediciones', N'U') IS NULL
BEGIN
    CREATE TABLE dw.FactMediciones (
        FactMedicionKey BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        TiempoKey INT NOT NULL,
        UbicacionKey INT NOT NULL,
        DispositivoKey INT NOT NULL,
        SensorKey INT NOT NULL,
        EstadoKey INT NOT NULL,
        UsuarioKey INT NULL,
        IdMedicionOrigen BIGINT NOT NULL,
        ValorMedicion DECIMAL(18, 4) NOT NULL,
        ValorLux DECIMAL(18, 4) NULL,
        ValorTemperatura DECIMAL(18, 4) NULL,
        ValorCorriente DECIMAL(18, 4) NULL,
        ValorMovimiento DECIMAL(18, 4) NULL,
        ConsumoKwh DECIMAL(18, 4) NULL,
        AlertasGeneradas BIT NOT NULL,
        CalidadDato NVARCHAR(50) NOT NULL,
        Fuente NVARCHAR(50) NOT NULL,
        CantidadMediciones INT NOT NULL,
        FechaCarga DATETIME2 NOT NULL
    );
END;

IF NOT EXISTS (SELECT 1 FROM dw.DimEstado)
BEGIN
    INSERT INTO dw.DimEstado (CodigoEstado, TipoEstado, Descripcion)
    VALUES
        (N'operativo_normal', N'operacion', N'Lectura sin alerta y con dispositivos activos.'),
        (N'alerta_activa', N'alerta', N'Existe alerta activa sobre la luminaria o el sensor.'),
        (N'mantenimiento', N'mantenimiento', N'Luminaria o dispositivo en mantenimiento.'),
        (N'falla', N'operacion', N'Dispositivo, sensor o luminaria en estado de falla.'),
        (N'sin_senal', N'conectividad', N'El dispositivo no reporta comunicacion.');
END;

;WITH ubicaciones_src AS (
    SELECT
        u.id_ubicacion,
        u.codigo_ubicacion,
        u.nombre_ubicacion,
        u.tipo_espacio,
        u.NombreZona,
        u.TipoZona,
        u.Municipio,
        u.Departamento,
        u.Latitud,
        u.Longitud,
        u.Direccion,
        u.Referencia,
        u.Activo
    FROM dbo.ubicacion u
)
INSERT INTO dw.DimUbicacion (
    IdUbicacionOrigen, CodigoUbicacion, NombreUbicacion, TipoEspacio, NombreZona, TipoZona,
    Municipio, Departamento, Latitud, Longitud, Direccion, Referencia, Activo
)
SELECT
    s.id_ubicacion,
    s.codigo_ubicacion,
    s.nombre_ubicacion,
    s.tipo_espacio,
    s.NombreZona,
    s.TipoZona,
    s.Municipio,
    s.Departamento,
    s.Latitud,
    s.Longitud,
    s.Direccion,
    s.Referencia,
    s.Activo
FROM ubicaciones_src s
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.DimUbicacion d
    WHERE d.IdUbicacionOrigen = s.id_ubicacion
);

;WITH dispositivos_src AS (
    SELECT
        d.id_dispositivo,
        d.codigo_dispositivo,
        d.modelo,
        d.fabricante,
        d.version_firmware,
        d.protocolo,
        d.estado,
        d.fecha_instalacion,
        d.ultimo_reporte
    FROM dbo.dispositivo_iot d
)
INSERT INTO dw.DimDispositivo (
    IdDispositivoOrigen, CodigoDispositivo, Modelo, Fabricante, VersionFirmware, Protocolo, Estado, FechaInstalacion, UltimoReporte
)
SELECT
    s.id_dispositivo,
    s.codigo_dispositivo,
    s.modelo,
    s.fabricante,
    s.version_firmware,
    s.protocolo,
    s.estado,
    s.fecha_instalacion,
    s.ultimo_reporte
FROM dispositivos_src s
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.DimDispositivo d
    WHERE d.IdDispositivoOrigen = s.id_dispositivo
);

;WITH sensores_src AS (
    SELECT
        s.id_sensor,
        s.id_dispositivo,
        s.id_tipo_sensor,
        s.codigo_sensor,
        s.estado,
        s.fecha_calibracion,
        s.intervalo_lectura_seg,
        ts.nombre,
        ts.modelo_hardware,
        ts.unidad_medida,
        ts.valor_minimo,
        ts.valor_maximo
    FROM dbo.sensor s
    INNER JOIN dbo.tipo_sensor ts ON ts.id_tipo_sensor = s.id_tipo_sensor
)
INSERT INTO dw.DimSensor (
    IdSensorOrigen, CodigoSensor, NombreSensor, ModeloHardware, UnidadMedida, ValorMinimo, ValorMaximo, Estado, IntervaloLecturaSeg
)
SELECT
    s.id_sensor,
    s.codigo_sensor,
    s.nombre,
    s.modelo_hardware,
    s.unidad_medida,
    s.valor_minimo,
    s.valor_maximo,
    s.estado,
    s.intervalo_lectura_seg
FROM sensores_src s
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.DimSensor d
    WHERE d.IdSensorOrigen = s.id_sensor
);

;WITH fechas_src AS (
    SELECT DISTINCT CAST(m.fecha_hora AS date) AS Fecha
    FROM dbo.medicion m
)
INSERT INTO dw.DimTiempo (
    TiempoKey, Fecha, Anio, Semestre, Trimestre, Mes, NombreMes, NombreDia, Dia, SemanaAnio, EsFinDeSemana, EsFestivo, Hora, Minuto
)
SELECT
    CONVERT(INT, CONVERT(CHAR(8), f.Fecha, 112)) AS TiempoKey,
    f.Fecha,
    DATEPART(year, f.Fecha),
    CASE WHEN DATEPART(month, f.Fecha) <= 6 THEN 1 ELSE 2 END,
    DATEPART(quarter, f.Fecha),
    DATEPART(month, f.Fecha),
    DATENAME(month, f.Fecha),
    DATENAME(weekday, f.Fecha),
    DATEPART(day, f.Fecha),
    DATEPART(iso_week, f.Fecha),
    CASE WHEN DATEPART(weekday, f.Fecha) IN (1, 7) THEN 1 ELSE 0 END,
    0,
    0,
    0
FROM fechas_src f
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.DimTiempo t
    WHERE t.Fecha = f.Fecha
);

;WITH mediciones_src AS (
    SELECT
        m.id_medicion,
        m.id_sensor,
        m.fecha_hora,
        m.valor,
        m.calidad_dato,
        m.fuente,
        m.created_at,
        s.id_dispositivo,
        s.id_tipo_sensor,
        s.estado AS estado_sensor,
        ts.nombre AS nombre_tipo_sensor,
        ts.unidad_medida,
        ts.valor_minimo,
        ts.valor_maximo,
        d.id_luminaria,
        l.id_ubicacion
    FROM dbo.medicion m
    INNER JOIN dbo.sensor s ON s.id_sensor = m.id_sensor
    INNER JOIN dbo.tipo_sensor ts ON ts.id_tipo_sensor = s.id_tipo_sensor
    INNER JOIN dbo.dispositivo_iot d ON d.id_dispositivo = s.id_dispositivo
    INNER JOIN dbo.luminaria l ON l.id_luminaria = d.id_luminaria
)
INSERT INTO dw.FactMediciones (
    TiempoKey, UbicacionKey, DispositivoKey, SensorKey, EstadoKey, UsuarioKey, IdMedicionOrigen,
    ValorMedicion, ValorLux, ValorTemperatura, ValorCorriente, ValorMovimiento,
    ConsumoKwh, AlertasGeneradas, CalidadDato, Fuente, CantidadMediciones, FechaCarga
)
SELECT
    t.TiempoKey,
    u.UbicacionKey,
    dd.DispositivoKey,
    ds.SensorKey,
    CASE
        WHEN ms.valor < ISNULL(ms.valor_minimo, ms.valor) OR ms.valor > ISNULL(ms.valor_maximo, ms.valor) THEN ISNULL((SELECT TOP 1 EstadoKey FROM dw.DimEstado WHERE CodigoEstado = N'alerta_activa'), 2)
        WHEN LOWER(ms.estado_sensor) LIKE '%mant%' THEN ISNULL((SELECT TOP 1 EstadoKey FROM dw.DimEstado WHERE CodigoEstado = N'mantenimiento'), 3)
        WHEN LOWER(ms.estado_sensor) LIKE '%fall%' THEN ISNULL((SELECT TOP 1 EstadoKey FROM dw.DimEstado WHERE CodigoEstado = N'falla'), 4)
        ELSE ISNULL((SELECT TOP 1 EstadoKey FROM dw.DimEstado WHERE CodigoEstado = N'operativo_normal'), 1)
    END AS EstadoKey,
    NULL AS UsuarioKey,
    ms.id_medicion,
    ms.valor,
    CASE WHEN LOWER(ISNULL(ms.unidad_medida, N'')) IN (N'lux', N'lx') THEN ms.valor END,
    CASE WHEN LOWER(ISNULL(ms.unidad_medida, N'')) LIKE N'%c%' AND LOWER(ISNULL(ms.nombre_tipo_sensor, N'')) LIKE N'%temper%' THEN ms.valor END,
    CASE WHEN LOWER(ISNULL(ms.unidad_medida, N'')) IN (N'a', N'amper', N'amperio', N'amp') OR LOWER(ISNULL(ms.nombre_tipo_sensor, N'')) LIKE N'%corr%' THEN ms.valor END,
    CASE WHEN LOWER(ISNULL(ms.nombre_tipo_sensor, N'')) LIKE N'%mov%' THEN ms.valor END,
    ms.valor,
    CASE WHEN ms.valor < ISNULL(ms.valor_minimo, ms.valor) OR ms.valor > ISNULL(ms.valor_maximo, ms.valor) THEN 1 ELSE 0 END,
    ms.calidad_dato,
    ms.fuente,
    1,
    ms.created_at
FROM mediciones_src ms
INNER JOIN dw.DimTiempo t ON t.Fecha = CAST(ms.fecha_hora AS date)
INNER JOIN dw.DimUbicacion u ON u.IdUbicacionOrigen = ms.id_ubicacion
INNER JOIN dw.DimDispositivo dd ON dd.IdDispositivoOrigen = ms.id_dispositivo
INNER JOIN dw.DimSensor ds ON ds.IdSensorOrigen = ms.id_sensor
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.FactMediciones f
    WHERE f.IdMedicionOrigen = ms.id_medicion
);

-- If you need a clean demo reload, uncomment the DELETE statements below and rerun.
-- DELETE FROM dw.FactMediciones;
-- DELETE FROM dw.DimTiempo;
-- DELETE FROM dw.DimSensor;
-- DELETE FROM dw.DimDispositivo;
-- DELETE FROM dw.DimUbicacion;