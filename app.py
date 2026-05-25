import os
from pathlib import Path

from flask import Flask, jsonify, redirect, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / 'frontend' / 'dist'

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('vue_app'))


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'mode': 'docker'}), 200


@app.route('/api/source-status')
def source_status():
    configured = bool(os.environ.get('SOMEE_SERVER') and os.environ.get('SOMEE_DATABASE'))
    return jsonify(
        {
            'configured': configured,
            'source': 'Somee/SQL Server',
            'mode': 'read-only' if configured else 'unconfigured',
            'powerbi_url': os.environ.get('POWER_BI_URL', 'https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9'),
        }
    ), 200


def get_somee_settings():
    user = os.environ.get('SOMEE_USER') or os.environ.get('SOMEE_USERNAME')
    return {
        'server': os.environ.get('SOMEE_SERVER') or 'iot_alumbrado_paipa.mssql.somee.com',
        'database': os.environ.get('SOMEE_DATABASE') or 'iot_alumbrado_paipa',
        'user': user,
        'password': os.environ.get('SOMEE_PASSWORD'),
    }


def somee_is_configured():
    settings = get_somee_settings()
    return all(settings.values())


def run_somee_query(sql):
    import pytds

    settings = get_somee_settings()
    if not all(settings.values()):
        raise RuntimeError('Somee connection is not configured')

    with pytds.connect(
        server=settings['server'],
        database=settings['database'],
        user=settings['user'],
        password=settings['password'],
        timeout=8,
        login_timeout=8,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description] if cursor.description else []
            rows = cursor.fetchall() if columns else []
            return [dict(zip(columns, row)) for row in rows]


def make_somee_payload(configured, mode, counts=None, latest_mediciones=None, error=None):
    payload = {
        'configured': configured,
        'source': 'Somee/SQL Server',
        'mode': mode,
        'counts': counts or {},
        'latest_mediciones': latest_mediciones or [],
    }
    if error:
        payload['error'] = error
    return payload


def fetch_somee_summary():
    mediciones = run_somee_query('SELECT COUNT(*) AS total_mediciones, MAX(fecha_hora) AS ultima_medicion FROM dbo.medicion')
    dispositivos = run_somee_query("SELECT COUNT(*) AS total_dispositivos, SUM(CASE WHEN estado = 'Activo' THEN 1 ELSE 0 END) AS dispositivos_activos FROM dbo.dispositivo_iot")
    fact_mediciones = run_somee_query('SELECT COUNT(*) AS total_fact_mediciones, MAX(FechaCarga) AS ultima_carga FROM dw.FactMediciones')
    return {
        'mediciones': mediciones[0] if mediciones else {},
        'dispositivos': dispositivos[0] if dispositivos else {},
        'fact_mediciones': fact_mediciones[0] if fact_mediciones else {},
    }


def fetch_somee_latest_measurements(limit=5):
    return run_somee_query(
        f'SELECT TOP {int(limit)} id_medicion, id_sensor, fecha_hora, valor, calidad_dato, fuente, created_at FROM dbo.medicion ORDER BY fecha_hora DESC'
    )


def fetch_somee_markers(limit=200):
    # Prefer DW locations if available, otherwise fall back to operational table
    try:
        sql = f"SELECT TOP {int(limit)} Latitud AS lat, Longitud AS lon, NombreUbicacion AS title, Direccion AS description, Activo FROM dw.DimUbicacion WHERE Latitud IS NOT NULL AND Longitud IS NOT NULL ORDER BY NombreUbicacion"
        rows = run_somee_query(sql)
        if rows:
            return [
                {"lat": float(r["lat"]), "lon": float(r["lon"]), "title": r.get("title") or "Ubicación", "description": r.get("description") or ""}
                for r in rows
                if r.get("lat") is not None and r.get("lon") is not None
            ]
    except Exception:
        # ignore and try fallback
        pass

    try:
        sql2 = f"SELECT TOP {int(limit)} Latitud AS lat, Longitud AS lon, nombre_ubicacion AS title, Direccion AS description FROM dbo.ubicacion WHERE Latitud IS NOT NULL AND Longitud IS NOT NULL ORDER BY nombre_ubicacion"
        rows2 = run_somee_query(sql2)
        return [
            {"lat": float(r["lat"]), "lon": float(r["lon"]), "title": r.get("title") or "Ubicación", "description": r.get("description") or ""}
            for r in rows2
            if r.get("lat") is not None and r.get("lon") is not None
        ]
    except Exception:
        return []


@app.route('/api/summary')
def summary():
    if not somee_is_configured():
        return jsonify(make_somee_payload(False, 'unconfigured'))

    try:
        return jsonify(make_somee_payload(True, 'read-only', counts=fetch_somee_summary()))
    except Exception as exc:
        return jsonify(make_somee_payload(False, 'error', error=str(exc)))


@app.route('/api/last-measurements')
def last_measurements():
    if not somee_is_configured():
        return jsonify(make_somee_payload(False, 'unconfigured', latest_mediciones=[]))

    limit = int(os.environ.get('LAST_MEASUREMENTS_LIMIT', 5))
    try:
        return jsonify(make_somee_payload(True, 'read-only', latest_mediciones=fetch_somee_latest_measurements(limit)))
    except Exception as exc:
        return jsonify(make_somee_payload(False, 'error', error=str(exc), latest_mediciones=[]))


@app.route('/api/dw-summary')
def dw_summary():
    if not somee_is_configured():
        return jsonify(make_somee_payload(False, 'unconfigured'))

    try:
        return jsonify(
            make_somee_payload(
                True,
                'read-only',
                counts=fetch_somee_summary(),
                latest_mediciones=fetch_somee_latest_measurements(5),
            )
        )
    except Exception as exc:
        return jsonify(make_somee_payload(False, 'error', error=str(exc)))


@app.route('/api/markers')
def markers():
    # Return an object with markers array to be consumed by the frontend map
    if not somee_is_configured():
        return jsonify({'markers': []}), 200

    try:
        data = fetch_somee_markers()
        return jsonify({'markers': data}), 200
    except Exception as exc:
        return jsonify({'markers': [], 'error': str(exc)}), 200


@app.route('/app', defaults={'path': ''})
@app.route('/app/<path:path>')
def vue_app(path):
    target = FRONTEND_DIST / path if path else FRONTEND_DIST / 'index.html'
    if path and target.exists():
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')


@app.route('/assets/<path:path>')
def vue_assets(path):
    return send_from_directory(FRONTEND_DIST / 'assets', path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
