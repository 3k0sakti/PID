#!/usr/bin/env python3
"""
Quick test script untuk Steam API - Test fetch data satu game
"""
import sys
import json
import requests


def test_steam_api(app_id: int = 570):
    """Test fetch game data dari Steam API"""
    print(f"🧪 Testing Steam API with App ID: {app_id}")
    print(f"   URL: https://store.steampowered.com/app/{app_id}\n")
    
    url = "https://store.steampowered.com/api/appdetails"
    params = {'appids': app_id, 'cc': 'us', 'l': 'english'}
    
    try:
        print("📡 Fetching data...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if str(app_id) not in data or not data[str(app_id)].get('success'):
            print(f"❌ Failed to get data for app {app_id}")
            print(f"   Response: {data}")
            return False
        
        game_data = data[str(app_id)]['data']
        
        print("✅ Success! Game data retrieved:\n")
        print("═" * 60)
        print(f"📦 Name: {game_data.get('name', 'Unknown')}")
        print(f"🎮 Type: {game_data.get('type', 'N/A')}")
        print()
        
        # Price info
        if game_data.get('is_free'):
            print("💰 Price: FREE TO PLAY")
        else:
            price = game_data.get('price_overview', {})
            if price:
                initial = price.get('initial', 0) / 100
                final = price.get('final', 0) / 100
                discount = price.get('discount_percent', 0)
                currency = price.get('currency', 'USD')
                
                print(f"💰 Price:")
                if discount > 0:
                    print(f"   Original: ${initial:.2f}")
                    print(f"   Current:  ${final:.2f}")
                    print(f"   Discount: {discount}% OFF 🔥")
                else:
                    print(f"   ${final:.2f}")
                print(f"   Currency: {currency}")
            else:
                print("💰 Price: N/A")
        print()
        
        # Rating
        metacritic = game_data.get('metacritic', {})
        if metacritic:
            print(f"⭐ Metacritic Score: {metacritic.get('score', 'N/A')}")
        
        recommendations = game_data.get('recommendations', {})
        if recommendations:
            total = recommendations.get('total', 0)
            print(f"👍 Recommendations: {total:,}")
        print()
        
        # DLC
        dlc = game_data.get('dlc', [])
        if dlc:
            print(f"🎁 DLC Count: {len(dlc)}")
            print()
        
        # Genres
        genres = game_data.get('genres', [])
        if genres:
            genre_names = [g.get('description', '') for g in genres]
            print(f"🏷️  Genres: {', '.join(genre_names)}")
        
        categories = game_data.get('categories', [])
        if categories:
            cat_names = [c.get('description', '') for c in categories[:5]]
            print(f"📋 Categories: {', '.join(cat_names)}")
        print()
        
        # Release date
        release = game_data.get('release_date', {})
        if release:
            date = release.get('date', 'TBA')
            coming_soon = release.get('coming_soon', False)
            status = "(Coming Soon)" if coming_soon else ""
            print(f"📅 Release Date: {date} {status}")
        print()
        
        # Developers & Publishers
        devs = game_data.get('developers', [])
        if devs:
            print(f"👨‍💻 Developers: {', '.join(devs)}")
        
        pubs = game_data.get('publishers', [])
        if pubs:
            print(f"🏢 Publishers: {', '.join(pubs)}")
        print()
        
        # Description
        desc = game_data.get('short_description', '')
        if desc:
            print(f"📝 Description:")
            print(f"   {desc[:200]}{'...' if len(desc) > 200 else ''}")
        
        print("═" * 60)
        print()
        print("✅ Test passed! Steam API is working correctly.")
        print()
        
        # Test player count (requires API key)
        print("📊 Testing player count API (optional)...")
        player_url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
        player_params = {'appid': app_id}
        
        try:
            player_response = requests.get(player_url, params=player_params, timeout=5)
            player_data = player_response.json()
            
            if player_data.get('response', {}).get('result') == 1:
                count = player_data['response'].get('player_count', 0)
                print(f"   ✅ Current players: {count:,}")
            else:
                print(f"   ⚠️  Player count not available for this game")
        except Exception as e:
            print(f"   ⚠️  Could not fetch player count: {e}")
        
        print()
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Steam API might be slow")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main function"""
    print()
    print("🎮 Steam API Test Script")
    print()
    
    # Default to Dota 2 (570)
    app_id = 570
    
    if len(sys.argv) > 1:
        try:
            app_id = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid App ID: {sys.argv[1]}")
            print("   Usage: python test_steam_api.py [APP_ID]")
            sys.exit(1)
    
    success = test_steam_api(app_id)
    
    if success:
        print("💡 Tip: You can test other games by providing App ID:")
        print(f"   python test_steam_api.py 730    # Counter-Strike 2")
        print(f"   python test_steam_api.py 1245620  # Elden Ring")
        print()
        print("📝 Find App IDs from Steam URLs:")
        print("   https://store.steampowered.com/app/APP_ID/Game_Name")
        print()
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
