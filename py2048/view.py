# -*- coding:utf-8 -*-
from cocos.sprite import Sprite
from cocos.layer import Layer
from pyglet.gl import glPushMatrix, glPopMatrix

SQUARE_SIZE = 0

IMAGES = {
    None: 'sprites/None.png',
    2: 'sprites/2.png',
    4: 'sprites/4.png',
    8: 'sprites/8.png',
    16: 'sprites/16.png',
    32: 'sprites/32.png',
    64: 'sprites/64.png',
    128: 'sprites/128.png',
    256: 'sprites/256.png',
    512: 'sprites/512.png',
    1024: 'sprites/1024.png',
    2048: 'sprites/2048.png',
    4096: 'sprites/4096.png'
}


class GameView(Layer):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.sprites = [Sprite(IMAGES[None]) for _ in range(16)]

    def draw(self, *args, **kwargs):
        glPushMatrix()
        self.transform()
        old = self.sprites
        self.sprites = [
            Sprite(IMAGES[sell], (50 * (i % 4), 50 * (i // 4)))
            for i, sell in enumerate(self.model.sells)
        ]
        for sp in self.sprites:
            sp.draw()

        for sp in old:
            sp.visible = False

        glPopMatrix()
