# Steam Game Monitor 🎮# Steam Game Monitor 🎮# Steam Game Monitor 🎮# Streaming IoT Metrics: Kafka → Spark → Dashboard (Python)



Aplikasi Python sederhana untuk memantau game Steam secara real-time dan menampilkan informasinya di dashboard web.



## Fitur UtamaSimple Python application that monitors Steam games in real-time and displays their information on a web dashboard.



✨ **Monitoring Real-time**

- Harga game dan diskon

- Jumlah pemain aktif saat ini## What you getSimple Python application that monitors Steam games in real-time and displays their information on a web dashboard.An end-to-end, native Python example that streams simulated IoT metrics into Kafka, processes them with PySpark Structured Streaming, and visualizes live aggregates on a minimal Flask dashboard.

- Rating dan review

- Informasi DLC- Steam API producer that fetches game data (prices, discounts, player counts, ratings, reviews, DLC info)

- Genre, kategori, dan tanggal rilis

- Flask dashboard with game cards and player statistics charts

📊 **Dashboard Web Interaktif**

- Kartu game dengan informasi lengkap- Game Manager interface to select which games to monitor

- Chart statistik pemain

- Badge diskon- Real-time updates every 2 minutes## What you get## What you get

- Auto-refresh setiap 30 detik

- Link langsung ke Steam Store- JSON-based data storage (no database required)



🎯 **Game Manager**- Pre-configured with 30+ popular games- Steam API producer that fetches game data (prices, discounts, player counts, ratings, reviews, DLC info)- Kafka single-broker in Docker (KRaft mode, Apache Kafka 3.8.0)

- Database 30+ game populer

- Search dan filter game

- Visual selection interface

- Save/load watchlist## Features- Flask dashboard with game cards and player statistics charts- Python Kafka producer (`kafka-python`) generating IoT telemetry



## Arsitektur- 📊 Live player statistics with charts



Sistem terdiri dari 2 komponen sederhana:- 💰 Price tracking with discount alerts- Game Manager interface to select which games to monitor- PySpark streaming job reading from Kafka and writing windowed aggregates



1. **Producer** (`src/steam_producer.py`)- ⭐ Game ratings and review summaries

   - Mengambil data dari Steam Web API

   - Menyimpan ke file JSON di `data/steam/`- 🎯 DLC information- Real-time updates every 2 minutes- Flask dashboard polling latest aggregates and rendering charts

   - Berjalan setiap 2 menit (default)

- 📝 Game details (genres, release dates, developers)

2. **Dashboard** (`src/dashboard/app.py`)

   - Flask web server di port 8080- 🔍 Search and filter games- JSON-based data storage (no database required)- Kafka UI at http://localhost:8080

   - Membaca file JSON dari producer

   - Menyajikan 2 halaman:- ✅ Easy game selection via web interface

     - `/steam` - Dashboard monitoring

     - `/games` - Game manager- Pre-configured with 30+ popular games



**Tidak ada Spark, Kafka, atau Docker!** Hanya Python murni dengan Flask dan Requests.## Prerequisites



## Prerequisites- Python 3.10+ (with `pip`)## Prereqs



- Python 3.10 atau lebih tinggi- Steam Web API key (get from https://steamcommunity.com/dev/apikey)

- Steam Web API key (opsional, untuk beberapa endpoint)

## Features- macOS with Docker Desktop running

## Instalasi

## Quick Start

### 1. Clone atau download project ini

- 📊 Live player statistics with charts- Python 3.10+ (with `pip`)

```bash

cd /path/to/spark-steam### 1. Create & activate virtualenv

```

- 💰 Price tracking with discount alerts- Java 8+ installed (required by PySpark)

### 2. Buat virtual environment

```zsh

```bash

python3 -m venv .venvpython3 -m venv .venv- ⭐ Game ratings and review summaries

source .venv/bin/activate

```source .venv/bin/activate



### 3. Install dependencies```- 🎯 DLC information## Quick start



```bash

pip install -r requirements.txt

```### 2. Install dependencies- 📝 Game details (genres, release dates, developers)



File `requirements.txt` berisi:

```

Flask==3.0.3```zsh- 🔍 Search and filter games1) Start Kafka (Docker)

