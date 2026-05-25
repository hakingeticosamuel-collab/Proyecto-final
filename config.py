import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "cambio_secreto_123")
SQL_SERVER = os.getenv("SQL_SERVER", "iot_alumbrado_paipa.mssql.somee.com")
SQL_DATABASE = os.getenv("SQL_DATABASE", "iot_alumbrado_paipa")
SQL_USER = os.getenv("SQL_USER", "Hakingetico_SQLLogin_1")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "p4iw2erhae")
POWERBI_URL = os.getenv(
    "POWERBI_URL",
    "https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9",
)
LOGIN_USER = os.getenv("LOGIN_USER", "admin")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "Alumbrado123")

DATABASE_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "TrustServerCertificate=yes;"
)
