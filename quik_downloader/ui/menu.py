# Main menu interface for QUIK Downloader
import os
import logging
from typing import List
from quik_downloader.core.file_handler import FileHandler
from quik_downloader.core.downloader import VideoDownloader
from quik_downloader.ui.settings_manager import SettingsManager
from quik_downloader.utils.file_editor import file_editor
from quik_downloader.utils.colors import *

# Get logger for this module
logger = logging.getLogger('QUIK_Downloader.menu')

class MenuInterface:
    """Main menu interface for the application."""
    
    def __init__(self):
        """Initialize MenuInterface with required components."""
        self.file_handler = FileHandler()
        self.settings_manager = SettingsManager()
        logger.info("MenuInterface initialized")
    
    def _clear_screen(self):
        """Clear terminal screen (cross-platform)."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self, title: str = ""):
        """Displays the application header."""
        self._clear_screen()
        if title:
            print_header(title)
        else:
            print(colored_text("QUIK Downloader", 'highlight'))
            print_neutral("Powered by FFMPEG | Navigate with numeric keys")
            print_separator(char='=')

    def show_main_menu(self):
        """Display the main menu options."""
        print("--------------------")
        print("  1. Download")
        print("  2. Edit URLs.txt")
        print("  3. Settings")
        print("  4. Exit")
        print()
        print_separator()
    
    def get_user_choice(self) -> str:
        """Get and validate user menu choice."""
        return input(f"{colored_text('➤ Select an option (1-4):', 'neutral')} ").strip()
    
    def run(self):
        """Main application loop."""
        while True:
            try:
                self.show_header()
                self.show_main_menu()
                
                choice = self.get_user_choice()
                
                if choice == '1':
                    self.download_videos()
                elif choice == '2':
                    self.edit_urls_file()
                elif choice == '3':
                    self.open_settings()
                elif choice == '4':
                    self.exit_application()
                    break
                else:
                    error("Invalid choice! Select 1-4")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                warning("\nApplication interrupted by user")
                break
            except Exception as e:
                error(f"Unexpected error: {e}")
                logger.error(f"Unexpected error in main loop: {e}")
                input("Press Enter to continue...")
    
    def download_videos(self):
        """Handle video downloading process."""
        self.show_header("VIDEO DOWNLOAD")
        
        # Refresh settings and get ffmpeg_path
        self.settings_manager.settings = self.file_handler.read_settings()
        ffmpeg_path = self.settings_manager.settings.get('ffmpeg_path', 'ffmpeg')
        logger.info(f"Using FFMPEG path: {ffmpeg_path}")

        # Check dependencies first using the correct path
        temp_downloader = VideoDownloader(ffmpeg_path=ffmpeg_path)
        if not temp_downloader.check_dependencies():
            print()
            warning("FFMPEG not found or not working!")
            print("  - Please install it and add it to your system's PATH.")
            print("  - Or, set the full path to the executable in Settings.")
            input("\nPress Enter to continue...")
            return
        
        # Get URLs
        urls = self.file_handler.read_urls()
        if not urls:
            warning("No URLs found")
            print_neutral("Add URLs using option 2 (Edit URLs.txt)")
            input("\nPress Enter to continue...")
            return
        
        print_info(f"{len(urls)} video(s) ready")
        
        # Ensure download directory exists
        download_dir = self.settings_manager.settings['download_directory']
        if not self.file_handler.ensure_download_directory(download_dir):
            error("Cannot access download directory")
            input("Press Enter to continue...")
            return
        
        # Show current settings
        quality = self.settings_manager.settings['video_quality']
        format_type = self.settings_manager.settings['output_format']
        print_neutral(f"Quality: {quality} | Format: {format_type}")
        
        # Confirm download
        print()
        confirm = input(f"{colored_text('Start download? (y/N):', 'neutral')} ").strip().lower()
        if confirm not in ['y', 'yes']:
            warning("Cancelled")
            input("Press Enter to continue...")
            return
        
        # Create downloader with current settings
        downloader = VideoDownloader(
            video_quality=quality,
            output_format=format_type,
            ffmpeg_path=ffmpeg_path
        )
        
        # Start downloads
        print()
        print_separator()
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n{colored_text(f'Video {i}/{len(urls)}', 'info')}")
            
            try:
                if downloader.download_video(url, download_dir):
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                error(f"Error: {str(e)[:30]}")
                failed += 1
                logger.error(f"Download exception for {url}: {e}")
        
        # Summary
        print()
        print_separator()
        
        if successful > 0:
            success(f"{successful} completed")
        if failed > 0:
            error(f"{failed} failed")
        
        if successful == len(urls):
            highlight("All downloads successful!")
        
        logger.info(f"Download session completed: {successful}/{len(urls)} successful")
        
        input("\nPress Enter to continue...")
    
    def edit_urls_file(self):
        """Open URLs.txt file for editing."""
        self.show_header("EDIT URLs.txt")
        
        print_info("Opening URLs.txt for editing...")
        print_neutral("Add one URL per line")
        print_neutral("Save and close when finished")
        print()
        
        try:
            file_editor("URLs.txt")
            success("File editing completed")
        except Exception as e:
            error(f"Cannot open file: {e}")
            logger.error(f"Error opening URLs.txt: {e}")
        
        input("Press Enter to continue...")
    
    def open_settings(self):
        """Open the settings menu."""
        self.show_header("SETTINGS")
        logger.info("Opening settings menu")
        self.settings_manager.show_settings_menu()
    
    def exit_application(self):
        """Handle application exit."""
        self.show_header("GOODBYE")
        print_highlight("Thank you for using QUIK Downloader!")
        print_neutral("Application closing...")
        logger.info("Application exit requested by user") 