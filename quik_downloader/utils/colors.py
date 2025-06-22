"""
Professional color output system for QUIK Downloader.
Cross-platform color support with robust fallbacks.
"""

import os
import sys
import platform

# Global variable to track color support
COLOR_ENABLED = False


def _init_colors():
    """Initialize color support based on platform and capabilities."""
    global COLOR_ENABLED
    
    # Try colorama first (best cross-platform solution)
    try:
        from colorama import init, Fore, Style
        init(autoreset=True, convert=True, strip=False)
        
        # Enable ANSI support on Windows
        if os.name == 'nt':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                # Enable virtual terminal processing
                handle = kernel32.GetStdHandle(-11)
                kernel32.SetConsoleMode(handle, 7)
            except:
                pass
        
        COLOR_ENABLED = True
        return Fore, Style
        
    except ImportError:
        # Fallback: No colors
        class DummyColors:
            RED = GREEN = YELLOW = CYAN = WHITE = MAGENTA = BLUE = ""
        class DummyStyle:
            BRIGHT = DIM = RESET_ALL = ""
            
        COLOR_ENABLED = False
        return DummyColors(), DummyStyle()


# Initialize colors
Fore, Style = _init_colors()


def _colorize(text: str, color_code: str) -> str:
    """Apply color to text if colors are enabled."""
    if COLOR_ENABLED:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text


def _print_colored(symbol: str, message: str, color_code: str):
    """Print colored message with symbol."""
    colored_symbol = _colorize(symbol, color_code + Style.BRIGHT)
    print(f"{colored_symbol} {message}")


# Core color functions
def print_success(message: str):
    """Print success message in green."""
    _print_colored("✓", message, Fore.GREEN)


def print_error(message: str):
    """Print error message in red."""
    _print_colored("✗", message, Fore.RED)


def print_warning(message: str):
    """Print warning message in yellow."""
    _print_colored("⚠", message, Fore.YELLOW)


def print_info(message: str):
    """Print info message in cyan."""
    _print_colored("ℹ", message, Fore.CYAN)


def print_highlight(message: str):
    """Print highlighted message in magenta."""
    _print_colored("★", message, Fore.MAGENTA)


def print_neutral(message: str):
    """Print neutral message."""
    print(message)


def print_progress(message: str):
    """Print progress message in dim style."""
    if COLOR_ENABLED:
        colored_text = _colorize(f"→ {message}", Style.DIM)
        print(colored_text)
    else:
        print(f"→ {message}")


def colored_text(text: str, color_type: str) -> str:
    """Return colored text string without printing."""
    if not COLOR_ENABLED:
        return text
    
    color_map = {
        'success': Fore.GREEN + Style.BRIGHT,
        'error': Fore.RED + Style.BRIGHT,
        'warning': Fore.YELLOW + Style.BRIGHT,
        'info': Fore.CYAN + Style.BRIGHT,
        'highlight': Fore.MAGENTA + Style.BRIGHT,
        'neutral': Fore.WHITE,
        'dim': Style.DIM
    }
    
    color_code = color_map.get(color_type, Fore.WHITE)
    return _colorize(text, color_code)


def print_separator(char: str = "=", length: int = 50):
    """Print a separator line."""
    line = char * length
    if COLOR_ENABLED:
        print(_colorize(line, Style.DIM))
    else:
        print(line)


def print_header(title: str):
    """Print a formatted header."""
    print_separator()
    if COLOR_ENABLED:
        centered_title = title.center(50)
        print(_colorize(centered_title, Fore.MAGENTA + Style.BRIGHT))
    else:
        print(title.center(50))
    print_separator()


# Shortcuts for common patterns
def success(msg: str): 
    """Shortcut for success message."""
    print_success(msg)

def error(msg: str): 
    """Shortcut for error message."""
    print_error(msg)

def warning(msg: str): 
    """Shortcut for warning message."""
    print_warning(msg)

def info(msg: str): 
    """Shortcut for info message."""
    print_info(msg)

def highlight(msg: str): 
    """Shortcut for highlight message."""
    print_highlight(msg)


def get_color(color_name: str) -> str:
    """Returns the ANSI code for a given color name."""
    if not COLOR_ENABLED:
        return ""
    
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'magenta': Fore.MAGENTA,
        'blue': Fore.BLUE,
        'reset': Style.RESET_ALL,
        'bright': Style.BRIGHT,
        'dim': Style.DIM
    }
    return color_map.get(color_name.lower(), "")


def get_color_status():
    """Return current color support status."""
    return {
        'enabled': COLOR_ENABLED,
        'platform': platform.system(),
        'python_version': sys.version_info[:2],
        'terminal': os.environ.get('TERM', 'unknown')
    }


def test_colors():
    """Test all color functions."""
    print("🎨 QUIK Downloader - Color System Test")
    print_separator()
    
    status = get_color_status()
    print(f"Platform: {status['platform']}")
    print(f"Colors Enabled: {status['enabled']}")
    print(f"Terminal: {status['terminal']}")
    print_separator()
    
    print_success("✓ Success messages (GREEN)")
    print_error("✗ Error messages (RED)")
    print_warning("⚠ Warning messages (YELLOW)")
    print_info("ℹ Info messages (CYAN)")
    print_highlight("★ Highlight messages (MAGENTA)")
    print_neutral("→ Neutral messages (DEFAULT)")
    print_progress("Progress messages (DIM)")
    
    print_separator()
    if COLOR_ENABLED:
        print("🎉 Colors are working!")
    else:
        print("⚠ Colors not available (fallback mode)")


# Test function accessible from command line
if __name__ == "__main__":
    test_colors() 