requests==2.31.0

```pip install -r requirements.txt



### 4. Set Steam API key (opsional)```- ✅ Easy game selection via web interface



```bash

export STEAM_API_KEY="your_api_key_here"

```### 3. Set Steam API key```zsh



**Catatan:** Producer tetap bisa berjalan tanpa API key, tapi beberapa data mungkin terbatas.



## Cara Menjalankan```zsh## Prerequisitesdocker compose up -d



### Terminal 1: Dashboardexport STEAM_API_KEY="your_api_key_here"



```bash```- Python 3.10+ (with `pip`)# or: docker-compose up -d

python src/dashboard/app.py

```



Output:### 4. Run the dashboard (Terminal 1)- Steam Web API key (get from https://steamcommunity.com/dev/apikey)```

```

 * Running on http://127.0.0.1:8080

```

```zsh

Buka browser ke **http://127.0.0.1:8080**

python src/dashboard/app.py

### Terminal 2: Producer

```## Quick Start2) Create & activate a virtualenv and install deps

```bash

python src/steam_producer.py --watchlist config/games_watchlist.json --interval 120

```

Dashboard will be available at **http://127.0.0.1:8080**

Output:

```

🎮 Steam Game Monitor

📋 Monitoring 2 games from watchlist### 5. Run the producer (Terminal 2)### 1. Create & activate virtualenv```zsh

⏱️  Update interval: 120 seconds

💾 Saving to: /path/to/data/steam

🎮 Games: [570, 578080]

```zshpython3 -m venv .venv

Fetching data for app_id: 570

  ✅ Dota 2python src/steam_producer.py --watchlist config/games_watchlist.json --interval 120

     Price: $0.00 (discount: 0%)

     Players: 401,101``````zshsource .venv/bin/activate

...

```



## Cara Menggunakan## How to Usepython3 -m venv .venvpip install -r requirements.txt



### 1. Menambah/Hapus Game dari Watchlist



**Via Web UI (Recommended):**1. **Open Dashboard**: Go to http://127.0.0.1:8080source .venv/bin/activate```

1. Buka http://127.0.0.1:8080/games

2. Cari game yang ingin dipantau2. **Manage Games**: Click "Game Manager" to add/remove games from watchlist

3. Klik card game untuk select/deselect

4. Klik tombol "Save Watchlist"3. **Select Games**: Browse 30+ available games, click to select/deselect```

5. Restart producer untuk menerapkan perubahan

4. **Save Watchlist**: Click "Save Watchlist" button

**Via Edit Manual:**

Edit file `config/games_watchlist.json`:5. **Monitor**: Return to main dashboard to see live updates3) Run the Flask dashboard (Terminal A)

```json

{

  "description": "Steam games watchlist",

  "games": [570, 730, 252490],## How it Works### 2. Install dependencies

  "game_info": {

    "570": "Dota 2",

    "730": "Counter-Strike 2",

    "252490": "Rust"### Producer```zsh

  }

}- Fetches data from Steam Web API every 2 minutes (configurable)

```

- Retrieves game details, current player count, pricing, and discounts```zshpython -m src.dashboard.app

### 2. Melihat Dashboard

- Saves data to JSON files in `data/steam/`:

Buka http://127.0.0.1:8080 untuk melihat:

- Game cards dengan harga dan diskon  - `latest_games.json` - All game informationpip install -r requirements.txt# open http://127.0.0.1:5000

- Jumlah pemain aktif

- Rating dan recommendations  - `player_stats.json` - Player count history

- Genre dan informasi game

- Chart statistik pemain  - `discounts.json` - Current discounts``````



### 3. Database Game Tersedia



File `config/available_games.json` berisi 30+ game populer:### Dashboard



**Free to Play:** Dota 2, CS2, PUBG, TF2, Warframe, Lost Ark, dll.- Reads JSON files updated by producer



