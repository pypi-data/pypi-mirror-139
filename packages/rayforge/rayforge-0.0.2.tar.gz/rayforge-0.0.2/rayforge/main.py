from pyray import *

import os

from rayforge.text import Text
from rayforge.input import Input

import rayforge.color as color
import rayforge.math as math

import __main__

class RayForge:
    def __init__(self, width = 1200, height = 600, fps = 60, background_color = color.Color(20, 20, 20), camera_position = math.Vector3(0, 0, 0), camera_target = math.Vector3(0, 0, 0), camera_up = math.Vector3(0, 1, 0), camera_fovy = 45, camera_projection = CAMERA_PERSPECTIVE):
        self.fps = fps
        self.width = width
        self.height = height
        self.background_color = background_color

        init_window(self.width, self.height, "RayForge")
        set_target_fps(self.fps)

        self.dt = get_frame_time()

        self.path = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(self.path, "./assets/icon/icon.png")
        icon = load_image(icon)
        set_window_icon(icon)

        self.destroyed = False
        self.functions = {}
        self.objects = []

        self.input = Input()
        self.camera = Camera3D(camera_position.get(), camera_target.get(), camera_up.get(), camera_fovy, camera_projection)

        self.keys = {
            "ESCAPE" : KEY_ESCAPE, "SPACE" : KEY_SPACE,
            "TAB" : KEY_TAB, "CAPSLOCK" : KEY_CAPS_LOCK,

            "UP" : KEY_UP, "DOWN" : KEY_DOWN,
            "LEFT" : KEY_LEFT, "RIGHT" : KEY_RIGHT,

            "A" : KEY_A, "B" : KEY_B, "C" : KEY_C,
            "D" : KEY_D, "E" : KEY_E, "F" : KEY_F,
            "G" : KEY_G, "H" : KEY_H, "I" : KEY_I,
            "J" : KEY_J, "K" : KEY_K, "L" : KEY_L,
            "M" : KEY_M, "N" : KEY_N, "O" : KEY_O,
            "P" : KEY_P, "Q" : KEY_Q, "R" : KEY_R,
            "S" : KEY_S, "T" : KEY_T, "U" : KEY_U,
            "V" : KEY_V, "W" : KEY_W, "X" : KEY_X,
            "Y" : KEY_Y, "Z" : KEY_Z,

            "0" : KEY_ZERO, "1" : KEY_ONE,"2" : KEY_TWO,
            "3" : KEY_THREE, "4" : KEY_FOUR, "5" : KEY_FIVE,
            "6" : KEY_SIX, "7" : KEY_SEVEN, "8" : KEY_EIGHT,
            "9" : KEY_NINE,

            "NUM0" : KEY_KP_0, "NUM1" : KEY_KP_1,"NUM2" : KEY_KP_2,
            "NUM3" : KEY_KP_3, "NUM4" : KEY_KP_4, "NUM5" : KEY_KP_5,
            "NUM6" : KEY_KP_6, "NUM7" : KEY_KP_7, "NUM8" : KEY_KP_8,
            "NUM9" : KEY_KP_9, "NUMLOCK" : KEY_NUM_LOCK,

            "F1" : KEY_F1, "F2" : KEY_F2, "F3" : KEY_F3,
            "F4" : KEY_F4, "F5" : KEY_F5, "F6" : KEY_F6,
            "F7" : KEY_F7, "F8" : KEY_F8, "F9" : KEY_F9,
            "F10" : KEY_F10, "F11" : KEY_F11, "F12" : KEY_F12,

            "LCTRL" : KEY_LEFT_CONTROL, "RCTRL" : KEY_RIGHT_CONTROL,
            "LSHIFT" : KEY_LEFT_SHIFT, "RSHIFT" : KEY_RIGHT_SHIFT,
            "LALT" : KEY_LEFT_ALT, "RALT" : KEY_RIGHT_ALT,

            "ENTER" : KEY_ENTER, "NUMENTER" : KEY_KP_ENTER,
            "BACKSPACE" : KEY_BACKSPACE,

            "SLASH" : KEY_SLASH, "BACKSLASH" : KEY_BACKSLASH,

            "PLUS": KEY_KP_ADD, "MINUS" : KEY_KP_SUBTRACT,
            "MULTIPLY" : KEY_KP_MULTIPLY, "DIVIDE" : KEY_KP_DIVIDE,

            "INSERT" : KEY_INSERT, "DELETE" : KEY_DELETE,
            "HOME" : KEY_HOME, "END" : KEY_END,
            "PAGEUP": KEY_PAGE_UP, "PAGEDOWN": KEY_PAGE_DOWN,
        }

        print("INFO: RAYFORGE: Initialized successfully")

    def run(self):
        while not window_should_close():
            self.dt = get_frame_time()

            update_camera(self.camera)

            if "update" in self.functions:
                self.functions["update"]()

            for object in self.objects:
                if not object.destroyed:
                    for script in object.scripts:
                        if hasattr(script, "update") and script.update:
                            script.update(object)

                    if hasattr(object, "update") and object.update:
                        object.update()

            begin_drawing()
            clear_background(self.background_color.get())

            if "draw" in self.functions:
                self.functions["draw"](False)
            
            for i in self.objects:
                if not i.is_3d:
                    i.draw()

            begin_mode_3d(self.camera)

            if "draw" in self.functions:
                self.functions["draw"](True)
            
            for i in self.objects:
                if i.is_3d:
                    i.draw()
            
            end_mode_3d()
            end_drawing()

        if "on_quit" in self.functions:
            self.functions["on_quit"]()

        close_window()

    def event(self, func):
        self.functions[func.__name__] = func

    def set_background_color(self, color):
        self.background_color = color

    def set_fps(self, fps):
        self.fps = fps
        set_target_fps(self.fps)

    def get_fps(self):
        return get_fps() / 1

    def set_window_pos(self, arg1, arg2 = None):
        if isinstance(arg1, Vector2):
            set_window_position(arg1.x, arg1.y)

        else:
            set_window_position(arg1, arg2)

    def set_window_size(self, width, height):
        set_window_size(width, height)

    def get_window_size(self):
        return get_screen_width(), get_screen_height()

    def set_window_width(self, width):
        set_window_size(width, get_screen_height())

    def set_window_height(self, height):
        set_window_size(get_screen_width(), height)

    def get_window_width(self):
        return get_screen_width()

    def get_window_height(self):
        return get_screen_height()

    def set_camera_position(self, position):
        self.camera.position = Vector3(position.x, position.y, position.z)

    def get_camera_position(self):
        return math.Vector3(self.camera.position.x, self.camera.position.y, self.camera.position.z)

    def set_camera_target(self, target):
        self.camera.position = Vector3(target.x, target.y, target.z)

    def get_camera_target(self):
        return math.Vector3(self.camera.target.x, self.camera.target.y, self.camera.target.z)

    def set_camera_up(self, up):
        self.camera.up = Vector3(up.x, up.y, up.z)

    def get_camera_up(self):
        return math.Vector3(self.camera.up.x, self.camera.up.y, self.camera.up.z)

    def set_camera_fovy(self, fovy):
        self.camera.fovy = fovy

    def get_camera_fovy(self):
        return self.camera.fovy

    def set_camera_projection(self, projection):
        self.camera.projection = projection

    def get_camera_projection(self):
        return self.camera.projection
    
    def destroy(self, entity = None):
        if entity == None:
            if "on_quit" in self.functions:
                self.functions["on_quit"]()

            close_window()

        else:
            entity.destroy()