import shutil
from typing import List, Tuple

class Display:
    # ANSI escape codes
    CLEAR_SCREEN = '\033[2J'
    CURSOR_HOME = '\033[H'

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

    def flush(self) -> None:
        if not self.frame_buffer:
            return

        output = ''.join(f'{self._move_cursor(x, y)}{text}' for x, y, text in self.frame_buffer)
        print(output, end='', flush=True)
        self.frame_buffer.clear()
