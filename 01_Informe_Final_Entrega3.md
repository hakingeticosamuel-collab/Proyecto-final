# Informe Final - Entrega 3: Integración TOTAL

## 1. Portada
**Proyecto:** Sistema Inteligente de Alumbrado Público - Paipa, Boyacá  
**Entrega:** 3 (Publicación Web + Prototipo + Sustentación Final)  
**Integrantes:** [Tu Nombre / Grupo]  
**Fecha:** [Fecha actual]

## 2. Introducción General
Este informe describe la integración total del proyecto: desde el prototipo IoT y la captura de datos, hasta el proceso ETL, el Data Warehouse, el dashboard de Power BI y la publicación del portal web en Flask. La solución busca convertir el alumbrado público en un servicio inteligente y gestionable mediante datos reales y visualizaciones interactivas.

## 3. Arquitectura Final del Ecosistema
El ecosistema completo se estructura como sigue:

IoT → SQL Server → ETL → DW → Power BI → Flask

El flujo de datos es:
- Sensores IoT miden luminosidad, temperatura, corriente y presencia.
- Las lecturas primarias llegan a SQL Server en un esquema operacional (`dbo`).
- Se ejecuta el proceso ETL para transformar y cargar los datos en el Data Warehouse (`dw`).
- Power BI consume el DW para visualizar métricas, mapas y tendencias.
- Flask publica la interfaz web y embebe el dashboard para acceso público.

## 4. Prototipo IoT

### 4.1 Descripción del prototipo
El prototipo es una maqueta de ciudad inteligente que representa sectores de Paipa con postes de alumbrado público. Incluye una maqueta urbana escalada y postes distribuidos en una pequeña “ciudad” con vías, zonas peatonales y áreas de parque.

### 4.2 Dispositivos utilizados
- **ESP32:** microcontrolador con conectividad WiFi.
- **BH1750:** sensor de luminosidad.
- **PIR:** sensor de movimiento.
- **SCT-013:** sensor de corriente para medir consumo eléctrico.
- **DS18B20:** sensor de temperatura.

### 4.3 Funcionamiento
- El ESP32 lee los sensores y genera datos periódicos.
- La maqueta simula condiciones de la ciudad: día/noche y presencia de personas.
- Cuando baja la luminosidad y se detecta movimiento, el sistema activa la iluminación inteligente.
- Los datos se envían a la base de datos para su procesamiento.

### 4.4 Evidencias
- Fotos de la maqueta completa.
- Fotos de los postes con sensores instalados.
- Fotos de las conexiones del ESP32 y de los cables de alimentación.

## 5. Publicación Web

### 5.1 Arquitectura Flask
La aplicación Flask actúa como backend y frontend ligero:
- **Backend:** `Flask` sirve APIs internas y consultas a la base de datos.
- **Frontend:** plantillas Jinja2 renderizan la interfaz y el mapa Leaflet.
- **Integración:** Flask recibe los datos de SQL Server, prepara JSON para el frontend y embebe Power BI en una vista principal.

La app está construida con:
- `pyodbc` para conexión a SQL Server.
- `Flask-Login` o sesión básica para autenticación mínima.
- `Bootstrap` para diseño responsivo.

### 5.2 Integración Power BI
El dashboard de Power BI se integra en el sitio mediante un iframe embebido. Esto permite mostrar:
- KPI de consumo y alertas.
- Tendencias temporales.
- Comparaciones por zona y dispositivo.

La publicación puede ser mediante Power BI Service o un reporte exportado como contenido web. El dashboard se refresca según el ciclo de actualización configurado.

### 5.3 Leaflet.js
Se utiliza `Leaflet.js` para mostrar un mapa interactivo de los postes:
- Los marcadores se cargan desde la tabla `dw.DimUbicacion`.
- Cada marcador muestra estado, consumo y alertas del poste.
- El mapa permite hacer zoom y seleccionar sectores para ver detalles.

### 5.4 Evidencias
- Captura del portal web con el dashboard embebido.
- Captura del mapa interactivo con marcadores activos.
- Captura de la página de login y de las métricas principales.

## 6. Dashboard Publicado
- **URL pública:** [Insertar URL pública o local].
- **Navegación:** menú con acceso a la vista general, mapa y reportes.
- **Filtros:** fecha, zona, tipo de sensor y estado de alertas.
- **Experiencia:** el usuario accede a métricas en tiempo real y puede explorar datos geográficos.

## 7. Sustentación

### 7.1 Organización del video
- **Duración:** 10-15 minutos.
- **Estructura:** 1) presentación del problema, 2) demo de la maqueta, 3) explicación de SQL/ETL, 4) visualización Power BI, 5) portal Flask, 6) conclusiones.

### 7.2 Participación individual
- **Integrante A:** explicación del prototipo IoT y la maqueta.
- **Integrante B:** descripción de SQL Server, ETL y el Data Warehouse.
- **Integrante C:** demostración de Power BI y la publicación en Flask.

### 7.3 Evidencias
- **YouTube:** [Insertar enlace del video].
- **Capturas:** imágenes del video, pantallazos de navegación y slides de sustentación.

## 8. Demostración Técnica
En la demostración se muestra:
- Ejecución del proceso ETL en SQL Server.
- Carga y transformación de datos hacia el DW.
- Actualización de visuales en Power BI.
- Navegación del portal Flask y el mapa Leaflet.
- Funcionamiento de la maqueta IoT.

## 9. Resultados Finales
- **Beneficios:** gestión inteligente del alumbrado, mayor eficiencia energética, monitoreo centralizado y mejor respuesta ante alertas.
- **Análisis:** se identifican zonas de mayor consumo y patrones de actividad por hora.
- **Funcionamiento:** el sistema opera como un ciclo completo de captura, transformación, análisis y publicación.

## 10. Conclusiones Generales
El proyecto integra IoT, Big Data y visualización para construir una solución real de ciudad inteligente. La propuesta demuestra que los datos pueden convertir el alumbrado público en un servicio más eficiente y seguro. La arquitectura final es escalable y permite futuras ampliaciones, como predicción de fallas o gestión multiciudad.
