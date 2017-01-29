# -*- coding:utf-8 -*-
import logging
from random import choice
from enum import Enum, auto

import cocos
from cocos.scenes.transitions import FadeTransition, FadeBLTransition
from cocos.text import Label

from pyglet.window import key
from PIL import Image, ImageDraw, ImageFont

K = 50
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.debug('test')


def get_sprite(n, size, color):
    """
    >>> im = get_sprite(4, 100, 100)
    >>> im.show()
    """
    im = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype("arial.ttf", size=60)
    draw.rectangle([0, 0, size, size], fill=color)
    # TODO improve text drawing
    draw.text((10, 10), str(n), fnt=fnt, fill=(255, 255, 255, 128))
    return im


class BackGround(cocos.layer.ColorLayer):
    def __init__(self, r=0, g=0, b=0, a=255):
        super().__init__(r, g, b, a)


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__('asdf')
        l = [cocos.menu.MenuItem('Start', self.start),
             cocos.menu.MenuItem('Options', self.foo),
             cocos.menu.MenuItem('Quit', self.foo)]
        self.create_menu(l, cocos.menu.zoom_in(), cocos.menu.zoom_out())

    def foo(self):
        LOGGER.debug('foo')

    def start(self):
        Master.play()


class MainScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__(BackGround(0, 50), MainMenu())


class GameLayer(cocos.layer.Layer):
    class Direction(Enum):
        UP = (0, 1)
        DOWN = (0, -1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)

    new_sell = (2, 4)

    def __init__(self, n):
        super().__init__()
        self._n = n
        self._sells = [None] * (n ** 2)
        self.add_more()
        self.add_more()

    def step(self, direction):
        self.move(direction)
        if self.game_over():
            self._end()
        else:
            self.add_more()

    def move(self, direction):
        if direction == self.Direction.UP:
            slices = self.columns(self._n)
        elif direction == self.Direction.DOWN:
            slices = self.columns(self._n, True)
        elif direction == self.Direction.LEFT:
            slices = self.rows(self._n)
        elif direction == self.Direction.RIGHT:
            slices = self.rows(self._n, True)
        else:
            raise Exception('Bad direction')

        for slice_ in slices:
            self._sells[slice_] = self.tk(self._sells[slice_])

    @staticmethod
    def tk(arr):
        n = len(arr)
        arr = [v for v in arr if v]
        i = 0
        while i < len(arr) - 1:
            if arr[i] == arr[i + 1]:
                arr[i:i + 2] = [arr[i] * 2]
            i += 1
        arr += [None] * (n - len(arr))
        return arr

    @staticmethod
    def columns(n, reverse=False):
        len_arr = n ** 2
        for i in range(n):
            if reverse:
                yield slice(len_arr - i - 1, None, -n)
            else:
                yield slice(i, len_arr, n)

    @staticmethod
    def rows(n, reverse=False):
        for i in range(n):
            if reverse:
                stop = i * n - 1
                if stop < 0:
                    stop = None
                yield slice(i * n + (n - 1), stop, -1)
            else:
                start = i * n
                yield slice(start, start + n)

    def add_more(self):
        free_sells = [num for num, sell in enumerate(self._sells)
                      if sell is None]
        self._sells[choice(free_sells)] = choice(self.new_sell)

    def game_over(self):
        return all(self._sells)

    def _end(self):
        print('Game over')

    def __str__(self):
        fmt = '{!s:<5}' * self._n
        return '\n'.join(fmt.format(*self._sells[slice_]) for slice_ in self.rows(self._n))


class GameScene(cocos.scene.Scene):
    def __init__(self, n):
        super().__init__(BackGround(50), GameLayer(n))


class Master:
    game = None

    @staticmethod
    def run():
        cocos.director.director.init(resizable=False, width=500, height=500)
        cocos.director.director.run(MainScene())

    @staticmethod
    def play():
        cocos.director.director.replace(FadeTransition(GameScene(5)))


if __name__ == '__main__':
    Master.run()
