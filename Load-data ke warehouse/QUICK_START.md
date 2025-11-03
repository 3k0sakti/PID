# Quick Start Guide

## Instalasi Dependencies

```bash
pip install -r requirements.txt
```

## Menjalankan Tutorial

1. **Buka VS Code** di folder project ini
2. **Buka Jupyter Notebook**: `hands_on_data_warehouse.ipynb`
3. **Jalankan cell** secara berurutan (Shift + Enter)

## Struktur Project

```
├── README.md                          # Dokumentasi utama
├── QUICK_START.md                     # Panduan ini
├── requirements.txt                   # Dependencies
├── hands_on_data_warehouse.ipynb     # Tutorial utama
├── src/                               # Source code
│   ├── config.py                      # Konfigurasi
│   ├── data_loader.py                 # ETL pipeline
│   └── warehouse_manager.py           # Database operations
├── sql/                               # SQL scripts
│   ├── create_tables.sql              # DDL
│   └── sample_queries.sql             # Analytics queries
├── data/                              # Data source
│   └── processed_sensor_data_*.csv    # Raw data
└── warehouse/                         # Database
    └── sensor_warehouse.db            # SQLite DB (auto-created)
```

## Troubleshooting

### Error: Module tidak ditemukan
```bash
pip install pandas sqlalchemy matplotlib seaborn plotly
```

### Error: Database terkunci
Restart Jupyter kernel dan jalankan ulang.

### Error: File CSV tidak ditemukan
Pastikan file CSV ada di folder `data/`.

## Tips

- 💡 Jalankan cell secara berurutan
- 🔄 Restart kernel jika ada error
- 📊 Perhatikan visualisasi untuk insights
- ⏱️ Monitor performance metrics

Happy learning! 🚀