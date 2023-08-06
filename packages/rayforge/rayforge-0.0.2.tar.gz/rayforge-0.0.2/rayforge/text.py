from pyray import *

from rayforge.color import Color

class Text:
    def __init__(self, window, text, x = 0, y = 0, is_3d = False, font_size = 24, color = Color(240, 240, 240), add_to_objects = True):
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.is_3d = is_3d
        self.font_size = font_size
        self.color = color
        self.add_to_objects = add_to_objects

        self.destroyed = False
        self.visible = True

        self.scripts = []

        if self.add_to_objects:
            self.window.objects.append(self)

    def draw(self):
        if not self.destroyed:
            if self.visible:
                draw_text(self.text, self.x, self.y, self.font_size, self.color.get())

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_font_size(self, font_size):
        self.font_size = font_size

    def get_font_size(self):
        return self.font_size

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_visible(self, visible):
        self.visible = visible

    def get_visible(self):
        return self.visible

    def destroy(self):
        self.destroyed = True

        if self.add_to_objects:
            try:
                self.window.objects.pop(self.window.objects.index(self))

            except:
                pass

    def add_script(self, script):
        self.scripts.append(script)

    def remove_script(self, script):
        self.scripts.pop(self.scripts.index(script))