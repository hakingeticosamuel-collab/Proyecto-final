import pyodbc
from functools import wraps
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
import config

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=config.SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

LOGIN_USER = config.LOGIN_USER
LOGIN_PASSWORD = config.LOGIN_PASSWORD
LOGIN_REQUIRED = config.LOGIN_REQUIRED
POWERBI_URL = config.POWERBI_URL


@app.context_processor
def inject_login_settings():
    return {"LOGIN_REQUIRED": LOGIN_REQUIRED}


def get_connection():
    return pyodbc.connect(config.DATABASE_CONNECTION_STRING, autocommit=True)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if LOGIN_REQUIRED and not session.get("user"):
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


def query_single_value(cursor, query, fallback=0):
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return row[0] if len(row) > 0 else fallback
    except Exception:
        return fallback
    return fallback


def get_user(username):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT UserId, Username, PasswordHash, DisplayName, Role "
                    "FROM app_users "
                    "WHERE Username = ?",
                    username,
                )
                row = cursor.fetchone()
                if row:
                    return {
                        "user_id": row[0],
                        "username": row[1],
                        "password_hash": row[2],
                        "display_name": row[3],
                        "role": row[4],
                    }
    except Exception:
        app.logger.exception("Error querying app_users table")
    return None


def record_audit(user_id, username, action, detail=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO audit_logs (UserId, Username, ActionType, Detail) "
                    "VALUES (?, ?, ?, ?)",
                    user_id,
                    username,
                    action,
                    detail,
                )
    except Exception:
        pass


@app.route("/")
@login_required
def index():
    metrics = {
        "total_mediciones": 0,
        "postes_activos": 0,
        "alertas_activas": 0,
        "consumo_promedio": 0,
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                metrics["total_mediciones"] = query_single_value(
                    cursor,
                    "SELECT COUNT(1) FROM dw.FactMediciones",
                )
                metrics["postes_activos"] = query_single_value(
                    cursor,
                    "SELECT COUNT(DISTINCT PostId) FROM dw.FactMediciones",
                )
                metrics["alertas_activas"] = query_single_value(
                    cursor,
                    "SELECT COUNT(1) FROM dw.FactMediciones WHERE EstadoAlerta = 'Activa' OR AlertLevel IS NOT NULL",
                )
                metrics["consumo_promedio"] = query_single_value(
                    cursor,
                    "SELECT AVG(ConsumoKwh) FROM dw.FactMediciones",
                    fallback=0,
                )
    except Exception:
        app.logger.exception("Error loading index metrics")
        flash(
            "No se pudo conectar a la base de datos. Verifica la configuración de SQL Server.",
            "warning",
        )

    return render_template(
        "index.html",
        metrics=metrics,
        powerbi_url=POWERBI_URL,
    )


@app.route("/map")
@login_required
def map_view():
    return render_template("map.html")


@app.route("/api/public/locations")
def api_public_locations():
    locations = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT TOP 200 "
                    "u.UbicacionKey, u.NombreUbicacion, u.Latitud, u.Longitud, "
                    "CASE WHEN u.Activo = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado, "
                    "ISNULL(agg.PromedioConsumo, 0) AS ConsumoKwh, "
                    "agg.UltimaFecha, agg.TotalAlertas, agg.PromedioConsumo "
                    "FROM dw.DimUbicacion u "
                    "LEFT JOIN ( "
                    "    SELECT UbicacionKey, MAX(FechaCarga) AS UltimaFecha, "
                    "           SUM(CASE WHEN AlertasGeneradas = 1 THEN 1 ELSE 0 END) AS TotalAlertas, "
                    "           AVG(ConsumoKwh) AS PromedioConsumo "
                    "    FROM dw.FactMediciones "
                    "    GROUP BY UbicacionKey "
                    ") agg ON agg.UbicacionKey = u.UbicacionKey "
                    "ORDER BY u.NombreUbicacion"
                )
                for row in cursor:
                    locations.append(
                        {
                            "id": row[0],
                            "name": row[1],
                            "lat": float(row[2]) if row[2] is not None else 0,
                            "lng": float(row[3]) if row[3] is not None else 0,
                            "status": row[4] or "Desconocido",
                            "consumo": float(row[5]) if row[5] is not None else 0,
                            "last_measurement": row[6].isoformat() if row[6] else None,
                            "alert_count": int(row[7]) if row[7] is not None else 0,
                            "average_consumption": float(row[8]) if row[8] is not None else 0,
                        }
                    )
    except Exception:
        app.logger.exception("Error loading public locations")
        return jsonify({"error": "No se pudieron cargar las ubicaciones."}), 500
    return jsonify(locations)


