#!/bin/bash
# Run script for QUIK Downloader on macOS and Linux

# --- Check for venv ---
if [ ! -d "venv" ]; then
    echo "❌ ERROR: Virtual environment not found."
    echo "Please run the 'install.sh' script first."
    read -p "Press Enter to exit..."
    exit 1
fi

# --- Activate venv and run ---
source venv/bin/activate
python3 main.py

# --- Deactivate on exit ---
deactivate
echo ""
echo "Application closed." 