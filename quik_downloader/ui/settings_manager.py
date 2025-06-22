# Settings management for QUIK Downloader
import os
import logging
from typing import Dict, Any, List, Tuple
from quik_downloader.core.file_handler import FileHandler
from quik_downloader.utils.colors import *

# Get logger for this module
logger = logging.getLogger('QUIK_Downloader.settings_manager')

class SettingsManager:
    """Handles all settings-related operations."""
    
    def __init__(self):
        """Initialize SettingsManager with FileHandler."""
        self.file_handler = FileHandler()
        self.settings = self.file_handler.read_settings()
        logger.info("SettingsManager initialized")
    
    def _clear_screen(self):
        """Clears the terminal screen - Cross Platform."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _get_quality_options(self) -> Dict[str, Dict[str, str]]:
        """Returns detailed quality options with descriptions and technical info."""
        return {
            'best': {
                'name': '[BEST] Original Quality',
                'description': 'Direct stream copy (~30s)',
                'technical': '-c copy',
                'speed': 'FAST',
                'warning': None
            },
            'high': {
                'name': '[HIGH] 720p Quality', 
                'description': 'Re-encoding to 720p (~2-5min)',
                'technical': '-vf scale=-2:720 -c:v libx264',
                'speed': 'SLOW',
                'warning': 'Requires re-encoding (much slower)'
            },
            'medium': {
                'name': '[MEDIUM] 480p Quality',
                'description': 'Re-encoding to 480p (~2-5min)', 
                'technical': '-vf scale=-2:480 -c:v libx264',
                'speed': 'SLOW',
                'warning': 'Requires re-encoding (much slower)'
            },
            'low': {
                'name': '[LOW] 360p Quality',
                'description': 'Re-encoding to 360p (~2-5min)',
                'technical': '-vf scale=-2:360 -c:v libx264', 
                'speed': 'SLOW',
                'warning': 'Requires re-encoding (much slower)'
            }
        }
    
    def _validate_quality_input(self, quality: str) -> Tuple[bool, str]:
        """Validates quality input and returns validation result."""
        if not quality:
            return True, "No change"
            
        quality = quality.lower().strip()
        valid_options = self._get_quality_options().keys()
        
        if quality in valid_options:
            return True, quality
        else:
            return False, f"Valid options: {', '.join(valid_options)}"
    
    def _show_quality_detailed_info(self):
        """Shows detailed information about all quality options."""
        print_header("QUALITY OPTIONS")
        
        options = self._get_quality_options()
        for key, info in options.items():
            print(f"\n{colored_text(info['name'], 'highlight')}")
            print(f"   {info['description']}")
            print(f"   Command: {colored_text(info['technical'], 'dim')}")
            print(f"   Speed: {colored_text(info['speed'], 'info')}")
            if info['warning']:
                print(f"   {colored_text('⚠ ' + info['warning'], 'warning')}")
    
    def _show_quality_warning(self, quality: str):
        """Shows warning for qualities that require re-encoding."""
        options = self._get_quality_options()
        if quality in options and options[quality]['warning']:
            warning(options[quality]['warning'])
            info("TIP: Use 'best' for fast downloads")
            
            confirm = input(f"\n{colored_text('Continue? (y/N):', 'neutral')} ").strip().lower()
            return confirm in ['y', 'yes']
        return True
    
    def show_settings_menu(self):
        """Display and handle the settings menu."""
        while True:
            self._clear_screen()
            self._display_settings()
            choice = input(f"\n{colored_text('Select option (1-6):', 'neutral')} ").strip()
            
            if choice == '1':
                self._edit_download_directory()
            elif choice == '2':
                self._edit_video_quality()
            elif choice == '3':
                self._edit_output_format()
            elif choice == '4':
                self._edit_ffmpeg_path()
            elif choice == '5':
                self._save_settings()
            elif choice == '6':
                logger.info("Exiting settings menu")
                break
            else:
                error("Invalid choice! Select 1-6")
                input("\nPress Enter to continue...")
    
    def _display_settings(self):
        """Display current settings."""
        print_header("SETTINGS")
        
        print(f"\n{colored_text('Current Settings:', 'info')}")
        print(f"  1. Download Directory: {colored_text(self.settings['download_directory'], 'neutral')}")
        print(f"  2. Video Quality: {colored_text(self.settings['video_quality'], 'highlight')}")
        print(f"  3. Output Format: {colored_text(self.settings['output_format'], 'neutral')}")
        
        ffmpeg_path = self.settings.get('ffmpeg_path') or 'ffmpeg'
        display_path = ffmpeg_path if ffmpeg_path != 'ffmpeg' else 'Auto (in PATH)'
        print(f"  4. FFMPEG Path: {colored_text(display_path, 'dim')}")
        
        print(f"\n  5. {colored_text('Save Settings', 'success')}")
        print(f"  6. {colored_text('Back to Main Menu', 'neutral')}")
        
        print_separator()
    
    def _edit_download_directory(self):
        """Modifies the download directory."""
        print(f"\nCurrent: {colored_text(self.settings['download_directory'], 'info')}")
        new_dir = input("New directory (Enter = keep current): ").strip()
        
        if new_dir:
            if self.file_handler.ensure_download_directory(new_dir):
                self.settings['download_directory'] = new_dir
                success(f"Updated to: {new_dir}")
                warning("Remember: Save settings to persist!")
            else:
                error("Invalid directory path")
        
        input("\nPress Enter to continue...")
    
    def _edit_video_quality(self):
        """Modifies the video quality with enhanced validation and warnings."""
        print(f"\nCurrent: {colored_text(self.settings['video_quality'], 'highlight')}")
        
        self._show_quality_detailed_info()
        
        print(f"\n{colored_text('Type', 'dim')} {colored_text('info', 'info')} {colored_text('to see options again', 'dim')}")
        new_quality = input("New quality (Enter = keep current): ").strip()
        
        if new_quality.lower() == 'info':
            input("\nPress Enter to continue...")
            return
        
        is_valid, result = self._validate_quality_input(new_quality)
        
        if not is_valid:
            error(result)
            input("Press Enter to continue...")
            return
        
        if result == "No change":
            input("Press Enter to continue...")
            return
        
        if not self._show_quality_warning(result):
            warning("Operation cancelled")
            input("Press Enter to continue...")
            return
        
        self.settings['video_quality'] = result
        success(f"Quality updated to: {result}")
        warning("Remember: Save settings to persist!")
        
        input("Press Enter to continue...")
    
    def _edit_output_format(self):
        """Modifies the output format."""
        print(f"\nCurrent: {colored_text(self.settings['output_format'], 'highlight')}")
        print(f"Options: {colored_text('mp4, mkv, avi, mov', 'dim')}")
        new_format = input("New format (Enter = keep current): ").strip().lower()
        
        if new_format and new_format in ['mp4', 'mkv', 'avi', 'mov']:
            self.settings['output_format'] = new_format
            success(f"Format updated to: {new_format}")
            warning("Remember: Save settings to persist!")
        elif new_format:
            error("Invalid format")
        
        input("Press Enter to continue...")
    
    def _edit_ffmpeg_path(self):
        """Modifies the FFMPEG path."""
        current = self.settings.get('ffmpeg_path') or 'ffmpeg'
        display_path = current if current != 'ffmpeg' else 'Auto (in PATH)'
        print(f"\nCurrent: {colored_text(display_path, 'info')}")
        print(f"{colored_text('Leave empty to use system PATH (default)', 'dim')}")
        new_path = input("Enter full path to FFMPEG executable: ").strip()
        
        # If user enters nothing, we set it to the default 'ffmpeg'
        self.settings['ffmpeg_path'] = new_path or 'ffmpeg'
        
        if self.settings['ffmpeg_path'] == 'ffmpeg':
            success("FFMPEG path set to auto-detection (from PATH)")
        else:
            success(f"FFMPEG path updated to: {self.settings['ffmpeg_path']}")
        
        warning("Remember: Save settings to persist!")
        input("\nPress Enter to continue...")
    
    def _save_settings(self):
        """Save current settings to file."""
        print_progress("Saving settings...")
        
        try:
            if self.file_handler.write_settings(self.settings):
                logger.info("Settings saved successfully")
                success("Settings saved successfully!")
            else:
                logger.error("Failed to save settings")
                error("Failed to save settings")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            error(f"Save failed: {e}")
        
        input("Press Enter to continue...") 