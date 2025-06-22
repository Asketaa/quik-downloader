# Cross-platform file editing utilities
import os
import subprocess
import platform
import logging
import sys
from quik_downloader.utils.colors import *

# Get logger for this module
logger = logging.getLogger('QUIK_Downloader.file_editor')

class FileEditor:
    """Cross-platform file editor for URLs.txt file."""
    
    def __init__(self):
        """Initialize FileEditor."""
        self.urls_file = 'URLs.txt'
    
    def open_urls_file(self):
        """Opens URLs.txt file with appropriate text editor for the OS."""
        print("📝 EDIT URLs.txt")
        print("=" * 20)
        
        # Check if file exists, create if not
        if not os.path.exists(self.urls_file):
            if self._create_urls_file():
                logger.info("Created new URLs.txt file for editing")
            else:
                logger.error("Failed to create URLs.txt file")
                return
        
        # Open file with OS-appropriate editor
        try:
            if self._open_file_with_editor():
                logger.info("Successfully opened URLs.txt with system editor")
                print("INFO: URLs.txt editing completed.")
            else:
                logger.warning("Could not open file with editor")
                print("ERROR: Could not open file with editor.")
                print("You can manually edit the URLs.txt file with any text editor.")
        except Exception as e:
            logger.error(f"Error during file editing: {e}")
    
    def _create_urls_file(self) -> bool:
        """Creates a new URLs.txt file with example content."""
        try:
            logger.info("Creating new URLs.txt file")
            print("ERROR: URLs.txt file not found!")
            print("Create a new URLs.txt file? (y/N): ", end="")
            choice = input().strip().lower()
            
            if choice in ['y', 'yes']:
                self._create_urls_file()
            else:
                print("Operation cancelled.")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            print(f"ERROR: Error creating file: {e}")
            return False
    
    def _open_file_with_editor(self) -> bool:
        """Opens file with appropriate editor based on OS."""
        try:
            os_name = platform.system().lower()
            
            if os_name == 'windows':
                return self._open_windows_editor()
            elif os_name == 'darwin':  # macOS
                return self._open_macos_editor()
            else:  # Linux and others
                return self._open_linux_editor()
                
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            print(f"ERROR: Error opening file: {e}")
            return False
    
    def _open_windows_editor(self) -> bool:
        """Opens file with Windows Notepad."""
        try:
            subprocess.run(['notepad', self.urls_file], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Failed to open with notepad on Windows")
            return False
    
    def _open_macos_editor(self) -> bool:
        """Opens file with macOS default text editor."""
        try:
            subprocess.run(['open', '-t', self.urls_file], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Failed to open with default text editor on macOS")
            return False
    
    def _open_linux_editor(self) -> bool:
        """Opens file with Linux text editor (tries multiple options)."""
        editors = ['nano', 'vim', 'vi', 'gedit']
        
        for editor in editors:
            try:
                subprocess.run([editor, self.urls_file], check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        logger.warning("No suitable text editor found on Linux")
        print("ERROR: No suitable text editor found!")
        print("Please manually edit URLs.txt file")
        return False 

    def _create_urls_file(self):
        """Create a new URLs.txt file with template content."""
        template_content = """# File for video URLs to download
# One URL per line
# Example:
# https://example.com/video1.m3u8
# https://example.com/video2.mp4

"""
        
        try:
            with open(self.urls_file, "w", encoding="utf-8") as f:
                f.write(template_content)
            print("SUCCESS: Created new URLs.txt file.")
            logger.info("Created new URLs.txt file")
            
            # Try to open the new file for editing
            self._open_with_system_editor(self.urls_file)
        except Exception as e:
            print(f"ERROR: Error creating file: {e}")
            logger.error(f"Error creating URLs.txt file: {e}")

    def _open_with_system_editor(self, file_path: str):
        """Opens a file with the system's default text editor."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', '-t', file_path])
            else:  # Linux and other Unix-like systems
                # Try various text editors in order of preference
                editors = ['nano', 'vim', 'vi', 'gedit']
                for editor in editors:
                    try:
                        subprocess.run([editor, file_path], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    print(f"ERROR: Error opening file: {e}")
                    logger.error(f"Error opening file with system editor: {e}")
                
            return True
        except Exception as e:
            print(f"ERROR: Error opening file: {e}")
            logger.error(f"Error opening file with system editor: {e}")
            return False

    def _handle_file_not_found(self):
        """Handle case when URLs.txt doesn't exist."""
        print("ERROR: URLs.txt file not found!")
        print("Create a new URLs.txt file? (y/N): ", end="")
        choice = input().strip().lower()
        
        if choice in ['y', 'yes']:
            self._create_urls_file()
        else:
            print("Operation cancelled.")

def file_editor(file_path: str):
    """
    Opens a file for editing using the system default editor.
    Cross-platform compatible.
    
    Args:
        file_path (str): Path to the file to edit
    """
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'w') as f:
                f.write("")
            logger.info(f"Created new file: {file_path}")
        except Exception as e:
            error(f"Cannot create file: {e}")
            logger.error(f"Failed to create file {file_path}: {e}")
            return
    
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows - use notepad
            subprocess.run(['notepad', file_path], check=True)
        elif system == "Darwin":
            # macOS - use TextEdit
            subprocess.run(['open', '-e', file_path], check=True)
        else:
            # Linux/Unix - try common editors
            editors = ['nano', 'vim', 'gedit', 'kate']
            editor_found = False
            
            for editor in editors:
                try:
                    subprocess.run([editor, file_path], check=True)
                    editor_found = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if not editor_found:
                warning("No suitable editor found")
                print_info("Trying system default...")
                subprocess.run(['xdg-open', file_path], check=True)
                
        logger.info(f"File editor opened for: {file_path}")
        
    except subprocess.CalledProcessError as e:
        error(f"Editor failed: {e}")
        logger.error(f"Editor subprocess error for {file_path}: {e}")
    except FileNotFoundError:
        error("Editor not found")
        logger.error(f"Editor not found for {file_path}")
    except Exception as e:
        error(f"Cannot open editor: {e}")
        logger.error(f"Unexpected error opening editor for {file_path}: {e}") 