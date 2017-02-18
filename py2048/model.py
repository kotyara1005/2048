# -*- coding:utf-8 -*-
from random import choice
from enum import Enum


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameModel:
    new_sell = (2, 4)

    def __init__(self, n=4):
        super().__init__()
        self._n = n
        self._sells = [None] * (n ** 2)
        self.add_more()
        self.add_more()

    @property
    def n(self):
        return self._n

    @property
    def sells(self):
        return tuple(self._sells)

    def step(self, direction):
        self.move(direction)
        if self.game_over():
            self.end()
        else:
            self.add_more()

    def move(self, direction):
        if direction == Direction.UP:
            slices = self.columns(self._n)
        elif direction == Direction.DOWN:
            slices = self.columns(self._n, True)
        elif direction == Direction.LEFT:
            slices = self.rows(self._n)
        elif direction == Direction.RIGHT:
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

    def end(self):
        print('Game over')

    def __str__(self):
        fmt = '{!s:<5}' * self._n
        return '\n'.join(fmt.format(*self._sells[slice_])
                         for slice_ in self.rows(self._n))
