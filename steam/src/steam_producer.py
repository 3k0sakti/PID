"""
Steam Producer - Fetch game data from Steam API and save to JSON
No Spark/Kafka required - Simple and standalone
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "steam"


class SteamAPIClient:
    """Client for Steam Web API"""
    
    BASE_URL = "https://store.steampowered.com/api"
    STATS_URL = "https://api.steampowered.com"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SteamMonitor/1.0)'
        })
    
    def get_app_details(self, app_id: int) -> Optional[Dict[str, Any]]:
        """Fetch game details from Steam Store API"""
        url = f"{self.BASE_URL}/appdetails"
        params = {'appids': app_id, 'cc': 'us', 'l': 'english'}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if str(app_id) in data and data[str(app_id)].get('success'):
                return data[str(app_id)]['data']
            return None
        except Exception as e:
            print(f"Error fetching app {app_id}: {e}")
            return None
    
    def get_player_count(self, app_id: int) -> Optional[int]:
        """Get current player count for a game"""
        if not self.api_key:
            # Try without API key
            url = f"{self.STATS_URL}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
            params = {'appid': app_id}
        else:
            url = f"{self.STATS_URL}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
            params = {'appid': app_id, 'key': self.api_key}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('response', {}).get('result') == 1:
                return data['response'].get('player_count', 0)
            return None
        except Exception as e:
            return None


def extract_game_data(app_id: int, details: Dict[str, Any], player_count: Optional[int]) -> Dict[str, Any]:
    """Extract relevant fields from Steam API response"""
    
    # Price information
    price_overview = details.get('price_overview', {})
    initial_price = price_overview.get('initial', 0) / 100 if price_overview else 0
    final_price = price_overview.get('final', 0) / 100 if price_overview else 0
    discount_percent = price_overview.get('discount_percent', 0) if price_overview else 0
    is_free = details.get('is_free', False)
    
    # Rating and reviews
    metacritic = details.get('metacritic', {})
    metacritic_score = metacritic.get('score', None) if metacritic else None
    
    recommendations = details.get('recommendations', {})
    total_recommendations = recommendations.get('total', 0) if recommendations else 0
    
    # DLC count
    dlc_list = details.get('dlc', [])
    dlc_count = len(dlc_list) if dlc_list else 0
    
    # Genres
    genres = details.get('genres', [])
    genre_list = [g.get('description', '') for g in genres] if genres else []
    
    # Categories
    categories = details.get('categories', [])
    category_list = [c.get('description', '') for c in categories] if categories else []
    
    # Release date
    release_date = details.get('release_date', {})
    release_date_str = release_date.get('date', 'TBA') if release_date else 'TBA'
    is_coming_soon = release_date.get('coming_soon', False) if release_date else False
    
    now = datetime.now(timezone.utc)
    ts_ms = int(now.timestamp() * 1000)
    
    return {
        'app_id': app_id,
        'name': details.get('name', 'Unknown'),
        'type': details.get('type', 'game'),
        'timestamp': ts_ms,
        'event_time': now.isoformat(),
        
        # Price & Discount
        'is_free': is_free,
        'initial_price': initial_price,
        'final_price': final_price,
        'discount_percent': discount_percent,
        'on_sale': discount_percent > 0,
        'currency': price_overview.get('currency', 'USD') if price_overview else 'USD',
        
        # Rating & Reviews
        'metacritic_score': metacritic_score,
        'total_recommendations': total_recommendations,
        
        # DLC
        'dlc_count': dlc_count,
        'has_dlc': dlc_count > 0,
        
        # Genre & Categories
        'genres': genre_list,
        'categories': category_list,
        
        # Release
        'release_date': release_date_str,
        'is_coming_soon': is_coming_soon,
        
        # Players
        'current_players': player_count,
        
        # Additional info
        'short_description': details.get('short_description', '')[:200],
        'header_image': details.get('header_image', ''),
        'developers': details.get('developers', []),
        'publishers': details.get('publishers', []),
    }


def load_watchlist(filepath: str) -> List[int]:
    """Load game IDs from watchlist file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get('games', [])
    except FileNotFoundError:
        print(f"Watchlist file not found: {filepath}")
        return []
    except Exception as e:
        print(f"Error loading watchlist: {e}")
        return []


