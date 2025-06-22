# Video downloader core module for QUIK Downloader
import subprocess
import time
import logging
import os
from typing import List, Optional
from urllib.parse import urlparse
from quik_downloader.utils.colors import *
from quik_downloader.ui.output_framer import print_header, print_content_line, print_footer, print_progress_line

# Get logger for this module
logger = logging.getLogger('QUIK_Downloader.downloader')

class VideoDownloader:
    """Handles M3U8 video downloading operations using FFMPEG."""
    
    def __init__(self, video_quality: str = 'best', output_format: str = 'mp4', 
                 ffmpeg_path: Optional[str] = None):
        """Initialize VideoDownloader with quality and format settings."""
        self.video_quality = video_quality
        self.output_format = output_format  
        self.ffmpeg_path = ffmpeg_path or 'ffmpeg'
        logger.info(f"VideoDownloader initialized: quality={video_quality}, format={output_format}")
        
    def set_quality(self, quality: str):
        """Update video quality setting."""
        self.video_quality = quality
        logger.info(f"Quality updated to: {quality}")
        
    def set_format(self, output_format: str):
        """Update output format setting."""
        self.output_format = output_format
        logger.info(f"Format updated to: {output_format}")
        
    def download_video(self, url: str, output_dir: str) -> bool:
        """Download a single video with configured settings."""
        if not url.strip() or not url.lower().startswith(('http://', 'https://')):
            error(f"Invalid or empty URL skipped: {url[:50]}...")
            return False
            
        try:
            # Generate output filename
            output_path = self._generate_output_filename(url, output_dir)
            
            # Show simple start message
            print_progress("Starting download...")
            
            # Build FFMPEG command based on quality setting
            cmd = self._build_ffmpeg_command(url, output_path)
            
            # Execute download, showing FFMPEG's native output
            if self._execute_ffmpeg_command(cmd, os.path.basename(output_path)):
                # Verify file was created and has content
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                    success(f"Download complete. File size: {file_size:.1f}MB")
                    logger.info(f"Successfully downloaded: {url}")
                    return True
                else:
                    error("Download finished, but the output file is empty.")
                    return False
            else:
                # For re-encoding failures, try fallback to copy mode
                if self.video_quality != 'best':
                    warning("Re-encoding failed. Attempting a direct copy as a fallback...")
                    return self._try_fallback_download(url, output_path)
                else:
                    error("Download failed. Check FFMPEG output above for details.")
                    return False
                    
        except subprocess.TimeoutExpired:
            error("FFMPEG process timed out (1 hour limit).")
            return False
        except Exception as e:
            error(f"An unexpected error occurred during download: {e}")
            logger.error(f"Exception downloading {url}: {e}")
            return False
    
    def _execute_ffmpeg_command(self, cmd: List[str], title: str) -> bool:
        """Executes the FFMPEG command and shows its output in a styled frame."""
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                       text=True, encoding='utf-8', errors='replace')
            
            print_header(title)
            
            # Read and print output line by line
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    # FFMPEG stats updates often use carriage return
                    if '\r' in line or line.lstrip().startswith(('frame=', 'size=')):
                        print_progress_line(line)
                    else:
                        print_content_line(line)
                process.stdout.close()
            
            # After progress line, move to next line before footer
            print() 

            # Wait for the process to finish
            return_code = process.wait()
            
            print_footer()
            
            return return_code == 0
            
        except FileNotFoundError:
            error(f"FFMPEG command not found. Please check your installation and PATH.")
            logger.error(f"FFMPEG not found when trying to execute command: {' '.join(cmd)}")
            return False
        except Exception as e:
            error(f"Failed to execute FFMPEG command: {e}")
            logger.error(f"Error executing FFMPEG command: {e}")
            return False
    
    def _generate_output_filename(self, url: str, output_dir: str) -> str:
        """Generate output filename based on URL."""
        try:
            # Extract domain name from URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')
            
            # Create timestamp for uniqueness
            timestamp = int(time.time())
            
            # Format: domain_timestamp.format
            filename = f"{domain}_{timestamp}.{self.output_format}"
            return os.path.join(output_dir, filename)
            
        except Exception:
            # Fallback: use generic timestamp
            timestamp = int(time.time())
            filename = f"video_{timestamp}.{self.output_format}"
            return os.path.join(output_dir, filename)
    
    def _get_quality_params(self) -> List[str]:
        """Get FFMPEG parameters for selected quality."""
        quality_map = {
            'best': ['-c', 'copy'],
            'high': ['-vf', 'scale=-2:720', '-c:v', 'libx264', '-c:a', 'aac'],
            'medium': ['-vf', 'scale=-2:480', '-c:v', 'libx264', '-c:a', 'aac'],
            'low': ['-vf', 'scale=-2:360', '-c:v', 'libx264', '-c:a', 'aac']
        }
        
        return quality_map.get(self.video_quality, quality_map['best'])
    
    def _build_ffmpeg_command(self, url: str, output_path: str) -> List[str]:
        """Build FFMPEG command for download."""
        cmd = [
            self.ffmpeg_path,
            '-i', url,
            '-bsf:a', 'aac_adtstoasc',
            '-y'  # Overwrite output file
        ]
        
        # Add FFMPEG flags to reduce console verbosity for cleaner output
        # -loglevel error: Shows only errors
        # -stats: Shows progress stats
        cmd.extend(['-loglevel', 'error', '-stats'])

        # Add quality parameters
        quality_params = self._get_quality_params()
        cmd.extend(quality_params)
        cmd.append(output_path)
        
        logger.debug(f"FFMPEG command: {' '.join(cmd)}")
        return cmd
    
    def _try_fallback_download(self, url: str, output_path: str) -> bool:
        """Fallback to copy mode if re-encoding fails."""
        try:
            # Build fallback command with copy mode
            fallback_cmd = [
                self.ffmpeg_path,
                '-i', url,
                '-c', 'copy',
                '-bsf:a', 'aac_adtstoasc',
                '-y',
                output_path
            ]
            
            if self._execute_ffmpeg_command(fallback_cmd, "Fallback Attempt"):
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    success("Fallback download method successful.")
                    logger.info(f"Fallback download successful for: {url}")
                    return True
                else:
                    error("Fallback download finished, but the output file is empty.")
                    return False
            else:
                error("The alternative download method (direct copy) also failed.")
                return False
                
        except Exception as e:
            error(f"An unexpected error occurred during fallback download: {e}")
            logger.error(f"Fallback exception for {url}: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check if FFMPEG is available."""
        try:
            result = subprocess.run([self.ffmpeg_path, '-version'], 
                                    capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True
            else:
                error("FFMPEG not working")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            error("FFMPEG not found")
            return False
        except Exception as e:
            error(f"FFMPEG check failed")
            return False 