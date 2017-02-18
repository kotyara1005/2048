# -*- coding:utf-8 -*-
import logging
from random import choice
from enum import Enum, auto

import cocos
from cocos.scenes.transitions import FadeTransition, FadeBLTransition
from cocos.text import Label

from pyglet.window import key
from PIL import Image, ImageDraw, ImageFont

from py2048.controlier import GameController
from py2048.view import GameView
from py2048.model import GameModel

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


class GameScene(cocos.scene.Scene):
    def __init__(self):
        model = GameModel()
        super().__init__(BackGround(50), GameView(model), GameController(model))


class Master:
    game = None

    @staticmethod
    def run():
        cocos.director.director.init(resizable=False, width=500, height=500)
        cocos.director.director.run(MainScene())

    @staticmethod
    def play():
        cocos.director.director.replace(FadeTransition(GameScene()))


if __name__ == '__main__':
    Master.run()
