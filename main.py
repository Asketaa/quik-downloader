#!/usr/bin/env python3
"""
QUIK Downloader - Professional Video Downloading Tool
A cross-platform video downloader powered by FFMPEG.
"""

import logging
import sys
import os
from quik_downloader.ui.menu import MenuInterface
from quik_downloader.utils.colors import *

def setup_logging():
    """Configure logging for the application."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Only log to file, not console for cleaner user experience
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('quik_downloader.log')
        ]
    )
    
    # Set specific loggers to WARNING to reduce noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        error("Python 3.7 or higher required")
        print_info(f"Current version: {sys.version}")
        sys.exit(1)

def main():
    """Main application entry point."""
    try:
        # Check Python version
        check_python_version()
        
        # Setup logging
        setup_logging()
        logger = logging.getLogger('QUIK_Downloader')
        logger.info("Application starting")
        
        # Create and run menu interface
        menu = MenuInterface()
        menu.run()
        
        logger.info("Application terminated normally")
        
    except KeyboardInterrupt:
        warning("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        error(f"Critical error: {e}")
        logging.error(f"Critical application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 