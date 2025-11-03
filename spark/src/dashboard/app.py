from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, render_template

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT.parent.parent / "data" / "aggregates" / "latest.json"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(ROOT / "templates"),
        static_folder=str(ROOT / "static"),
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/metrics")
    def metrics():
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
            except Exception as e:  # pragma: no cover - safeguard
                data = {"updated_at": 0, "records": [], "error": str(e)}
        else:
            data = {"updated_at": 0, "records": []}
        return jsonify(data)

    return app


if __name__ == "main__":  # pragma: no cover
    # Incorrect guard intentionally avoided; use module run instead.
    pass


if __name__ == "__main__":
    # Allow host/port override via env vars
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    app = create_app()
    app.run(host=host, port=port, debug=True)