**AAA Games:** GTA V, Cyberpunk 2077, Elden Ring, Red Dead Redemption 2, Witcher 3, dll.- Displays game cards with:### 3. Set Steam API key4) Start the Spark streaming job (Terminal B)



**Survival:** Rust, ARK, The Forest, 7 Days to Die, Conan Exiles, dll.  - Current price and discount badges



**Indie:** Stardew Valley, Terraria, Hades, Dead Cells, Celeste, dll.  - Player counts



## Konfigurasi  - Ratings and review summaries



### Argumen Producer  - Quick links to Steam store```zsh```zsh



```bash- Auto-refreshes every 30 seconds

python src/steam_producer.py --help

```- Interactive charts showing player trendsexport STEAM_API_KEY="your_api_key_here"python -m src.spark_streaming



Options:

- `--watchlist PATH` - Path ke file watchlist JSON (required)

- `--interval SECONDS` - Interval update dalam detik (default: 120)### Game Manager``````



Contoh:- Lists 30+ pre-configured popular games

```bash

# Update setiap 5 menit- Search/filter by name, category, or status

python src/steam_producer.py --watchlist config/games_watchlist.json --interval 300

- Visual selection interface

# Update setiap 1 menit (hati-hati rate limit!)

python src/steam_producer.py --watchlist config/games_watchlist.json --interval 60- Saves selections to `config/games_watchlist.json`### 4. Run the dashboard (Terminal 1)The first run will download Spark Kafka connector jars; give it a minute.

```



### Environment Variables Dashboard

## Configuration

- `FLASK_HOST` - Host address (default: 127.0.0.1)

- `FLASK_PORT` - Port number (default: 8080)



Contoh:### Watchlist```zsh5) Start the IoT producer (Terminal C)

```bash

export FLASK_PORT=9000Edit `config/games_watchlist.json` or use the Game Manager UI:

python src/dashboard/app.py

``````jsonpython src/dashboard/app.py



### Environment Variables Producer{



- `STEAM_API_KEY` - Steam API key untuk endpoint yang memerlukan auth  "games": [570, 578080, 730]``````zsh



## Struktur Data}



### Output Files (data/steam/)```python -m src.producer --devices 8 --rate 4.0 --topic iot-metrics --bootstrap localhost:9092



Producer menghasilkan 3 file JSON:



**1. latest_games.json** - Data lengkap semua game### Available GamesDashboard will be available at **http://127.0.0.1:8080**```

```json

{Pre-configured in `config/available_games.json` with popular titles:

  "updated_at": 1699234567890,

  "game_count": 2,- **Free to Play**: Dota 2, PUBG, CS2, Warframe, etc.

  "games": [

    {- **AAA Games**: Cyberpunk 2077, Elden Ring, RDR2, etc.

      "app_id": 570,

      "name": "Dota 2",- **Indie Games**: Stardew Valley, Terraria, Hades, etc.### 5. Run the producer (Terminal 2)You should see the dashboard update every ~2s with average temperature and humidity per device in the latest 10s window.

      "is_free": true,

      "final_price": 0.0,- **Survival**: Rust, ARK, The Forest, etc.

      "discount_percent": 0,

      "current_players": 401101,

      "metacritic_score": 90,

      "total_recommendations": 1234567,### Environment Variables

      "dlc_count": 0,

      "genres": ["Action", "Free to Play", "Strategy"],- `STEAM_API_KEY` - Your Steam API key (required)```zsh## How it works

      "release_date": "Jul 9, 2013",

      ...- `FLASK_HOST` - Dashboard host (default: 127.0.0.1)

    }

  ]- `FLASK_PORT` - Dashboard port (default: 8080)python src/steam_producer.py --watchlist config/games_watchlist.json --interval 120- Producer publishes JSON such as:

}

```



**2. player_stats.json** - Statistik pemain### Producer Options```

