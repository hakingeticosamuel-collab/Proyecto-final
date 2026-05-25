import pyodbc
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory, abort
import config

app = Flask(__name__)
app.config.update(
    SECRET_KEY=config.SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

LOGIN_USER = config.LOGIN_USER
LOGIN_PASSWORD = config.LOGIN_PASSWORD
POWERBI_URL = config.POWERBI_URL


def get_connection():
    return pyodbc.connect(config.DATABASE_CONNECTION_STRING, autocommit=True)


def login_required(view):
    def wrapped_view(**kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(**kwargs)

    wrapped_view.__name__ = view.__name__
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
                    "SELECT TOP 200 UbicacionId, NombreUbicacion, Latitud, Longitud, Estado, ConsumoKwh FROM dw.DimUbicacion"
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
                        }
                    )
    except Exception:
        return jsonify({"error": "No se pudieron cargar las ubicaciones."}), 500
    return jsonify(locations)


@app.route("/api/public/metrics")
def api_public_metrics():
    metrics = {
        "total_mediciones": 0,
        "postes_activos": 0,
        "alertas_activas": 0,
        "consumo_promedio": 0,
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(1) FROM dw.FactMediciones")
                row = cursor.fetchone()
                metrics["total_mediciones"] = row[0] if row and row[0] is not None else 0

                cursor.execute("SELECT COUNT(DISTINCT PostId) FROM dw.FactMediciones")
                row = cursor.fetchone()
                metrics["postes_activos"] = row[0] if row and row[0] is not None else 0

                cursor.execute("SELECT COUNT(1) FROM dw.FactMediciones WHERE EstadoAlerta = 'Activa' OR AlertLevel IS NOT NULL")
                row = cursor.fetchone()
                metrics["alertas_activas"] = row[0] if row and row[0] is not None else 0

                cursor.execute("SELECT AVG(ConsumoKwh) FROM dw.FactMediciones")
                row = cursor.fetchone()
                metrics["consumo_promedio"] = float(row[0]) if row and row[0] is not None else 0
    except Exception:
        return jsonify({"error": "No se pudieron cargar las métricas."}), 500
    return jsonify(metrics)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == LOGIN_USER and password == LOGIN_PASSWORD:
            session["user"] = username
            return redirect(url_for("index"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


FRONTEND_DIST = Path(__file__).resolve().parent / "frontend" / "dist"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def public_app(path):
    if path.startswith("api/") or path.startswith("login") or path.startswith("logout"):
        abort(404)

    if not FRONTEND_DIST.exists():
        abort(404, description="Frontend no está construido. Ejecuta npm run build en frontend.")

    target = FRONTEND_DIST / path
    if path != "" and target.exists() and target.is_file():
        return send_from_directory(FRONTEND_DIST, path)

    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
