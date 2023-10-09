#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File       : util.py

@Author     : hsn

@Date       : 10/9/23 8:36 PM
"""
import random
from pathlib import Path

import pygame
from pygame import Surface


def color_func(num):
    return (255 - num * 56) % 255, (255 - num * 31) % 255, (255 - num * 23) % 255


class AnimUpdater:
    def __init__(self, callback, screen: Surface, total: int):
        self.now = 0
        self.total = total
        self.anim = callback
        self.screen = screen

    def update(self):
        self.anim(self.screen, self.now, self.total)
        return self.total - self.seek(1, 1)

    def seek(self, i: int, mode: int = 0):
        if mode == 0:
            self.now = i
        elif mode == 1:
            self.now += i
        elif mode == 2:
            self.now = self.total - i
        if self.now < 0 or self.now > self.total:
            raise ValueError('now out of range')
        return self.now

    def __next__(self):
        self.update()


class Block:
    def __init__(self, d_rect: dict = None):
        self.num = random.randint(1, 2)
        while True:
            x, y = random.randint(0, 3), random.randint(0, 3)
            if (x, y) not in d_rect:
                break
        self.x, self.y = x, y
        self._move = None
        self._on_load = True

    def update(self, screen: Surface):
        if not self._on_load:
            font = pygame.font.Font((Path('assets') / 'font' / 'unifont-15.1.02.otf'), 100)
            text = font.render(str(pow(2, self.num)), True, (0, 0, 0))
            tx, ty = text.get_size()

            # print in screen
            pygame.draw.rect(screen, color_func(self.num), (self.x * 200 + 20, self.y * 200 + 20, 180, 180), 0,
                             border_radius=5)
            screen.blit(text, (self.x * 200 + 110 - tx // 2, self.y * 200 + 110 - ty // 2))

            # return animation
        return AnimUpdater(self.anim, screen, 10)

    def anim(self, screen: Surface, now: int, total: int):

        if self._move:
            mv_x, mv_y = self._move
            font = pygame.font.Font((Path('assets') / 'font' / 'unifont-15.1.02.otf'), 100)
            text = font.render(str(pow(2, self.num)), True, (0, 0, 0))
            tx, ty = text.get_size()

            def anim_func(x):
                return pow(2, x) - 1

            pygame.draw.rect(screen, color_func(self.num),
                             ((self.x - mv_x) * 200 + mv_x * 200 * anim_func(now / total) + 20,
                              (self.y - mv_y) * 200 + mv_y * 200 * anim_func(now / total) + 20,
                              180, 180),
                             0,
                             border_radius=5)
            screen.blit(text, ((self.x - mv_x) * 200 + mv_x * 200 * anim_func(now / total) + 110 - tx // 2,
                               (self.y - mv_y) * 200 + mv_y * 200 * anim_func(now / total) + 110 - ty // 2))
            if now == total - 1:
                self._move = None
        else:
            self.update(screen)
        if self._on_load and now == total - 1:
            self._on_load = False
            self.update(screen)

    def move(self, v_x, v_y):
        self._move = (v_x, v_y)
        self.x += v_x
        self.y += v_y

    def move_to(self, x, y):
        if self._move:
            mv_x, mv_y = self._move
        else:
            mv_x, mv_y = 0, 0
        self._move = mv_x + x - self.x, mv_y + y - self.y
        self.x, self.y = x, y
