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
    
    # Check if this is a Debian/Ubuntu system missing python3-venv
    if command -v apt &> /dev/null; then
        echo ""
        echo "🔧 SOLUTION for Debian/Ubuntu/Pop!_OS systems:"
        echo "   The python3-venv package is missing. Install it with:"
        echo ""
        echo "   sudo apt update"
        echo "   sudo apt install python3-venv"
        echo ""
        echo "   Then run this installer again: ./install.sh"
        echo ""
    fi
    
    echo "Press Enter to exit..."
    read -r
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

# Alternative methods for different terminal environments
if [ -n "$DISPLAY" ]; then
    # If running in a graphical environment, try additional pause methods
    echo "If the window closes immediately, run this script from a terminal with: bash install.sh"
    sleep 2
    
    # Try to keep terminal open with multiple methods
    if command -v zenity &> /dev/null; then
        zenity --info --text="Installation completed successfully!\n\nTo run the application, use: bash run.sh" --width=400 2>/dev/null
    fi
    
    # Final fallback - longer sleep
    sleep 5
fi 