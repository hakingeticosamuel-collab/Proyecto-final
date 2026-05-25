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


@app.route('/api/dw-summary')
def dw_summary():
    if not somee_is_configured():
        return jsonify(
            {
                'configured': False,
                'source': 'Somee/SQL Server',
                'mode': 'unconfigured',
                'counts': {},
                'latest_mediciones': [],
            }
        ), 200

    try:
        mediciones = run_somee_query('SELECT COUNT(*) AS total_mediciones, MAX(fecha_hora) AS ultima_medicion FROM dbo.medicion')
        dispositivos = run_somee_query("SELECT COUNT(*) AS total_dispositivos, SUM(CASE WHEN estado = 'Activo' THEN 1 ELSE 0 END) AS dispositivos_activos FROM dbo.dispositivo_iot")
        fact_mediciones = run_somee_query('SELECT COUNT(*) AS total_fact_mediciones, MAX(FechaCarga) AS ultima_carga FROM dw.FactMediciones')
        latest_mediciones = run_somee_query(
            'SELECT TOP 5 id_medicion, id_sensor, fecha_hora, valor, calidad_dato, fuente, created_at FROM dbo.medicion ORDER BY fecha_hora DESC'
        )

        return jsonify(
            {
                'configured': True,
                'source': 'Somee/SQL Server',
                'mode': 'read-only',
                'counts': {
                    'mediciones': mediciones[0] if mediciones else {},
                    'dispositivos': dispositivos[0] if dispositivos else {},
                    'fact_mediciones': fact_mediciones[0] if fact_mediciones else {},
                },
                'latest_mediciones': latest_mediciones,
            }
        ), 200
    except Exception as exc:
        return jsonify(
            {
                'configured': False,
                'source': 'Somee/SQL Server',
                'mode': 'error',
                'error': str(exc),
                'counts': {},
                'latest_mediciones': [],
            }
        ), 200


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
