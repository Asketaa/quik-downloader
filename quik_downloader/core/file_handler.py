# File handling operations for QUIK Downloader
import os
import configparser
import logging
from typing import Dict, Any, List
from quik_downloader.utils.colors import *

# Get logger for this module
logger = logging.getLogger('QUIK_Downloader.file_handler')

# Project root, so the application finds its own files no matter which
# directory it was launched from (a shortcut, an elevated prompt, or
# 'python /full/path/to/main.py' all used to create a second settings.ini).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class FileHandler:
    """Handles all file operations for the application."""

    def __init__(self):
        """Initialize FileHandler with default paths."""
        self.settings_file = os.path.join(BASE_DIR, 'settings.ini')
        self.urls_file = os.path.join(BASE_DIR, 'URLs.txt')
        self.default_settings = {
            'download_directory': os.path.join(BASE_DIR, 'downloads'),
            'video_quality': 'best',
            'output_format': 'mp4',
            'ffmpeg_path': 'ffmpeg'
        }
        logger.info("FileHandler initialized")
    
    def read_settings(self) -> Dict[str, Any]:
        """
        Reads settings from settings.ini file.
        Creates file with defaults if it doesn't exist.
        
        Returns:
            Dict[str, Any]: Settings dictionary
        """
        config = configparser.ConfigParser(interpolation=None)
        
        try:
            if os.path.exists(self.settings_file):
                config.read(self.settings_file)
                
                if 'SETTINGS' in config:
                    settings = {}
                    for key in self.default_settings:
                        settings[key] = config.get('SETTINGS', key, fallback=self.default_settings[key])
                    
                    settings['download_directory'] = self.normalize_directory(settings['download_directory'])
                    logger.info("Settings loaded successfully")
                    return settings
                else:
                    warning("Invalid settings file - using defaults")
                    return self._create_default_settings()
            else:
                info("Settings file not found - creating with defaults")
                return self._create_default_settings()
                
        except Exception as e:
            error(f"Settings read error: {e}")
            logger.error(f"Error reading settings: {e}")
            return self.default_settings.copy()
    
    def write_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Writes settings to settings.ini file.
        
        Args:
            settings (Dict[str, Any]): Settings to write
            
        Returns:
            bool: True if successful
        """
        config = configparser.ConfigParser(interpolation=None)
        config['SETTINGS'] = settings
        
        try:
            with open(self.settings_file, 'w') as f:
                config.write(f)
            
            logger.info("Settings saved successfully")
            return True
            
        except Exception as e:
            error(f"Settings save error: {e}")
            logger.error(f"Error writing settings: {e}")
            return False
    
    def _create_default_settings(self) -> Dict[str, Any]:
        """Create settings file with default values."""
        try:
            self.write_settings(self.default_settings)
            success("Default settings created")
            logger.info("Default settings file created")
            return self.default_settings.copy()
        except Exception as e:
            error(f"Cannot create settings: {e}")
            logger.error(f"Error creating default settings: {e}")
            return self.default_settings.copy()
    
    def read_urls(self) -> List[str]:
        """Read URLs from URLs.txt, creating the file if it doesn't exist."""
        urls = []
        try:
            if not os.path.exists(self.urls_file):
                logger.info("'URLs.txt' not found, creating it with a welcome message.")
                with open(self.urls_file, 'w', encoding='utf-8') as f:
                    f.write("# Welcome to QUIK Downloader!\n")
                    f.write("# Add your M3U8 video links here, one per line.\n")
                    f.write("# Lines starting with '#' are ignored.\n")
                return [] # Return empty list on first creation

            with open(self.urls_file, 'r', encoding='utf-8') as f:
                # Read non-empty lines that are not comments
                urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

            logger.info(f"Read {len(urls)} URLs from 'URLs.txt'")
            return urls

        except Exception as e:
            logger.error(f"Failed to read URLs from 'URLs.txt': {e}")
            error(f"Could not read 'URLs.txt': {e}")
            return []

    @staticmethod
    def normalize_directory(directory: str) -> str:
        """
        Normalizes a user-supplied directory path.

        Strips surrounding quotes (Windows Explorer's "Copy as path" includes
        them), then expands environment variables and '~'. Without this, such a
        path is stored verbatim and later fails or creates a literal '~' folder.

        Args:
            directory (str): Raw directory path

        Returns:
            str: Normalized directory path
        """
        return os.path.expanduser(os.path.expandvars(directory.strip().strip('"\'')))

    def ensure_download_directory(self, directory: str) -> bool:
        """
        Ensures download directory exists and is writable.
        
        Args:
            directory (str): Directory path
            
        Returns:
            bool: True if directory is ready
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            # Test write permissions
            test_file = os.path.join(directory, '.test_write')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
            except Exception:
                error("Directory not writable")
                return False
            
            logger.info(f"Download directory ready: {directory}")
            return True
            
        except Exception as e:
            error(f"Directory error: {e}")
            logger.error(f"Error with download directory {directory}: {e}")
            return False 