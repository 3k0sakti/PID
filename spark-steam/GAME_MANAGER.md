# 🎮 Game Manager - Fitur Baru

## Fitur yang Ditambahkan

### 1. **Halaman Game Manager** (`/games`)
Interface visual untuk mengelola watchlist games:
- ✅ Daftar 30+ game populer siap dipilih
- ✅ Search games by name
- ✅ Filter by category (Free to Play, AAA, Indie, Survival)
- ✅ Click to select/deselect games
- ✅ Visual indicator untuk game yang dipilih
- ✅ Counter untuk tracking berapa game yang dimonitor
- ✅ Save watchlist langsung dari browser

### 2. **Database Game Populer**
File `config/available_games.json` berisi 30+ game:

**Free to Play:**
- Dota 2, CS2, Team Fortress 2, Apex Legends, PUBG

**AAA Games:**
- GTA V, Elden Ring, Baldur's Gate 3, Cyberpunk 2077
- The Witcher 3, Red Dead Redemption 2, Sekiro
- Call of Duty, Black Myth: Wukong, Hogwarts Legacy
- Spider-Man, Starfield, Forza Horizon 5

**Indie Games:**
- Stardew Valley, Terraria, Hades, Hollow Knight, Among Us

**Survival:**
- Rust, Valheim

### 3. **API Endpoints Baru**

```
GET  /games                    # Halaman Game Manager
GET  /api/games/available      # List semua game yang tersedia
GET  /api/games/watchlist      # Get watchlist saat ini
POST /api/games/watchlist      # Update watchlist
```

### 4. **Navigasi Terintegrasi**
Semua dashboard (IoT, Steam, Game Manager) sekarang punya navigasi menu.

---

## Cara Menggunakan

### 1. Akses Game Manager
```bash
# Jalankan dashboard
python src/dashboard/app.py

# Buka di browser
http://127.0.0.1:5000/games
```

### 2. Pilih Games
1. **Search** - Ketik nama game di search box
2. **Filter** - Klik kategori (Free to Play, AAA, Indie, dll)
3. **Select** - Klik pada game card untuk select/deselect
4. **Bulk Actions**:
   - "Select All Visible" - pilih semua game yang tampil
   - "Clear Selection" - hapus semua pilihan

### 3. Save Watchlist
1. Klik tombol **"💾 Save Watchlist"**
2. Watchlist akan tersimpan di `config/games_watchlist.json`
3. **Restart Steam Producer** untuk apply perubahan:
   ```bash
   # Stop producer (Ctrl+C)
   # Start lagi
   python src/steam_producer.py --watchlist config/games_watchlist.json
   ```

---

## Fitur Detail

### Visual Indicators
- **Selected games** - Border hijau + checkmark
- **Hover effect** - Card naik saat di-hover
- **Counter** - Menampilkan "X / Y selected"
- **Changes detection** - Save button hanya aktif jika ada perubahan

### Search
- Real-time search saat mengetik
- Case-insensitive
- Mencari di nama game

### Filters
- **All** - Tampilkan semua game
- **Free to Play** - Game gratis
- **AAA** - Game triple-A besar
- **Indie** - Game indie
- **Survival** - Game survival

### Game Info
Setiap card menampilkan:
- Nama game
- App ID
- Category tag (warna biru)
- Genre tag (warna hijau)

---

## Workflow

```
1. Buka Game Manager
   ↓
2. Pilih games yang mau dimonitor
   ↓
3. Save Watchlist
   ↓
4. Restart Producer
   ↓
5. Data game otomatis di-fetch
   ↓
6. Lihat di Steam Dashboard
```

---

## Menambah Game Baru ke Database

Edit `config/available_games.json`:

```json
{
  "app_id": 123456,
  "name": "Game Baru",
  "category": "AAA",
  "genre": "Action"
}
```

**Categories yang tersedia:**
- "Free to Play"
- "AAA"
- "Indie"
- "Survival"
- "Battle Royale"

**Genres:** (bebas, contoh)
- "FPS", "RPG", "Action", "MOBA", "Simulation", "Racing", dll

---

## Screenshots Flow

### Game Manager
- Grid layout dengan cards
- Search & filter di atas
- Action bar dengan statistics
- Selected games dengan checkmark

### Setelah Save
- Notification popup "Watchlist saved!"
- Counter "Currently monitoring" terupdate
- Save button disabled sampai ada perubahan lagi

---

## Tips

### 1. Start Small
Mulai dengan 5-10 games untuk testing, baru tambah lebih banyak.

### 2. Monitor Free Games
Free games biasanya punya data player count yang lebih reliable.

### 3. Mix Categories
Pilih campuran free/paid untuk lihat variety discount patterns.

### 4. Check Regularly
Buka Game Manager untuk adjust watchlist berdasarkan kebutuhan.

---

## Troubleshooting

### "Save button tidak aktif"
- Normal jika belum ada perubahan
- Pilih/unselect game untuk aktivasi

### "Game tidak muncul di Steam Dashboard"
- Pastikan sudah save di Game Manager
- Restart Steam Producer
- Tunggu 1-2 menit untuk update pertama

### "Search tidak menemukan game"
- Check spelling
- Game mungkin belum ada di database
- Tambahkan manual di `available_games.json`

---

## File Structure

```
config/
├── available_games.json      # Database 30+ game populer
└── games_watchlist.json      # Watchlist aktif (auto-generated)

src/dashboard/
├── app.py                    # Backend API endpoints
└── templates/
    ├── games.html            # Game Manager UI
    ├── steam.html            # Steam Dashboard
    └── index.html            # IoT Dashboard
```

---

## Next Steps

Setelah setup watchlist:

1. ✅ Pilih games di Game Manager
2. ✅ Save watchlist
3. ✅ Restart producer
4. ✅ Monitor di Steam Dashboard
5. ✅ Dapat notifikasi email untuk discounts

Happy Gaming! 🎮