@app.route("/api/public/report-summary")
def api_public_report_summary():
    summary = {
        "total_locations": 0,
        "locations_with_coordinates": 0,
        "measurement_count": 0,
        "alert_count": 0,
        "average_consumption": 0,
    }
    recent_measurements = []
    top_locations = []

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                summary["total_locations"] = query_single_value(cursor, "SELECT COUNT(1) FROM dw.DimUbicacion")
                summary["locations_with_coordinates"] = query_single_value(
                    cursor,
                    "SELECT COUNT(1) FROM dw.DimUbicacion WHERE Latitud IS NOT NULL AND Longitud IS NOT NULL",
                )
                summary["measurement_count"] = query_single_value(cursor, "SELECT COUNT(1) FROM dw.FactMediciones")
                summary["alert_count"] = query_single_value(
                    cursor,
                    "SELECT COUNT(1) FROM dw.FactMediciones WHERE AlertasGeneradas = 1 OR EstadoKey IN (2, 3, 4, 5)",
                )
                summary["average_consumption"] = query_single_value(
                    cursor,
                    "SELECT AVG(ConsumoKwh) FROM dw.FactMediciones",
                    fallback=0,
                )

                cursor.execute(
                    "SELECT TOP 8 "
                    "f.IdMedicionOrigen, "
                    "COALESCE(u.NombreUbicacion, CONCAT('Ubicacion ', CAST(f.UbicacionKey AS NVARCHAR(32)))) AS NombreUbicacion, "
                    "COALESCE(f.FechaCarga, CAST(t.Fecha AS datetime2)) AS FechaReferencia, "
                    "f.ConsumoKwh, "
                    "COALESCE(e.CodigoEstado, 'operativo_normal') AS EstadoActual, "
                    "f.AlertasGeneradas "
                    "FROM dw.FactMediciones f "
                    "LEFT JOIN dw.DimUbicacion u ON u.UbicacionKey = f.UbicacionKey "
                    "LEFT JOIN dw.DimTiempo t ON t.TiempoKey = f.TiempoKey "
                    "LEFT JOIN dw.DimEstado e ON e.EstadoKey = f.EstadoKey "
                    "ORDER BY f.FechaCarga DESC"
                )
                for row in cursor:
                    recent_measurements.append(
                        {
                            "post_id": row[0],
                            "location": row[1],
                            "measurement_date": row[2].isoformat() if row[2] else None,
                            "consumo": float(row[3]) if row[3] is not None else 0,
                            "alert_status": row[4] or "Sin alerta",
                            "alert_level": row[5],
                        }
                    )

                cursor.execute(
                    "SELECT TOP 5 "
                    "u.UbicacionKey, u.NombreUbicacion, "
                    "CASE WHEN u.Activo = 1 THEN 'Activo' ELSE 'Inactivo' END AS EstadoActual, "
                    "ISNULL(agg.PromedioConsumo, 0) AS ConsumoKwh, "
                    "ISNULL(agg.TotalAlertas, 0) AS TotalAlertas "
                    "FROM dw.DimUbicacion u "
                    "LEFT JOIN ( "
                    "    SELECT UbicacionKey, SUM(CASE WHEN AlertasGeneradas = 1 THEN 1 ELSE 0 END) AS TotalAlertas, AVG(ConsumoKwh) AS PromedioConsumo "
                    "    FROM dw.FactMediciones "
                    "    GROUP BY UbicacionKey "
                    ") agg ON agg.UbicacionKey = u.UbicacionKey "
                    "ORDER BY ISNULL(agg.PromedioConsumo, 0) DESC, u.NombreUbicacion"
                )
                for row in cursor:
                    top_locations.append(
                        {
                            "id": row[0],
                            "name": row[1],
                            "status": row[2] or "Desconocido",
                            "consumo": float(row[3]) if row[3] is not None else 0,
                            "alert_count": int(row[4]) if row[4] is not None else 0,
                        }
                    )
    except Exception:
        app.logger.exception("Error loading public report summary")
        return jsonify({"error": "No se pudo cargar el resumen de reportes."}), 500

    return jsonify(
        {
            "summary": summary,
            "recent_measurements": recent_measurements,
            "top_locations": top_locations,
        }
    )


