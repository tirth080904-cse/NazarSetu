#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "==================================================================="
echo "              NazarSetu - Autonomous Civic Action Platform         "
echo "==================================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found. Please install Python 3.10+."
    exit 1
fi

# Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment 'venv'..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install dependencies
echo "[*] Installing/verifying dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Setup .env if missing
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "[*] Initialized .env configuration file."
fi

echo "[*] Launching NazarSetu on http://localhost:8501 ..."
streamlit run app.py
