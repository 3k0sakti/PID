#!/bin/zsh
# Quick Start Script for IoT Streaming Pipeline
# Run: chmod +x start.sh && ./start.sh

set -e

echo "🚀 IoT Streaming Pipeline - Quick Start"
echo "========================================"

# Check Docker
echo "\n1. Checking Docker..."
if ! docker ps >/dev/null 2>&1; then
    echo "❌ Docker not running. Please start Docker Desktop."
    exit 1
fi
echo "✅ Docker is running"

# Start Kafka
echo "\n2. Starting Kafka..."
docker compose up -d
sleep 5
echo "✅ Kafka started (localhost:9092)"
echo "✅ Kafka UI available at http://localhost:8080"

# Check Python
echo "\n3. Checking Python..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 not found. Please install Python 3.10+."
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Java (needed for PySpark)
echo "\n4. Checking Java..."
if ! command -v java >/dev/null 2>&1; then
    echo "⚠️  Java not found. PySpark requires Java 8+."
    echo "   Install with: brew install temurin"
    exit 1
fi
echo "✅ Java found: $(java -version 2>&1 | head -n 1)"

# Setup venv
echo "\n5. Setting up Python environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

source .venv/bin/activate

echo "\n6. Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo "\n"
echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps (open 3 terminals):"
echo ""
echo "Terminal 1 (Dashboard):"
echo "  source .venv/bin/activate"
echo "  python -m src.dashboard.app"
echo "  → Open http://127.0.0.1:5000"
echo ""
echo "Terminal 2 (Spark Streaming):"
echo "  source .venv/bin/activate"
echo "  python -m src.spark_streaming"
echo ""
echo "Terminal 3 (Producer):"
echo "  source .venv/bin/activate"
echo "  python -m src.producer --devices 8 --rate 4.0"
echo ""
echo "To stop: Ctrl+C in each terminal, then 'docker compose down'"
echo "========================================"