```json

{```zsh

  "updated_at": 1699234567890,

  "total_games": 2,python src/steam_producer.py --help```json

  "total_players": 486238,

  "games": [```

    {

      "app_id": 570,## How to Use{

      "name": "Dota 2",

      "current_players": 401101Options:

    }

  ]- `--watchlist` - Path to watchlist JSON file  "device_id": "device-2g7xqa",

}

```- `--interval` - Update interval in seconds (default: 120)



**3. discounts.json** - Game yang sedang diskon1. **Open Dashboard**: Go to http://127.0.0.1:8080  "ts": 1730638574123,

```json

{## Data Files

  "updated_at": 1699234567890,

  "discount_count": 1,2. **Manage Games**: Click "Game Manager" to add/remove games from watchlist  "temperature": 24.7,

  "discounts": [

    {### Output Data (`data/steam/`)

      "app_id": 252490,

      "name": "Rust",- `latest_games.json` - Current game data for all monitored games3. **Select Games**: Browse 30+ available games, click to select/deselect  "humidity": 55.3,

      "discount_percent": 30,

      "initial_price": 39.99,- `player_stats.json` - Player count statistics

      "final_price": 27.99,

      "savings": 12.00- `discounts.json` - Active discounts4. **Save Watchlist**: Click "Save Watchlist" button  "battery": 82.5,

    }

  ]

}

```### Configuration (`config/`)5. **Monitor**: Return to main dashboard to see live updates  "status": "ok",



### API Endpoints Dashboard- `games_watchlist.json` - Games currently being monitored



Dashboard menyediakan REST API:- `available_games.json` - Database of available games  "location": "lab"



- `GET /` - Redirect ke /steam

- `GET /steam` - Halaman dashboard

- `GET /games` - Halaman game manager## Troubleshooting## How it Works}

- `GET /api/steam/games` - Data semua game

- `GET /api/steam/players` - Statistik pemain

- `GET /api/steam/discounts` - Game yang diskon

- `GET /api/games/available` - List game tersedia### No data on dashboard```

- `GET /api/games/watchlist` - Watchlist saat ini

- `POST /api/games/watchlist` - Update watchlist- Check producer is running and fetching data



## Troubleshooting- Verify Steam API key is set correctly### Producer



### Dashboard tidak menampilkan data- Check `data/steam/*.json` files are being updated



**Penyebab:**- Look for error messages in producer terminal- Fetches data from Steam Web API every 2 minutes (configurable)- Spark reads from Kafka, parses JSON, converts `ts` (epoch ms) to `event_time`, then computes 10s tumbling window aggregates per device (avg temperature/humidity, battery min/max, count).

- Producer belum jalan atau belum selesai fetch data

- File JSON belum dibuat



**Solusi:**### API rate limits- Retrieves game details, current player count, pricing, and discounts- Each micro-batch writes:

1. Cek producer berjalan di terminal

2. Cek file di `data/steam/` sudah ada- Steam API has rate limits

3. Tunggu beberapa saat sampai producer selesai fetch

- Default 120-second interval is safe- Saves data to JSON files in `data/steam/`:  - `data/aggregates/latest.json` (small payload the dashboard polls)

### Producer error "Failed to fetch"

- Don't set interval too low (< 60 seconds)

**Penyebab:**

- Steam API down atau rate limited  - `latest_games.json` - All game information  - historical Parquet files in `data/aggregates/parquet/`

- Network/internet issue

- Invalid app_id### Invalid game IDs



**Solusi:**- Verify game IDs (appids) from Steam store URL  - `player_stats.json` - Player count history

1. Cek koneksi internet

2. Tunggu beberapa menit (rate limit)- Example: https://store.steampowered.com/app/570/ → appid is 570

3. Verify app_id valid dari Steam Store URL

4. Lihat error detail di terminal- Not all games support all API endpoints  - `discounts.json` - Current discounts## Configs



### Rate limit Steam API



**Penyebab:**## Project Structure- Kafka topic: `iot-metrics` (auto-created)

- Terlalu sering request (interval < 60 detik)

- Terlalu banyak game di watchlist



