
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from typing import Text, Tuple
from enum import Enum

class TextRow(Enum):
    FIRST = 1,
    SECOND = 2,
    THIRD = 3,
    FOURTH = 4,
    TOPBAR = 5,

class Display:
    def __init__(self, width: int, height: int, address: int, margins: Tuple[int, int] = (3, 3)) -> None:
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._oled = adafruit_ssd1306.SSD1306_I2C(width, height, self._i2c, addr=address)
        self._width = width
        self._height = height
        self._address = address
        self._image = Image.new('1', (self._width, self._height))
        self._draw = ImageDraw.Draw(self._image)
        self._font = ImageFont.load_default()
        self._char_width, self._char_height = self._font.getsize('█'.encode('CP437'))

        self._text_positions = {
            TextRow.FIRST: self.topbar_height(),
            TextRow.SECOND: self.topbar_height() + self.char_height(),
            TextRow.THIRD: self.topbar_height() + (self.char_height() * 2),
            TextRow.FOURTH: self.topbar_height() + (self.char_height() * 3),
            TextRow.TOPBAR: 0
        }

        self._oled.fill(0)
        self._oled.show()

    def char_height(self) -> int:
        return self._char_height

    def char_width(self) -> int:
        return self._char_width

    def text_line_capacity(self) -> int:
        return self.width() / self.char_width()
    
    def text_lines_amount(self) -> int:
        return self.height() / self.char_height()
    
    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height
    
    def address(self) -> int:
        return self._address

    def topbar_height(self) -> int:
        return 16

    def row_position(self, row: TextRow) -> int:
        return self._text_positions[row]
    
    def show(self) -> None:
        self._oled.image(self._image)
        self._oled.show()

    def clear(self) -> None:
        self._draw.rectangle([(0, 0), (self.width(), self.height())], fill=0)

    def is_text_in_bounds(self, text: str, x: int, y: int) -> Tuple[bool, bool]:
        text_width, text_height = self._font.getsize(text)
        width_ok = True
        height_ok = True
        
        if text_width > self.width():
            print(f'WARNING: Text "{text}" is too wide - it has {text_width} pixels, but the screen has only {self.width()} pixels')
            width_ok = False
        elif (text_width + x) > self.width():
            print(f'WARNING: Text "{text}" will be drawn out of screen bounds - it\'s {text_width} pixels wide, and will be drawn at X = {x}, but the screen has only {self.width()} pixels')
            width_ok = False
        
        if (text_height + y) > self.height():
            print(f'WARNING: Text "{text}" will be drawn out of screen bounds - it\'s {text_height} pixels long, and will be drawn at Y = {y}, but the screen has only {self.height()} pixels')
            height_ok = False

        return (width_ok, height_ok)

    def is_text_in_row_bounds(self, text: str, row: TextRow) -> bool:
        return self.is_text_in_bounds(text, 0, self.row_position(row))[0]

    def draw_text(self, text: str, x: int, y: int) -> None:
        self._draw.text(
            (x, y),
            text,
            font=self._font,
            fill=255
        )

    def draw_text_in_row(self, text: str, row: TextRow) -> None:
        self.draw_text(text, 0, self.row_position(row))

    def draw_line(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self._draw.line([start, end], fill=255)

    def draw_rectangle(self, start: Tuple[int, int], end: Tuple[int, int], fill: bool = True) -> None:
        if fill:
            self._draw.rectangle([start, end], fill=255)
        else:
            self._draw.rectangle([start, end], outline=255)