from pyray import *

from rayforge.color import Color
from rayforge.text import Text

class FpsCounter(Text):
    def __init__(self, window, x = 10, y = 10, font_size = 24, color = Color(240, 240, 240)):
        super().__init__(
            window = window,
            text = "",
            x = x,
            y = y,
            font_size = font_size,
            color = color
        )

    def update(self):
        self.text = str(self.window.get_fps() / 1)