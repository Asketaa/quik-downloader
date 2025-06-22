#!/bin/bash
# Installation script for QUIK Downloader on macOS and Linux

echo "QUIK Downloader Installer"
echo "--------------------------"

# --- Check for Python 3 ---
if ! command -v python3 &> /dev/null
then
    echo "❌ ERROR: Python 3 is not installed. Please install it to continue."
    exit 1
fi

echo "✅ Python 3 found."

# --- Create Virtual Environment ---
echo "Creating virtual environment in 'venv'..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to create virtual environment."
    exit 1
fi

echo "✅ Virtual environment created."

# --- Activate and Install Requirements ---
echo "Activating environment and installing requirements..."
source venv/bin/activate
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to install required packages."
    exit 1
fi

echo "✅ Requirements installed successfully."
deactivate

echo ""
echo "==========================================="
echo "🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉"
echo "==========================================="
echo ""
echo "✅ Python 3 detected and working"
echo "✅ Virtual environment created in 'venv/'"
echo "✅ All dependencies installed"
echo ""
echo "Next steps:"
echo "  • To run the application, use: bash run.sh"
echo "  • Or double-click 'run.sh' if your system supports it"
echo ""
echo "==========================================="
echo ""

# Multiple methods to pause and ensure user sees the output
echo "Press Enter to close this window..."
read -r 