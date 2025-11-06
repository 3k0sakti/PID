from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, render_template, redirect
import requests

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

    @app.delete("/api/games/watchlist/<int:app_id>")
    def remove_from_watchlist(app_id: int):
        """Remove a single game from the watchlist by app_id"""
        try:
            # Load current watchlist (create empty structure if missing)
            if WATCHLIST_FILE.exists():
                with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {"description": "Steam games watchlist", "games": [], "game_info": {}}

            games = set(data.get("games", []))
            info = data.get("game_info", {})

            if app_id not in games:
                return jsonify({"success": False, "error": "Game not in watchlist"}), 404

            # Remove
            games.discard(app_id)
            if str(app_id) in info:
                info.pop(str(app_id), None)
            if app_id in info:
                info.pop(app_id, None)

            # Persist
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "description": data.get("description", "Steam games watchlist"),
                    "games": sorted(list(games)),
                    "game_info": info,
                }, f, indent=2)

            return jsonify({"success": True, "message": f"Removed {app_id} from watchlist"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.get("/api/steam/search")
    def steam_search():
        """Search Steam store for apps by name (server-side helper for UI)"""
        from flask import request
        q = request.args.get("q", "").strip()
        limit = int(request.args.get("limit", "50"))
        if not q or len(q) < 2:
            return jsonify({"success": True, "count": 0, "results": []})
        try:
            url = "https://store.steampowered.com/api/storesearch"
            params = {"term": q, "cc": "us", "l": "english"}
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
            items = data.get("items", [])
            results = []
            for it in items[:limit]:
                # Normalize fields we use in Game Manager
                app_id = it.get("id") or it.get("appid")
                name = it.get("name")
                if not app_id or not name:
                    continue
                results.append({
                    "app_id": app_id,
                    "name": name,
                    "category": "Steam",
                    "genre": (it.get("type") or "Game"),
                })
            return jsonify({"success": True, "count": len(results), "results": results})
        except Exception as e:
            return jsonify({"success": False, "error": str(e), "results": []}), 500

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
