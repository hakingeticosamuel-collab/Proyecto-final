# Informe Final - Entrega 3

## 1. Portada
**Proyecto:** Sistema Inteligente de Alumbrado Público - Paipa, Boyacá  
**Entrega:** 3 - Publicación Web + Prototipo + Sustentación Final  
**Integrantes:** [Nombre(s) del equipo]  
**Programa:** [Programa académico]  
**Fecha:** [Fecha de entrega]

## 2. Introducción General
Este proyecto integra un prototipo IoT, una base de datos en SQL Server, un proceso ETL, un Data Warehouse, visualización en Power BI y una publicación web en Flask. La solución fue diseñada para representar una ciudad inteligente aplicada al alumbrado público, permitiendo capturar datos, transformarlos, analizarlos y exponerlos en una interfaz web accesible para demostración y sustentación.

La entrega 3 reúne toda la cadena funcional del proyecto: captura de datos desde el prototipo, almacenamiento operacional en Somee/SQL Server, procesamiento analítico en el DW, visualización en Power BI y despliegue público en Render mediante Docker.

## 3. Arquitectura Final del Ecosistema
La arquitectura final del ecosistema se resume así:

IoT → SQL Server → ETL → DW → Power BI → Flask

### Flujo general
- El prototipo IoT simula la captura de variables del entorno y del alumbrado.
- Los datos se almacenan inicialmente en SQL Server, incluyendo la base pública alojada en Somee cuando aplica para pruebas y consulta.
- El proceso ETL limpia, transforma y consolida la información.
- El Data Warehouse organiza los datos para el análisis.
- Power BI consume el DW para construir visualizaciones, indicadores y reportes.
- Flask publica el portal web y sirve como capa de presentación para la experiencia final.

### Consideraciones de integración
- La conexión a SQL Server debe conservar la configuración definida para Somee y los objetos del esquema operativo y analítico.
- El reporte de Power BI debe estar vinculado al conjunto de datos correcto y a la cuenta publicada.
- El portal web actúa como la cara pública del ecosistema y como punto de acceso para la sustentación.

## 4. Prototipo IoT

### 4.1 Descripción del prototipo
El prototipo corresponde a una maqueta de ciudad inteligente con calles, zonas urbanas y postes de alumbrado. Su función es representar un entorno realista donde se observa cómo el sistema responde a cambios de luz, presencia y consumo eléctrico.

### 4.2 Dispositivos utilizados
- **ESP32:** microcontrolador principal encargado de leer sensores y coordinar el envío de datos.
- **Sensores de luminosidad:** para medir variaciones de iluminación ambiental.
- **Sensores de presencia o movimiento:** para detectar actividad en la zona.
- **Sensores de corriente:** para estimar consumo eléctrico en el sistema de alumbrado.
- **Sensores de temperatura:** para complementar el monitoreo del entorno.

### 4.3 Funcionamiento
- El ESP32 captura las lecturas de los sensores de forma periódica.
- El sistema simula el comportamiento del alumbrado en una ciudad, encendiendo o reaccionando según el contexto.
- Las lecturas permiten observar escenarios de día, noche y presencia de usuarios.
- Los datos se envían al entorno de almacenamiento para su posterior consulta y análisis.

### 4.4 Evidencias
- Fotografía de la maqueta completa.
- Fotografía de los postes y componentes electrónicos.
- Fotografía de sensores y cableado.
- Captura del prototipo encendido y en funcionamiento.

## 5. Publicación Web

### 5.1 Arquitectura Flask
La publicación web fue organizada con Flask como backend ligero y como servidor del frontend construido para producción.

- **Backend:** Flask expone las rutas mínimas necesarias para salud, navegación y entrega de la aplicación.
- **Frontend:** Vue 3 renderiza la interfaz de usuario y organiza la navegación del sitio.
- **Integración:** el proyecto se despliega en Docker y se publica en Render como un servicio web estable.

La versión final prioriza estabilidad y despliegue reproducible. En la etapa de validación se redujo la dependencia de servicios externos durante el arranque para evitar fallos por conexión y asegurar que la publicación web responda correctamente.

### 5.2 Integración Power BI
Power BI forma parte central de la presentación analítica del proyecto. El dashboard debe mostrarse embebido o enlazado desde la publicación web, según la configuración elegida para la entrega.

### Configuración a considerar
- Publicación del reporte en Power BI Service.
- Uso del enlace de inserción o iframe cuando la política de publicación lo permita.
- Verificación del conjunto de datos conectado al DW.
- Actualización de credenciales y permisos del espacio de trabajo.

### Información a documentar en el informe final
- Nombre del reporte.
- URL pública o enlace de inserción.
- Página principal del dashboard.
- Métricas visibles: consumo, alertas, zonas, tendencias y estado del alumbrado.

### 5.3 Leaflet.js
Leaflet.js se usa para el mapa interactivo del proyecto cuando se presenta la parte geográfica del sistema.

- Los marcadores representan ubicaciones o postes.
- Cada punto puede mostrar información de estado, consumo o alertas.
- El mapa permite navegación visual por sectores.

### 5.4 Evidencias
- Captura del sitio publicado funcionando.
- Captura del mapa interactivo.
- Captura del dashboard o sección analítica integrada.
- Captura de la versión desplegada en Render.

## 6. Dashboard Publicado
- **URL pública:** [Colocar URL de Render o del sitio publicado].
- **Navegación:** acceso a la vista principal, arquitectura y estado general del proyecto.
- **Filtros:** si el dashboard los incluye, documentar rango de fechas, zonas, dispositivos o estados.
- **Relación con la base de datos:** indicar que el tablero consume la información preparada desde SQL Server y el DW.

## 7. Sustentación

### 7.1 Organización del video
- **Duración sugerida:** 10 a 15 minutos.
- **Estructura sugerida:** presentación del problema, prototipo IoT, base de datos y ETL, Power BI, publicación web, conclusiones.

### 7.2 Participación individual
- **Integrante 1:** explicación del prototipo IoT y la maqueta.
- **Integrante 2:** explicación de SQL Server, ETL y DW.
- **Integrante 3:** explicación de Power BI y publicación web en Flask.

### 7.3 Evidencias
- **YouTube:** [Insertar enlace del video].
- **Capturas:** incluir pantallas del video, presentación y sustentación.

## 8. Demostración Técnica
La demostración técnica debe mostrar, en orden, el funcionamiento real de la solución:

- SQL Server con la base operacional o pública utilizada para pruebas.
- Proceso ETL ejecutado y carga al Data Warehouse.
- Power BI con el dashboard conectado al modelo analítico.
- Flask publicado en Render y accesible por URL.
- Maqueta IoT y sensores funcionando como evidencia física del prototipo.

## 9. Resultados Finales
- El proyecto logró integrar la adquisición de datos, su procesamiento y la visualización final.
- La solución permite explicar el ciclo completo de una ciudad inteligente aplicada al alumbrado.
- La publicación web facilita la demostración pública y la sustentación técnica.
- El modelo analítico en Power BI aporta una lectura comprensible del comportamiento del sistema.

## 10. Conclusiones Generales
La entrega final demuestra la integración de IoT, Big Data y visualización en una propuesta de ciudad inteligente. El proyecto conecta el prototipo físico con SQL Server, ETL, Data Warehouse, Power BI y Flask, logrando una solución coherente de principio a fin.

La principal utilidad del sistema es convertir datos operacionales en información visual y útil para la toma de decisiones. Además, el uso de publicación web y de una base de datos pública como Somee facilita la demostración y el acceso al proyecto desde un entorno real de despliegue.
