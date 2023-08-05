import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import time
import pygame
import sys

from aerforge.input import *
from aerforge.error import *
from aerforge.color import *
from aerforge.shape import *
from aerforge.entity import *
from aerforge.sprite import *
from aerforge.logo import *

import __main__

def init():
    pygame.init()

class Forge:
    def __init__(self, width = 1200, height = 600, background_color = Color(20, 20, 20), fullscreen = False, frame = True, doublebuf = False, opengl = False, fade = True, logo = True, fps = 60):
        self.width = width
        self.height = height
        self.fps = fps

        self.background_color = background_color

        pygame.init()

        self.destroyed = False

        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.dt = 0

        self.fullscreen = fullscreen
        self.frame = frame
        self.opengl = opengl
        self.doublebuf = doublebuf

        self.path = os.path.dirname(os.path.abspath(__file__))

        try:
            pygame.display.set_icon(pygame.image.load(os.path.join(self.path, "./assets/icon/icon.png")))

        except:
            pygame.display.set_icon(pygame.image.load("icon.png"))

        pygame.display.set_caption("Forge")

        self.build_window()

        self.window.fill(self.background_color.get())

        self.logo = Logo(self)

        if not logo:
            self.logo.logo.destroy()

        if not fade:
            self.logo.fade.destroy()

        self.input = Input()

        self.keys = {
            "ESCAPE" : pygame.K_ESCAPE,

            "UP" : pygame.K_UP, "DOWN" : pygame.K_DOWN,
            "LEFT" : pygame.K_LEFT, "RIGHT" : pygame.K_RIGHT,

            "A" : pygame.K_a, "B" : pygame.K_b, "C" : pygame.K_c,
            "D" : pygame.K_d, "E" : pygame.K_e, "F" : pygame.K_f,
            "G" : pygame.K_g, "H" : pygame.K_h, "I" : pygame.K_i,
            "J" : pygame.K_j, "K" : pygame.K_k, "L" : pygame.K_l,
            "M" : pygame.K_m, "N" : pygame.K_n, "O" : pygame.K_o,
            "P" : pygame.K_p, "Q" : pygame.K_q, "R" : pygame.K_r,
            "S" : pygame.K_s, "T" : pygame.K_t, "U" : pygame.K_u,
            "V" : pygame.K_v, "W" : pygame.K_w, "X" : pygame.K_x,
            "Y" : pygame.K_y, "Z" : pygame.K_z,
    
            "0" : pygame.K_0, "1" : pygame.K_1, "2" : pygame.K_2, 
            "3" : pygame.K_3, "4" : pygame.K_4, "5" : pygame.K_5,
            "6" : pygame.K_6, "7" : pygame.K_7, "8" : pygame.K_8,
            "9" : pygame.K_9,

            "F1" : pygame.K_F1, "F2" : pygame.K_F2, "F3" : pygame.K_F3,
            "F4" : pygame.K_F4, "F5" : pygame.K_F5, "F6" : pygame.K_F6,
            "F7" : pygame.K_F7, "F8" : pygame.K_F8, "F9" : pygame.K_F9,
            "F10" : pygame.K_F10, "F11" : pygame.K_F11, "F12" : pygame.K_F12,

            "LCTRL" : pygame.K_LCTRL, "RCTRL" : pygame.K_RCTRL,
            "LSHIFT" : pygame.K_LSHIFT, "RSHIFT" : pygame.K_RSHIFT,
            "LALT" : pygame.K_LALT, "RALT" : pygame.K_RALT,

            "TAB" : pygame.K_TAB, "CAPSLOCK" : pygame.K_CAPSLOCK,

            "HOME" : pygame.K_HOME, "END" : pygame.K_END,
            "INSERT" : pygame.K_INSERT, "DELETE" : pygame.K_DELETE, 

            "RETURN" : pygame.K_RETURN, "BACKSPACE" : pygame.K_BACKSPACE, 
            "SPACE" : pygame.K_SPACE, 

            "PLUS" : pygame.K_PLUS, "MINUS" : pygame.K_MINUS, 
            "SLASH" : pygame.K_SLASH, "BACKSLASH" : pygame.K_BACKSLASH,
            "ASTERISK" : pygame.K_ASTERISK, 
        }

        self.buttons = {
            "LEFT" : 0, "MIDDLE" : 1, "RIGHT" : 2,
        }

        self.objects = []
        self.functions = {}

        self.dt = 0
        self.clock.tick(self.fps)

    def event(self, func):
        self.functions[func.__name__] = func

    def build_window(self):
        if self.fullscreen:
            if self.opengl:
                self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)
            
            else:
                if self.doublebuf:
                    self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF)

                else:
                    self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

        else:
            if self.opengl:
                if not self.frame:
                    self.window = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.OPENGL, pygame.NOFRAME)

                else:
                    self.window = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.OPENGL)

            else:
                if self.doublebuf:
                    if not self.frame:
                        self.window = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF, pygame.NOFRAME)

                    else:
                        self.window = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)

                else:
                    if not self.frame:
                        self.window = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)

                    else:
                        self.window = pygame.display.set_mode((self.width, self.height))

    def run(self):
        key = ""

        while True:
            self.dt = self.clock.tick(self.fps) / 1000.0

            if "update" in self.functions:
                self.functions["update"]()

            if "draw" in self.functions:
                self.functions["draw"]()

            for object in self.objects:
                if not object.destroyed:
                    if hasattr(object, "visible"):
                        if object.visible:
                            object.draw()

                    for script in object.scripts:
                        if hasattr(script, "update") and script.update:
                            script.update(object)

                        if hasattr(script, "input") and object.input:
                            if self.input.key_pressed():
                                if self.input.get_pressed() != "":
                                    key = self.input.get_pressed()
                                    script.input(key)

                    if hasattr(object, "update") and object.update:
                        object.update()

                    if hasattr(object, "input") and object.input:
                        if self.input.key_pressed():
                            if self.input.get_pressed() != "":
                                key = self.input.get_pressed()
                                object.input(key)

            if not self.logo.destroyed:
                self.logo.update()

            pygame.display.flip()

            self.input.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.destroyed = True

                if event.type == pygame.KEYDOWN:
                    self.input.update(event)

            if self.input.key_pressed():
                if "input" in self.functions:
                    if self.input.get_pressed() != "":
                        key = self.input.get_pressed()
                        self.functions["input"](key)

            self.window.fill(self.background_color.get())

            if self.destroyed:
                if "on_quit" in self.functions:
                    self.functions["on_quit"]()

                pygame.quit()
                sys.exit()

    def destroy(self, entity = None):
        if entity == None:
            self.destroyed = True

        else:
            entity.destroy()

    def get_fps(self):
        return self.clock.get_fps()

    def destroyall(self):
        for i in self.objects:
            i.destroy()

    def minimize(self):
        pygame.display.iconify()

    def get_hwnd(self):
        return pygame.display.get_wm_info()["window"]

    def get_fonts(self):
        return pygame.font.get_fonts()

    def draw(self, shape = Rect, color = Color(240, 240, 240), fill = True, x = 0, y = 0, width = 200, height = 200, points = []):
        fill = not fill
        
        if shape == Rect:
            pygame.draw.rect(self.window, color.get(), (x, y, width, height), fill)

        elif shape == Circle:
            pygame.draw.ellipse(self.window, color.get(), (x, y, width, height), fill)

        elif shape == Polygon:
            pygame.draw.polygon(self.window, color.get(), points, fill)

        elif shape == Line:
            for point in points:
                pygame.draw.aaline(self.window, color.get(), point[0], point[1])

        else:
            raise ForgeError("Invalid shape")