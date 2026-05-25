# Deploy en Render

Este repositorio está preparado para desplegarse en Render usando un servicio Docker.

## Arquitectura de despliegue

- `Dockerfile`: construye el frontend Vue/Tailwind y el backend Flask en una imagen única.
- `render.yaml`: define el servicio web de Render y el Dockerfile a usar.
- `app.py`: sirve la API pública y el frontend estático generado en `frontend/dist`.

## Pasos para configurar en Render

1. Crea una cuenta en [Render](https://render.com) si no la tienes.
2. Conecta tu cuenta de Render con GitHub.
3. En Render, crea un nuevo servicio de tipo `Web Service`.
4. Selecciona el repositorio `hakingeticosamuel-collab/Proyecto-final`.
5. Usa la rama `main`.
6. Como entorno selecciona `Docker`.
7. Render detectará automáticamente `render.yaml`, así que no necesitas definir el comando de build manualmente.
8. En el panel de `Environment` agrega estas variables de entorno:

   - `SECRET_KEY` = `un_secreto_largo_y_seguro`
   - `SQL_SERVER` = `iot_alumbrado_paipa.mssql.somee.com`
   - `SQL_DATABASE` = `iot_alumbrado_paipa`
   - `SQL_USER` = `Hakingetico_SQLLogin_1`
   - `SQL_PASSWORD` = `p4iw2erhae`
   - `POWERBI_URL` = `https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9`
   - `LOGIN_USER` = `admin`
   - `LOGIN_PASSWORD` = `Alumbrado123`

9. Guarda y lanza el deploy.

## Qué hace la imagen Docker

- Construye el frontend en `frontend/dist`.
- Instala el driver ODBC de SQL Server requerido para `pyodbc`.
- Instala las dependencias Python del backend.
- Copia el código del proyecto.
- Ejecuta `gunicorn app:app --bind 0.0.0.0:5000 --workers 4 --threads 2`.

## Alternativa: Render sin Docker

Si prefieres crear el servicio como `Python 3` en Render en lugar de usar Docker:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --threads 2`

También puedes usar este `Procfile` en la raíz del repositorio:

```text
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --threads 2
```

En ambos casos, agrega las variables de entorno necesarias y no subas tu archivo `.env`.

## Pruebas locales antes del deploy

En tu máquina local puedes validar la construcción antes de push:

```bash
cd "d:\UNIVERSIDAD\Proyecto final\frontend"
npm install
npm run build
cd ..
python -m pip install -r requirements.txt
python app.py
```

Luego abre `http://127.0.0.1:5000`.

## Nota de rutas

- El backend sirve la UI en la misma aplicación.
- Si `frontend/dist` está disponible, la ruta raíz (`/`) carga el portal construido.
- La API pública está disponible en:
  - `/api/public/metrics`
  - `/api/public/locations`

## Recomendaciones

- No subas `.env` a GitHub.
- Usa variables de entorno en Render para el acceso a la base de datos y el reporte Power BI.
- Si Render usa un plan gratuito, tarda unos minutos en construir la imagen Docker.
