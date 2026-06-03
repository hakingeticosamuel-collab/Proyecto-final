# Presentación del Proyecto: Sistema Inteligente de Alumbrado Público

## 1. Resumen ejecutivo

Este proyecto integra una solución completa de ciudad inteligente aplicada al alumbrado público de Paipa, Boyacá. Incluye:

- Prototipo IoT con sensores de luz, presencia, corriente y temperatura.
- Base de datos operacional en SQL Server (Somee) para registrar mediciones y dispositivos.
- Proceso ETL para cargar y transformar datos en un Data Warehouse (DW).
- Modelo multidimensional para análisis eficiente.
- Dashboard en Power BI para visualización.
- Publicación web en Flask + Vue 3 desplegada en Render.

## 2. Arquitectura general

La arquitectura del proyecto sigue este flujo:

1. Prototipo IoT → 2. SQL Server (operacional) → 3. ETL → 4. Data Warehouse → 5. Power BI → 6. Web en Flask

### Componentes

- `SQL Server Somee`: almacena la información operativa.
- `DW` con esquema `dw`: guarda dimensiones y hechos preparados para análisis.
- `Power BI`: consume el DW y muestra indicadores estratégicos.
- `Flask + Vue 3`: publica la aplicación web accesible en la URL final.

## 3. Modelo relacional

El modelo relacional es la base operativa del proyecto. Está compuesto por tablas principales como:

- `dbo.ubicacion`: puntos físicos y zonas de la maqueta.
- `dbo.dispositivo_iot`: luminarias, controladores y dispositivos conectados.
- `dbo.sensor`: sensores instalados en los dispositivos.
- `dbo.medicion`: registros de lectura de sensores con `fecha_hora`, `valor`, `calidad_dato` y `fuente`.
- Tablas auxiliares de estado y usuarios.

### Para qué sirve

- Registra los datos en bruto tal como los genera el prototipo o la simulación.
- Soporta consultas operativas y sirve como origen para el ETL.

## 4. Simulación de datos para Big Data

Esta parte es clave para justificar la maqueta y el volumen de información.

### ¿Qué es?

Se simula el comportamiento de los sensores porque la maqueta no está desplegada a escala real. El objetivo es recrear el flujo de datos que un sistema de alumbrado inteligente generaría en producción.

### ¿Cómo se hace?

- Se utiliza un procedimiento almacenado en SQL Server que genera 1.000.000 de lecturas.
- Cada 15 minutos se crea un valor por sensor activo en el período simulado.
- Se modela la distribución real del dato:
  - Luminosidad: 0–800 lux
  - Presencia: binario 0/1
  - Corriente: 0–12 A
  - Temperatura: 18–53 °C
- La calidad del dato también se simula: 95% válido, 3% dudoso y 2% fuera de rango.

### Resultado

- 1.000.000 registros en `dbo.medicion`.
- Esta muestra permite validar los procesos ETL, el rendimiento del DW y la visualización sin necesidad de infraestructura física completa.

### Texto mejorado para presentar

> Esta es la parte de Big Data: tenemos un volumen de un millón de filas generadas con la misma frecuencia y rangos que tendría el sistema real. Esto nos permite validar toda la arquitectura sin necesitar la infraestructura física desplegada.

### Pregunta probable del jurado

- **¿Por qué simulan y no usan datos reales?**
  - La maqueta es demostrativa; la simulación es una práctica estándar en Big Data para validar pipelines antes del despliegue a producción.
  - Con datos simulados podemos garantizar el volumen, la variedad y la calidad del flujo de información sin depender de un sistema real que aún no está desplegado.

## 5. Modelo multidimensional

El DW usa un esquema estrella con las siguientes tablas:

- `dw.DimUbicacion`
- `dw.DimDispositivo`
- `dw.DimSensor`
- `dw.DimEstado`
- `dw.DimUsuario`
- `dw.DimTiempo`
- `dw.FactMediciones`

### ¿Para qué funciona?

- El modelo multidimensional organiza los datos por dimensiones y medidas.
- Facilita consultas analíticas rápidas y agregadas.
- Soporta visualizaciones de tendencias, comparativos y análisis por zona, sensor, tiempo y estado.

### Qué aporta

- Reduce la complejidad de las consultas respecto al modelo relacional puro.
- Permite generar métricas como conteo de mediciones, alertas, valores promedio y comportamiento por periodo.

## 6. ETL en Visual Studio / SSIS / SSMS

### Objetivo del ETL

- Extraer datos de las tablas operativas de SQL Server.
- Transformarlos para limpiar, normalizar y obtener claves de dimensiones.
- Cargarlos en el DW en `dw.FactMediciones` y dimensiones correlacionadas.

### Pasos principales

1. Crear el esquema `dw` y las tablas de dimensiones/hechos con `sql/seed_somee_dw.sql`.
2. Cargar dimensiones:
   - `DimUbicacion`
   - `DimDispositivo`
   - `DimSensor`
   - `DimEstado`
   - `DimUsuario`
   - `DimTiempo`
