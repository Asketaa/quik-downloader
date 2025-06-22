import shutil
from quik_downloader.utils.colors import print_progress, get_color

def get_terminal_width():
    """Gets the width of the terminal."""
    return shutil.get_terminal_size((80, 20)).columns

def print_header(title: str):
    """Prints a styled header box for FFMPEG output."""
    width = get_terminal_width()
    
    # Use cyan for the box
    box_color = get_color('cyan')
    reset_color = get_color('reset')
    
    title_text = f" FFMPEG Output: {title} "
    
    print(box_color + '┌' + '─' * (width - 2) + '┐' + reset_color)
    print(box_color + '│' + title_text.center(width - 2) + '│' + reset_color)
    print(box_color + '├' + '─' * (width - 2) + '┤' + reset_color)

def print_content_line(line: str):
    """Prints a line of content within the box, correctly formatted."""
    width = get_terminal_width()
    
    box_color = get_color('cyan')
    reset_color = get_color('reset')

    # Clean the line from ffmpeg
    cleaned_line = line.strip()

    # Truncate line if it's too long
    max_line_width = width - 4
    if len(cleaned_line) > max_line_width:
        cleaned_line = cleaned_line[:max_line_width]
    
    # Format and print
    formatted_line = f" {cleaned_line.ljust(width - 4)} "
    print(box_color + '│' + reset_color + formatted_line + box_color + '│' + reset_color)

def print_progress_line(line: str):
    """Prints a progress line within the box, using carriage return to overwrite."""
    width = get_terminal_width()
    
    box_color = get_color('cyan')
    reset_color = get_color('reset')

    # Clean the line from ffmpeg
    cleaned_line = line.strip()

    # Truncate line if it's too long
    max_line_width = width - 4
    if len(cleaned_line) > max_line_width:
        cleaned_line = cleaned_line[:max_line_width]
    
    # Format and print using carriage return
    formatted_line = f" {cleaned_line.ljust(width - 4)} "
    print(box_color + '│' + reset_color + formatted_line + box_color + '│' + reset_color, end='\r')

def print_footer():
    """Prints the footer of the box."""
    width = get_terminal_width()
    box_color = get_color('cyan')
    reset_color = get_color('reset')
    
    print(box_color + '└' + '─' * (width - 2) + '┘' + reset_color)

def print_boxed_output(title: str, output_lines: list):
    """Prints a list of lines inside a styled box."""
    print_header(title)
    for line in output_lines:
        print_content_line(line)
    print_footer() 