@app.route("/api/public/metrics")
def api_public_metrics():
    metrics = {
        "total_mediciones": 0,
        "postes_activos": 0,
        "alertas_activas": 0,
        "consumo_promedio": 0,
    }
    period = request.args.get("period", "7d")
    if period == "24h":
        date_filter = "WHERE FechaCarga >= DATEADD(hour, -24, SYSUTCDATETIME())"
    elif period == "30d":
        date_filter = "WHERE FechaCarga >= DATEADD(day, -30, SYSUTCDATETIME())"
    else:
        date_filter = "WHERE FechaCarga >= DATEADD(day, -7, SYSUTCDATETIME())"

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(1) FROM dw.FactMediciones {date_filter}")
                row = cursor.fetchone()
                metrics["total_mediciones"] = row[0] if row and row[0] is not None else 0

                cursor.execute(f"SELECT COUNT(DISTINCT UbicacionKey) FROM dw.FactMediciones {date_filter}")
                row = cursor.fetchone()
                metrics["postes_activos"] = row[0] if row and row[0] is not None else 0

                cursor.execute(f"SELECT COUNT(1) FROM dw.FactMediciones {date_filter} AND (AlertasGeneradas = 1 OR EstadoKey IN (2, 3, 4, 5))")
                row = cursor.fetchone()
                metrics["alertas_activas"] = row[0] if row and row[0] is not None else 0

                cursor.execute(f"SELECT AVG(ConsumoKwh) FROM dw.FactMediciones {date_filter}")
                row = cursor.fetchone()
                metrics["consumo_promedio"] = float(row[0]) if row and row[0] is not None else 0
    except Exception:
        app.logger.exception("Error loading public metrics")
        return jsonify({"error": "No se pudieron cargar las métricas."}), 500
    return jsonify(metrics)


@app.route("/api/public/records")
def api_public_records():
    records = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT TOP 50 RecordId, DeviceId, MeasurementDate, Value, Status "
                    "FROM project_records ORDER BY MeasurementDate DESC"
                )
                for row in cursor:
                    records.append(
                        {
                            "id": row[0],
                            "device_id": row[1],
                            "measurement_date": row[2].isoformat() if row[2] else None,
                            "value": float(row[3]) if row[3] is not None else 0,
                            "status": row[4] or "Activo",
                        }
                    )
    except Exception:
        app.logger.exception("Error loading public records")
        return jsonify({"error": "No se pudieron cargar los registros."}), 500
    return jsonify(records)


@app.route("/api/records", methods=["POST"])
@login_required
def api_records():
    data = request.get_json() or {}
    device_id = data.get("device_id", "").strip()
    value = data.get("value")
    status = data.get("status", "Activo").strip()

    if not device_id or value is None:
        return jsonify({"error": "device_id y value son obligatorios."}), 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO project_records (DeviceId, MeasurementDate, Value, Status) "
                    "VALUES (?, GETUTCDATE(), ?, ?)",
                    device_id,
                    float(value),
                    status,
                )
        record_audit(None, session.get("user"), "record_created", f"device={device_id} value={value}")
    except Exception:
        app.logger.exception("Error saving project record")
        return jsonify({"error": "No se pudo guardar el registro."}), 500
    return jsonify({"ok": True}), 201


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = get_user(username)
        if user and check_password_hash(user["password_hash"], password):
            session["user"] = user["username"]
            record_audit(user["user_id"], user["username"], "login_success")
            return redirect(url_for("index"))

        if username == LOGIN_USER and password == LOGIN_PASSWORD:
            session["user"] = username
            record_audit(None, username, "login_success", "fallback_env_user")
            return redirect(url_for("index"))

        record_audit(None, username, "login_failed")
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/health")
def health_check():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return jsonify({"status": "ok"}), 200
    except Exception:
        app.logger.exception("Health check failed")
        return jsonify({"status": "error", "detail": "No se pudo conectar a la base de datos."}), 500


@app.route("/app", defaults={"path": ""})
@app.route("/app/<path:path>")
def vue_app(path):
    if path and (FRONTEND_DIST / path).exists():
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, "index.html")


@app.route("/assets/<path:path>")
def vue_assets(path):
    return send_from_directory(FRONTEND_DIST / "assets", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
