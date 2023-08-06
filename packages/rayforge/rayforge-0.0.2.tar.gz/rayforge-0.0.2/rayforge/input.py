from pyray import *

class Input:
    def __init__(self):
        pass

    def key_pressed(self, key):
        return is_key_down(key)