def save_data(games_data: List[Dict[str, Any]]):
    """Save data directly to JSON files"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save all games
    latest_games = {
        "updated_at": int(time.time()),
        "game_count": len(games_data),
        "games": games_data
    }
    
    with open(DATA_DIR / "latest_games.json", "w") as f:
        json.dump(latest_games, f, indent=2)
    
    # Save discounts
    discounts = [g for g in games_data if g['on_sale'] and g['discount_percent'] > 0]
    discount_data = {
        "updated_at": int(time.time()),
        "discount_count": len(discounts),
        "discounts": sorted(discounts, key=lambda x: x['discount_percent'], reverse=True)
    }
    
    with open(DATA_DIR / "discounts.json", "w") as f:
        json.dump(discount_data, f, indent=2)
    
    # Save player stats
    with_players = [g for g in games_data if g['current_players'] is not None]
    player_data = {
        "updated_at": int(time.time()),
        "total_games": len(with_players),
        "total_players": sum(g['current_players'] for g in with_players),
        "games": sorted(with_players, key=lambda x: x['current_players'], reverse=True)
    }
    
    with open(DATA_DIR / "player_stats.json", "w") as f:
        json.dump(player_data, f, indent=2)
    
    print(f"\n💾 Data saved:")
    print(f"   - {len(games_data)} games")
    print(f"   - {len(discounts)} on discount")
    print(f"   - {len(with_players)} with player stats")


def main():
    parser = argparse.ArgumentParser(description="Steam Game Data Producer")
    parser.add_argument("--watchlist", default="config/games_watchlist.json", help="Path to watchlist JSON")
    parser.add_argument("--interval", type=int, default=300, help="Fetch interval in seconds (default: 5 min)")
    parser.add_argument("--steam-api-key", help="Steam API key for player stats (optional)")
    args = parser.parse_args()
    
    # Initialize Steam API client
    steam_client = SteamAPIClient(api_key=args.steam_api_key)
    
    # Load watchlist
    app_ids = load_watchlist(args.watchlist)
    
    if not app_ids:
        print("❌ No games in watchlist. Add games to config/games_watchlist.json")
        return
    
    print(f"🎮 Steam Game Monitor")
    print(f"📋 Monitoring {len(app_ids)} games from watchlist")
    print(f"⏱️  Update interval: {args.interval} seconds")
    print(f"💾 Saving to: {DATA_DIR}")
    print(f"🎮 Games: {app_ids}\n")
    
    try:
        while True:
            games_data = []
            
            for app_id in app_ids:
                print(f"Fetching data for app_id: {app_id}")
                
                # Fetch game details
                details = steam_client.get_app_details(app_id)
                if not details:
                    print(f"  ⚠️  Failed to fetch details for {app_id}")
                    time.sleep(2)
                    continue
                
                # Fetch player count
                player_count = steam_client.get_player_count(app_id)
                
                # Extract and structure data
                game_data = extract_game_data(app_id, details, player_count)
                games_data.append(game_data)
                
                print(f"  ✅ {game_data['name']}")
                print(f"     Price: ${game_data['final_price']:.2f} (discount: {game_data['discount_percent']}%)")
                if player_count:
                    print(f"     Players: {player_count:,}")
                
                # Rate limiting
                time.sleep(2)
            
            # Save all data
            save_data(games_data)
            
            print(f"\n⏳ Waiting {args.interval} seconds before next update...\n")
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping producer...")
    finally:
        print("✅ Producer closed.")


if __name__ == "__main__":
    main()