3. Cargar hechos:
   - Usar `dbo.medicion` como origen.
   - Obtener las claves surrogate de cada dimensión con `Lookup`.
   - Insertar en `dw.FactMediciones`.
4. Validar la carga: `SELECT COUNT(*) FROM dw.FactMediciones;` debe devolver 1.000.000.

### Cómo explicar el ETL

- El ETL convierte datos operativos en información analítica.
- Cada dimensión recibe su versión limpia y normalizada.
- El hecho `FactMediciones` es la tabla central que une tiempo, ubicación, sensor, dispositivo y estado.

## 7. Dashboard

### Qué muestra

- Estado general de las mediciones.
- Tendencias de consumo y de variables ambientales.
- Calidad de datos y alertas.
- Comparación por zonas, dispositivos y tipos de sensor.

### Herramientas usadas

- Power BI Desktop para construir el reporte.
- Power BI Service para publicar y compartir.
- Enlace público del reporte: `https://app.powerbi.com/view?r=...`.

### Para qué funciona

- Convierte los resultados del DW en insights visuales.
- Permite a un usuario no técnico entender el comportamiento del sistema.
- Sirve como evidencia de la capa analítica del proyecto.

## 8. Resultados del análisis multidimensional

### Indicadores principales

- Volumen total de mediciones.
- Última fecha de reporte.
- Distribución por sensor y por zona.
- Calidad de datos y detección de valores fuera de rango.
- Alertas generadas por estado del dispositivo.

### Qué demuestra

- El DW puede manejar un volumen de 1.000.000 de hechos.
- El modelo multidimensional entrega resultados rápidos.
- Power BI puede consumir ese modelo y presentar insights claros.

## 9. Del proceso al resultado web

### 1. Partimos de la maqueta IoT

- El prototipo genera datos de sensores.
- Estos datos llegan a SQL Server en bruto.

### 2. Armamos el modelo relacional

- Definimos tablas de ubicación, dispositivo, sensor y medición.
- Ese diseño soporta la captura del flujo de datos.

### 3. Simulamos Big Data

- Generamos 1.000.000 de registros para recrear volumen real.
- Validamos la arquitectura sin depender del despliegue físico.

### 4. Construimos el ETL y el DW

- Creamos el esquema `dw`.
- Cargamos dimensiones y hechos.
- Obtenemos un modelo listo para análisis.

### 5. Construimos el dashboard

- Power BI consume el DW.
- Creamos visualizaciones significativas.

### 6. Publicamos la solución web

- Flask sirve la aplicación y el frontend Vue.
- Se despliega en Render.
- La URL de acceso final es `https://proyecto-final-24st.onrender.com/app`.

## 10. Guía para la presentación

### Orden recomendado de diapositivas

1. Problema y objetivo del proyecto.
2. Prototipo IoT y maqueta.
3. Modelo relacional y almacenamiento operativo.
4. Simulación de Big Data.
5. ETL y Data Warehouse.
6. Dashboard Power BI.
7. Publicación web.
8. Resultados y conclusiones.

### Qué decir en cada sección

- **Problema:** mostrar la necesidad de un alumbrado inteligente y la importancia del monitoreo.
- **IoT:** explicar sensores, lecturas y funcionamiento del prototipo.
- **Relacional:** decir que es la estructura de entrada de datos.
- **Simulación:** enfatizar el volumen y la validación del pipeline.
- **ETL:** describir la transformación de datos y la carga al DW.
- **Dashboard:** mostrar resultados visuales y métricas clave.
- **Web:** presentar la URL pública y cómo se accede.
- **Conclusión:** insistir en la integración completa de IoT, datos y visualización.

### Roles sugeridos

- Integrante 1: IoT y simulación de datos.
- Integrante 2: SQL Server, ETL y DW.
- Integrante 3: Power BI y publicación web.

## 11. Preguntas probables y respuestas

- **¿Por qué usaron Somee y Render?**
  - Somee proporciona una base SQL Server accesible desde internet para la demo.
  - Render permite publicar la aplicación web con Docker de forma estable.

- **¿Por qué simular datos y no usar datos reales?**
  - Porque la maqueta es demostrativa y no reproduce aún una ciudad completa.
  - La simulación es una práctica común en Big Data para probar el pipeline antes de desplegar una solución real.

- **¿Qué aporta el modelo multidimensional?**
  - Velocidad en consultas analíticas.
  - Facilidad para crear dashboards y métricas agregadas.

- **¿Cómo se valida que el ETL funcionó?**
  - Con conteos de filas en las tablas dimension y de hecho.
  - Con análisis de la calidad de datos y la última fecha de carga.

## 12. Enlaces finales

- Aplicación web: `https://proyecto-final-24st.onrender.com/app`
- Dashboard Power BI: `https://app.powerbi.com/view?r=...`

> Nota: no incluyas credenciales de conexión en documentos públicos. Dentro del proyecto, el backend usa variables de entorno para SQL Server y Power BI.
