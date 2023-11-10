#!/usr/bin/python

import sys
import csv

import pygame
import random

from gresource import *
from board import *

CURSOR_MOVE_LEFT = 1
CURSOR_MOVE_DOWN = 2
CURSOR_MOVE_RIGHT = 4
CURSOR_MOVE_UP = 8

class cursor_object :
    def __init__(self, map) :
        self.x = 0
        self.y = 0
        self.map = map

        self.rows, self.cols = self.map.get_size()

    def get_cur_pos(self) :
        return [self.x, self.y]

    def set_pos(self, x, y) :
        self.x = x
        self.y = y

    def move(self, direction) :
        if direction == CURSOR_MOVE_UP:
            self.y += 1
            if self.y >= self.rows :
                self.y = self.rows - 1
        elif direction == CURSOR_MOVE_DOWN :
            self.y -= 1
            if self.y < 0 :
                self.y = 0
        elif direction == CURSOR_MOVE_LEFT :
            self.x -= 1
            if self.x < 0 :
                self.x = 0
        elif direction == CURSOR_MOVE_RIGHT :
            self.x += 1
            if self.x >= self.cols  :
                self.x = self.cols  - 1         

    def draw_rect(self, color, width) :
        cursor_rect = self.map.get_map_rect(self.x, self.y)
        pygame.draw.rect(gctrl.surface, color, cursor_rect, width, 3)

    def draw_circle(self, color) :
        cursor_rect = self.map.get_map_rect(self.x, self.y)
        pygame.draw.circle(gctrl.surface, color, cursor_rect.center, 3, 2)

if __name__ == '__main__' :
    print('cursor object')