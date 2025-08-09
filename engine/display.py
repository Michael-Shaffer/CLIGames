import re
import shutil
from enum import Enum
from typing import List, Tuple, Optional

class Color(Enum):
    """ANSI color codes"""
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Normal intensity versions
    DARK_RED = '\033[31m'
    DARK_GREEN = '\033[32m'
    DARK_YELLOW = '\033[33m'
    DARK_BLUE = '\033[34m'

    # Special color codes
    RESET = '\033[0m'

class Display:
    """Terminal display manager with buffering support"""

    # ANSI escape codes
    CLEAR_SCREEN = '\033[2J'
    CURSOR_HOME = '\033[H'

    ANSI_PATTERN = re.compile(r'\033\[[0-9;]*m')

    def __init__(self, *, immediate_flush: bool = False):
        # Get terminal dimensions
        size = shutil.get_terminal_size((80, 24)) # Fallback values
        self.width = size.columns
        self.height = size.lines

        # Frame buffer for batched output
        self.frame_buffer: List[Tuple[int, int, str]] = []
        self.immediate_flush = immediate_flush

    def _move_cursor(self, x: int, y: int) -> str: 
        return f'\033[{y};{x}H'

    def clear(self, *, move_cursor_top_left: bool = True) -> None:
        """Clears terminal screen and buffer

        Args:
            move_cursor_top_left: If True, move cursor to the top left of terminal after clearing
        """

        # Apply settings
        result = self.CLEAR_SCREEN
        if move_cursor_top_left: 
            result += self.CURSOR_HOME

        # Perform clear
        self.frame_buffer.clear()
        print(result, end='', flush=True)

    def print_at(self, x: int, y: int, text: str) -> None:
        """Print text at specific coordinates.

        Args:
            x: Column position (1-indexed)
            y: Row position (1-indexed)
            text: Text to display. Truncated if it exceeds terminal width

        Raises:
            ValueError: If coordinates are out of terminal bounds

        Note:
            Truncation may break ANSI color codes. Avoid printing colored
            text near the right edge of the terminal.
        """

        # Check bounds
        if not(1 <= x <= self.width and 1 <= y <= self.height):
            raise ValueError(f"Position ({x}, {y}) out of bounds for display of size {self.width}x{self.height}")

        if x + len(text) - 1 > self.width:
            text = text[:self.width - x + 1] # Truncate

        # ANSI escape code
        if self.immediate_flush:
            print(f"{self._move_cursor(x, y)}{text}", end='', flush=True)
        else:
            self.frame_buffer.append((x, y, text))

    def colored_text(self, text: str, color: Color) -> str:
        """Returns text with ANSI color codes.

        Args:
            text: Text to colorize
            color: Color name (e.g. RED, GREEN, BLUE)

        Returns:
            Text with appropriate coloring
        """

        # Clean any color codes
        clean_text = self.ANSI_PATTERN.sub('', text)

        return f"{color.value}{clean_text}{Color.RESET.value}"

    def center_text(self, text: str, y: Optional[int] = None) -> None:
        """Print text centered on the given row.

        Args:
            text: Text to center
            y: Row position (1-indexed). If None, centers vertically
        """
        if y is None:
            y = self.height // 2

        visible_length = len(self.ANSI_PATTERN.sub('', text))
        x = (self.width - visible_length) // 2 + 1
        self.print_at(max(1, x), y, text)

    def flush(self) -> None:
        if not self.frame_buffer:
            return

        output = ''.join(f'{self._move_cursor(x, y)}{text}' for x, y, text in self.frame_buffer)
        print(output, end='', flush=True)
        self.frame_buffer.clear()