**Solusi:**```### Dashboard- Kafka bootstrap: 

1. Naikkan interval ke 120 detik atau lebih

2. Kurangi jumlah game di watchlist├── src/

3. Tunggu beberapa menit sebelum retry

│   ├── steam_producer.py      # Data fetcher from Steam API- Reads JSON files updated by producer  - `localhost:9092` (from host machine - Python producer/consumer)

### Port 8080 sudah dipakai

│   └── dashboard/

**Penyebab:**

- Ada aplikasi lain di port 8080│       ├── app.py              # Flask web server- Displays game cards with:  - `kafka:29092` (from inside Docker - Kafka UI)



**Solusi:**│       └── templates/

```bash

# Ganti port│           ├── steam.html      # Main dashboard  - Current price and discount badges- Window: 10 seconds, watermark: 1 minute

export FLASK_PORT=9000

python src/dashboard/app.py│           └── games.html      # Game manager

```

├── config/  - Player counts

Atau kill proses di port 8080:

```bash│   ├── games_watchlist.json    # Active watchlist

lsof -ti :8080 | xargs kill -9

```│   └── available_games.json    # Game database  - Ratings and review summariesEnv overrides:



## Cara Menambah Game Baru├── data/



### 1. Cari App ID dari Steam│   └── steam/                  # Output JSON files  - Quick links to Steam store- `KAFKA_BOOTSTRAP` and `KAFKA_TOPIC` for the Spark job



Buka halaman game di Steam Store, lihat URL:└── requirements.txt            # Python dependencies

```

https://store.steampowered.com/app/570/Dota_2/```- Auto-refreshes every 30 seconds- `FLASK_HOST` and `FLASK_PORT` for the dashboard

                                    ^^^

                                App ID = 570

```

## Dependencies- Interactive charts showing player trends

### 2. Tambahkan ke available_games.json



Edit `config/available_games.json`:

```json- **Flask 3.0.3** - Web framework## Troubleshooting

{

  "app_id": 570,- **Requests 2.31.0** - HTTP library for API calls

  "name": "Dota 2",

  "category": "Free to Play",### Game Manager- Spark Kafka connector not found: ensure internet access; we set `spark.jars.packages` to `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1` matching PySpark 3.5.1

  "genre": "MOBA"

}That's it! No Spark, no Kafka, no Java required. Simple and lightweight. 🚀

```

- Lists 30+ pre-configured popular games- PySpark requires Java. On macOS, install with e.g. `brew install temurin` then re-run.

### 3. Pilih via Game Manager

- Search/filter by name, category, or status- If no data on the dashboard, check:

1. Refresh http://127.0.0.1:8080/games

2. Game baru akan muncul di list- Visual selection interface  - Producer logs (messages being sent)

3. Klik untuk select dan save

- Saves selections to `config/games_watchlist.json`  - Spark logs (streaming started, no errors)

## Struktur Project

  - File `data/aggregates/latest.json` being updated

```

spark-steam/## Configuration

├── src/

│   ├── steam_producer.py          # Producer utama## Stop

│   └── dashboard/

│       ├── app.py                  # Flask server### Watchlist```zsh

│       ├── __init__.py

│       └── templates/Edit `config/games_watchlist.json` or use the Game Manager UI:docker compose down

│           ├── steam.html          # Dashboard page

│           └── games.html          # Game manager page```json```

│

