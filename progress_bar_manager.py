from display import Display
from typing import Tuple

class ProgressBarManager():
    def __init__(self, display: Display, position: Tuple[int, int], size: Tuple[int, int]) -> None:
        self._display = display
        self._position = position
        self._size = size
        self._progress = 0.0

    def position(self) -> Tuple[int, int]:
        return self._position

    def size(self) -> Tuple[int, int]:
        return self._size

    def width(self) -> int:
        return self.size()[0]

    def height(self) -> int:
        return self.size()[1]

    def x(self) -> int:
        return self.position()[0]

    def y(self) -> int:
        return self.position()[1]

    def set_progress(self, percent: float) -> None:
        self._progress = percent

    def progress(self) -> float:
        return self._progress

    def draw(self) -> None:
        progress_line_y = int(self.y() + (self.height() / 2))
        progress_line_x_start = self.x()
        progress_line_x_end = self.x() + self.width()
        
        # Draw the bar
        self._display.draw_line((progress_line_x_start, progress_line_y), (progress_line_x_end, progress_line_y))

        # Draw the beginning and the end lines
        start_line_x = self.x()
        end_line_x = self.x() + self.width()
        line_y_start = self.y()
        line_y_end = self.y() + self.height()
        self._display.draw_line((start_line_x, line_y_start), (start_line_x, line_y_end))
        self._display.draw_line((end_line_x, line_y_start), (end_line_x, line_y_end))

        # Draw current progress
        progress_start_x = start_line_x
        progress_end_x = int(start_line_x + ((end_line_x - start_line_x) * self.progress()))
        progress_thickness = int(self.height() * 0.2)
        progress_top_y = progress_line_y - progress_thickness
        progress_bottom_y = progress_line_y + progress_thickness

        self._display.draw_rectangle((progress_start_x, progress_top_y), (progress_end_x, progress_bottom_y))