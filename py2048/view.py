# -*- coding:utf-8 -*-
from cocos.layer import Layer
from pyglet.gl import glPushMatrix, glPopMatrix


class GameView(Layer):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def draw(self, *args, **kwargs):
        glPushMatrix()
        self.transform()



        glPopMatrix()