├── config/{

│   ├── games_watchlist.json        # Watchlist (user-editable)  "games": [570, 578080, 730]

│   └── available_games.json        # Database game (30+ games)}

│```

├── data/

│   └── steam/                      # Output directory### Available Games

│       ├── latest_games.json       # Game dataPre-configured in `config/available_games.json` with popular titles:

│       ├── player_stats.json       # Player stats- **Free to Play**: Dota 2, PUBG, CS2, Warframe, etc.

│       └── discounts.json          # Discount data- **AAA Games**: Cyberpunk 2077, Elden Ring, RDR2, etc.

│- **Indie Games**: Stardew Valley, Terraria, Hades, etc.

├── requirements.txt                # Python dependencies- **Survival**: Rust, ARK, The Forest, etc.

├── README.md                       # Dokumentasi ini

└── .venv/                          # Virtual environment (git ignored)### Environment Variables

```- `STEAM_API_KEY` - Your Steam API key (required)

- `FLASK_HOST` - Dashboard host (default: 127.0.0.1)

## Dependencies- `FLASK_PORT` - Dashboard port (default: 8080)



Hanya 2 package Python:### Producer Options

```zsh

- **Flask 3.0.3** - Web framework untuk dashboard dan APIpython src/steam_producer.py --help

- **Requests 2.31.0** - HTTP client untuk Steam API```



Total install size: ~50MB (sangat ringan!)Options:

- `--watchlist` - Path to watchlist JSON file

## Tips & Best Practices- `--interval` - Update interval in seconds (default: 120)



### 1. Interval Update## Data Files



- **Development:** 60-120 detik (testing)### Output Data (`data/steam/`)

- **Production:** 180-300 detik (lebih aman)- `latest_games.json` - Current game data for all monitored games

- **Heavy load:** 300+ detik (banyak game)- `player_stats.json` - Player count statistics

- `discounts.json` - Active discounts

### 2. Jumlah Game

### Configuration (`config/`)

- **Optimal:** 5-10 games- `games_watchlist.json` - Games currently being monitored

- **Maximum:** 20 games- `available_games.json` - Database of available games

- Lebih banyak game = lebih lama fetch time

## Troubleshooting

### 3. Rate Limiting

### No data on dashboard

Steam API memiliki rate limit. Jika kena limit:- Check producer is running and fetching data

- Producer akan skip game yang error- Verify Steam API key is set correctly

- Tunggu beberapa menit- Check `data/steam/*.json` files are being updated

- Interval akan otomatis dijaga (2 detik per game)- Look for error messages in producer terminal



### 4. Background Running### API rate limits

- Steam API has rate limits

Untuk run producer di background:- Default 120-second interval is safe

```bash- Don't set interval too low (< 60 seconds)

nohup python src/steam_producer.py --watchlist config/games_watchlist.json --interval 120 > producer.log 2>&1 &

```### Invalid game IDs

- Verify game IDs (appids) from Steam store URL

Stop dengan:- Example: https://store.steampowered.com/app/570/ → appid is 570

```bash- Not all games support all API endpoints

ps aux | grep steam_producer

kill <PID>## Project Structure

```

```

## Lisensi├── src/

│   ├── steam_producer.py      # Data fetcher from Steam API

Project ini untuk keperluan edukasi dan monitoring pribadi. Pastikan mematuhi [Steam Web API Terms of Use](https://steamcommunity.com/dev).│   └── dashboard/

│       ├── app.py              # Flask web server

## Troubleshooting Lanjutan│       └── templates/

│           ├── steam.html      # Main dashboard

### Memory Usage│           └── games.html      # Game manager

├── config/

Producer sangat ringan (~50MB RAM). Jika tinggi:│   ├── games_watchlist.json    # Active watchlist

- Kurangi jumlah game di watchlist│   └── available_games.json    # Game database

- Naikkan interval update├── data/

│   └── steam/                  # Output JSON files

### CPU Usage└── requirements.txt            # Python dependencies

```

Minimal, spike hanya saat fetch data. Jika tinggi:

- Cek loop tidak crash/restart terus## Dependencies

- Cek network tidak timeout terus

- **Flask 3.0.3** - Web framework

### Disk Space- **Requests 2.31.0** - HTTP library for API calls



JSON files sangat kecil (~100KB per update). Safe untuk run berhari-hari.That's it! No Spark, no Kafka, no Java required. Simple and lightweight. 🚀


## Roadmap Future

- [ ] Historical data tracking
- [ ] Email/Discord notifications untuk diskon
- [ ] Price tracking dan alert
- [ ] Export data ke CSV
- [ ] Mobile-responsive dashboard
- [ ] Multi-language support

---

**Happy Monitoring!** 🎮🚀

Jika ada pertanyaan atau issue, cek terminal logs untuk detail error.
