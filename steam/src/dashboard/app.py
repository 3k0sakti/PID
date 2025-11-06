from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, render_template, redirect

ROOT = Path(__file__).resolve().parent

# Steam data files
STEAM_DATA_DIR = ROOT.parent.parent / "data" / "steam"
STEAM_GAMES_FILE = STEAM_DATA_DIR / "latest_games.json"
STEAM_PLAYERS_FILE = STEAM_DATA_DIR / "player_stats.json"
STEAM_DISCOUNTS_FILE = STEAM_DATA_DIR / "discounts.json"

# Config files
CONFIG_DIR = ROOT.parent.parent / "config"
WATCHLIST_FILE = CONFIG_DIR / "games_watchlist.json"
AVAILABLE_GAMES_FILE = CONFIG_DIR / "available_games.json"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(ROOT / "templates"),
        static_folder=str(ROOT / "static"),
    )

    @app.get("/")
    def index():
        """Redirect to Steam dashboard"""
        return redirect("/steam")
    
    @app.get("/steam")
    def steam_dashboard():
        """Steam games dashboard page"""
        return render_template("steam.html")
    
    @app.get("/api/steam/games")
    def steam_games():
        """Get latest Steam game data"""
        if STEAM_GAMES_FILE.exists():
            try:
                with open(STEAM_GAMES_FILE, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
            except Exception as e:
                data = {"updated_at": 0, "game_count": 0, "games": [], "error": str(e)}
        else:
            data = {"updated_at": 0, "game_count": 0, "games": []}
        return jsonify(data)
    
    @app.get("/api/steam/players")
    def steam_players():
        """Get player statistics"""
        if STEAM_PLAYERS_FILE.exists():
            try:
                with open(STEAM_PLAYERS_FILE, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
            except Exception as e:
                data = {"updated_at": 0, "total_games": 0, "total_players": 0, "games": [], "error": str(e)}
        else:
            data = {"updated_at": 0, "total_games": 0, "total_players": 0, "games": []}
        return jsonify(data)
    
    @app.get("/api/steam/discounts")
    def steam_discounts():
        """Get current discounts"""
        if STEAM_DISCOUNTS_FILE.exists():
            try:
                with open(STEAM_DISCOUNTS_FILE, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
            except Exception as e:
                data = {"updated_at": 0, "discount_count": 0, "discounts": [], "error": str(e)}
        else:
            data = {"updated_at": 0, "discount_count": 0, "discounts": []}
        return jsonify(data)
    
    @app.get("/games")
    def games_manager():
        """Games manager page"""
        return render_template("games.html")
    
    @app.get("/api/games/available")
    def available_games():
        """Get list of available games"""
        if AVAILABLE_GAMES_FILE.exists():
            try:
                with open(AVAILABLE_GAMES_FILE, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
            except Exception as e:
                data = {"games": [], "error": str(e)}
        else:
            data = {"games": []}
        return jsonify(data)
    
    @app.get("/api/games/watchlist")
    def get_watchlist():
        """Get current watchlist"""
        if WATCHLIST_FILE.exists():
            try:
                with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                    data: Dict[str, Any] = json.load(f)
            except Exception as e:
                data = {"games": [], "error": str(e)}
        else:
            data = {"games": []}
        return jsonify(data)
    
    @app.post("/api/games/watchlist")
    def update_watchlist():
        """Update watchlist"""
        from flask import request
        try:
            new_watchlist = request.get_json()
            if not new_watchlist or "games" not in new_watchlist:
                return jsonify({"success": False, "error": "Invalid data"}), 400
            
            # Ensure config directory exists
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Save watchlist
            with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
                json.dump(new_watchlist, f, indent=2)
            
            return jsonify({"success": True, "message": "Watchlist updated"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return app


if __name__ == "main__":  # pragma: no cover
    # Incorrect guard intentionally avoided; use module run instead.
    pass


if __name__ == "__main__":
    # Allow host/port override via env vars
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "8080"))
    app = create_app()
    app.run(host=host, port=port, debug=True)
