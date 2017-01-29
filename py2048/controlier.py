# -*- coding:utf-8 -*-
from cocos.layer import Layer
from pyglet.window import key

from py2048.model import Direction


class Dungeon(Layer):
    is_event_handler = True

    def __init__(self, model):
        super().__init__()
        self.model = model

    def on_key_press(self, k, _):
        if k == key.UP:
            direction = Direction.UP
        elif k == key.DOWN:
            direction = Direction.DOWN
        elif k == key.LEFT:
            direction = Direction.LEFT
        elif k == key.RIGHT:
            direction = Direction.RIGHT
        else:
            direction = None

        if direction is not None:
            self.model.step(direction)
