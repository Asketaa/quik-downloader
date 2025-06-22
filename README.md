# QUIK Downloader

A fast, professional, and cross-platform M3U8 video downloader for your terminal, powered by Python and FFMPEG.

![image](https://github.com/user-attachments/assets/e60388d1-c1f1-43f1-b924-a15d7e5d8a0d)

## Features

- **Sequential Downloads**: Downloads videos one by one from a list.
- **Customizable Quality**: Choose between direct stream copy (`best`) or re-encode to specific resolutions (`720p`, `480p`, `360p`).
- **Multiple Formats**: Save videos as `.mp4`, `.mkv`, `.avi`, or `.mov`.
- **Easy URL Management**: Edit a simple `URLs.txt` file to manage your download queue.
- **Professional Output**: Clean, color-coded, and framed terminal output.
- **Persistent Settings**: All your configurations are saved in a `settings.ini` file.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

---

## Prerequisites

Before you begin, please ensure you have the following installed on your system. The provided installation scripts handle the project's dependencies, but they **do not** install Python or FFMPEG. You must install them manually.

- **Python 3.7+**
  <details>
  <summary><b>Click for Python Installation Instructions</b></summary>
  
  - **Windows**: Download from [python.org](https://www.python.org/downloads/). **Important:** During installation, make sure to check the box that says **"Add Python to PATH"**.
  - **macOS**: The easiest way is to use [Homebrew](https://brew.sh/): `brew install python`
  - **Linux (Debian/Ubuntu)**: `sudo apt update && sudo apt install python3`
  
  </details>

- **FFMPEG**
  <details>
  <summary><b>Click for FFMPEG Installation Instructions</b></summary>
  
  FFMPEG is essential for downloading and processing videos. You must install it and ensure it's accessible via your system's PATH.
  
  - **On Windows**:
    1.  Go to the [FFMPEG downloads page](https://www.gyan.dev/ffmpeg/builds/) and download a release build (e.g., `ffmpeg-release-full.7z`).
    2.  Extract the archive using a tool like [7-Zip](https://www.7-zip.org/).
    3.  Move the extracted folder to a permanent location, like `C:\ffmpeg`.
    4.  Add the `bin` directory from that folder (e.g., `C:\ffmpeg\bin`) to your system's `PATH` environment variable.

  - **On macOS**:
    The easiest way is to use [Homebrew](https://brew.sh/): `brew install ffmpeg`

  - **On Linux (Debian/Ubuntu)**:
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
    
  *After installing, you may need to restart your terminal or PC for the `PATH` changes to take effect.*
  </details>

---

## Easy Installation & Usage

For the simplest setup, use the provided scripts.

1.  **Clone or download the repository.**
2.  **Run the installer:**
    -   On **Windows**, double-click `install.bat`.
    -   On **macOS/Linux**, open your terminal, navigate to the folder, and run: `bash install.sh`
        
        *Note: If you get a permission error, run: `chmod +x install.sh run.sh` first*
        
3.  **Run the application:**
    -   On **Windows**, double-click `run.bat`.
    -   On **macOS/Linux**, run: `bash run.sh`

---

<details>
<summary><b>For Advanced Users: Manual Installation</b></summary>

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/m3u8DL.git
    cd m3u8DL
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```
</details>

---

## Configuration

Upon first run, a `settings.ini` file is created. You can edit your preferences here or through the in-app **Settings** menu.

```ini
[General]
download_directory = downloads
video_quality = best
output_format = mp4
ffmpeg_path = ffmpeg
```

- **`download_directory`**: Where your videos will be saved.
- **`video_quality`**: `best` (fastest), `high` (720p), `medium` (480p), `low` (360p).
- **`output_format`**: `mp4`, `mkv`, `avi`, `mov`.
- **`ffmpeg_path`**: If FFMPEG is not in your system's PATH, provide the full path to the executable here (e.g., `C:\ffmpeg\bin\ffmpeg.exe`).

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Project Structure

```
m3u8DL/
├── .gitignore             # Git ignore file
├── downloads/             # Default directory for downloaded videos
├── quik_downloader/       # Main application package
│   ├── core/
│   │   ├── downloader.py  # Core download logic using FFMPEG
│   │   └── file_handler.py# Manages files and directories
│   ├── ui/
│   │   ├── menu.py        # Interactive terminal menu
│   │   └── settings_manager.py # Manages application settings
│   └── utils/
│       ├── colors.py      # Color system for console output
│       └── file_editor.py # Cross-platform file editing
├── main.py                # Application entry point
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── settings.ini           # User-defined settings
└── URLs.txt               # List of video URLs to download
```

## Error Handling

The application provides clear feedback for common issues:
- Missing FFMPEG dependency.
- Invalid URLs or network problems.
- File system permission errors.
- User-initiated interruptions (`Ctrl+C`).

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the tool.

## Disclaimer

This tool is provided for educational purposes only. The user is solely responsible for ensuring they have the legal right to download and store any content accessed through this application. 