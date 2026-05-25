# Paipa Smart Light — UI & Local Run

This document explains how to run the frontend and backend locally and which environment variables are required to show the live Power BI embed and Somee connection.

Requirements
- Node 18+ and npm
- Python 3.11+ (venv recommended)

Frontend
1. Install dependencies and build:

```bash
cd frontend
npm install
npm run build
```

Backend
1. Create and activate a venv, then install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Environment variables (set these to enable Somee read-only and Power BI):

- `SOMEE_SERVER` (default: iot_alumbrado_paipa.mssql.somee.com)
- `SOMEE_DATABASE` (default: iot_alumbrado_paipa)
- `SOMEE_USER` or `SOMEE_USERNAME`
- `SOMEE_PASSWORD`
- `POWER_BI_URL` (public Power BI report URL)

Run backend:

```powershell
.\.venv\Scripts\python.exe app.py
```

Notes
- The app exposes `/api/summary` and `/api/last-measurements` for the frontend.
- If Somee is not configured, the UI shows a clean fallback state without exposing errors.
