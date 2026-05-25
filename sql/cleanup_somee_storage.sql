-- Script de limpieza ligero para liberar espacio en la base de datos Somee.
-- Ejecútalo solo si estás seguro de que los datos históricos no son necesarios.
-- Ajusta las condiciones de fecha según tu modelo y política de retención.
-- Primero, identifica la columna de fecha correcta en la tabla dw.FactMediciones:
--
-- SELECT c.name AS ColumnName, t.name AS DataType
-- FROM sys.columns c
-- JOIN sys.types t ON c.user_type_id = t.user_type_id
-- JOIN sys.objects o ON c.object_id = o.object_id
-- WHERE o.name = 'FactMediciones' AND schema_name(o.schema_id) = 'dw'
-- ORDER BY c.column_id;
--
-- Reemplaza <NombreColumnaFecha> en las siguientes instrucciones por la columna real.

BEGIN TRANSACTION;

-- 1) Eliminar mediciones muy antiguas de la tabla de hechos.
-- La columna de fecha correcta en FactMediciones es FechaCarga.
IF OBJECT_ID(N'dw.FactMediciones', N'U') IS NOT NULL
BEGIN
    DELETE TOP (1000)
    FROM dw.FactMediciones
    WHERE FechaCarga < DATEADD(month, -6, SYSUTCDATETIME());
END;

-- 2) Eliminar logs de auditoría antiguos (> 60 días), solo si la tabla existe.
IF OBJECT_ID(N'dbo.audit_logs', N'U') IS NOT NULL
BEGIN
    DELETE TOP (1000)
    FROM dbo.audit_logs
    WHERE CreatedAt < DATEADD(day, -60, SYSUTCDATETIME());
END;

-- 3) Eliminar registros de proyecto antiguos (> 90 días), solo si la tabla existe.
IF OBJECT_ID(N'dbo.project_records', N'U') IS NOT NULL
BEGIN
    DELETE TOP (1000)
    FROM dbo.project_records
    WHERE MeasurementDate < DATEADD(day, -90, SYSUTCDATETIME());
END;

COMMIT TRANSACTION;

-- Nota: Si tu usuario tiene permisos, este comando puede liberar espacio en el archivo de registro.
-- Úsalo solo si no se incumple la política de Somee.
-- DBCC SHRINKFILE(N'<NombreDelArchivoDeRegistro>', 1);

PRINT 'Limpieza ligera completada. Revisa el espacio disponible y repite si es necesario.';
