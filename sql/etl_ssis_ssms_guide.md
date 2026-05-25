# Guía de ETL SSIS / SSMS para el DW local

## Conexión local

- Servidor: `(localdb)\MSSQLLocalDB`
- Base de datos: `iot_alumbrado_paipa`
- Archivo con definición DW: `sql/seed_somee_dw.sql`

## Estado actual verificado

En la base de datos local ya hay:

- `dbo.medicion`: 1,047,616 registros
- `dw.FactMediciones`: 1,000,000 registros
- Dimensiones cargadas:
  - `dw.DimUbicacion`: 4
  - `dw.DimDispositivo`: 4
  - `dw.DimSensor`: 16
  - `dw.DimEstado`: 6
  - `dw.DimUsuario`: 3
  - `dw.DimTiempo`: 731

> Esto significa que ya tienes 1 millón de filas de hechos en el almacén de datos local, que es la fuente ideal para un modelo multidimensional o cubo SSAS.

## Pasos en SSMS

1. Abrir SQL Server Management Studio.
2. Conectarse a `(localdb)\\MSSQLLocalDB` y a la base `iot_alumbrado_paipa`.
3. Ejecutar el contenido de `sql/seed_somee_dw.sql` para crear el esquema `dw`, las dimensiones y la tabla de hechos.
4. Verificar con estas consultas:

```sql
SELECT COUNT(*) AS total_mediciones FROM dbo.medicion;
SELECT COUNT(*) AS total_fact_mediciones FROM dw.FactMediciones;
SELECT COUNT(*) AS total_dim_ubicacion FROM dw.DimUbicacion;
SELECT COUNT(*) AS total_dim_dispositivo FROM dw.DimDispositivo;
SELECT COUNT(*) AS total_dim_sensor FROM dw.DimSensor;
SELECT COUNT(*) AS total_dim_estado FROM dw.DimEstado;
SELECT COUNT(*) AS total_dim_usuario FROM dw.DimUsuario;
SELECT COUNT(*) AS total_dim_tiempo FROM dw.DimTiempo;
```

## Diseño sugerido de paquete SSIS en Visual Studio

### 1. Control Flow

- Ejecutar `Execute SQL Task` para crear el esquema y las tablas usando `sql/seed_somee_dw.sql`.
- Agregar un `Data Flow Task` para cargar dimensiones.
- Agregar otro `Data Flow Task` para cargar hechos.

### 2. Carga de dimensiones

Para cada dimensión:

- Usar un origen OLE DB desde la tabla operativa correspondiente (`dbo.ubicacion`, `dbo.dispositivo_iot`, `dbo.sensor`, `dbo.medicion`, etc.).
- Agregar un `Lookup` sobre la dimensión destino `dw.Dim...` para evitar duplicados.
- En caso de no existir, insertar en la dimensión destino.

### 3. Carga de hechos `dw.FactMediciones`

- Usar `dbo.medicion` como origen principal.
- Agregar `Lookup` para obtener las claves surrogate de cada dimensión: `TiempoKey`, `UbicacionKey`, `DispositivoKey`, `SensorKey`, `EstadoKey`, `UsuarioKey`.
- Agregar columnas derivadas para `FechaCarga`, `Cantidades`, `Fuente`, `CalidadDato`, etc.
- Insertar en `dw.FactMediciones`.

### 4. Validación final

- Ejecutar la siguiente consulta para confirmar que el DW tiene 1,000,000 registros:

```sql
SELECT COUNT(*) AS total_fact_mediciones FROM dw.FactMediciones;
```

- Si usas un cubo SSAS multidimensional, procesa el cubo después de cargar los hechos. El número de filas del grupo de medidas se calculará a partir de `dw.FactMediciones`.

## Cómo mostrar el millón de registros en el modelo multidimensional

- En SSAS, crea una nueva base de datos de análisis o un cubo que use `dw.FactMediciones` como tabla de hechos.
- Usa las dimensiones `dw.DimUbicacion`, `dw.DimDispositivo`, `dw.DimSensor`, `dw.DimEstado`, `dw.DimUsuario`, `dw.DimTiempo`.
- Procesa el cubo.
- Revisa la vista de exploración del cubo; el total de filas del grupo de medidas debe reflejar 1,000,000 hechos si la carga y el procesamiento se realizaron correctamente.

## Recomendaciones

- Si necesitas que prepare el flujo exacto de SSIS (tareas, conexiones OLE DB, lookups, transformaciones), puedo darte el diseño completo paso a paso.
- Si prefieres, también puedo generar el script T-SQL que carga la tabla de hechos con 1,000,000 de filas a partir de `dbo.medicion` y la valida directamente en SSMS.
