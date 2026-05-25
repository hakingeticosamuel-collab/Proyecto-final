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
