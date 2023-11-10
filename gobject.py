#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gresource import *

class game_object :
    global gctrl

    def __init__(self, x, y, resource_path) :
        if resource_path != None :
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width() / 2
            self.height = self.object.get_height() / 2
            self.object = pygame.transform.scale(self.object, (self.width, self.height))

        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.set_position(x, y)

        self.life_count = 1

    def set_position(self, x, y) : 
        self.x = x
        self.y = y
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def move(self, del_x, del_y) :
        self.x += del_x
        self.y += del_y

        if self.y < 0 :
            self.y = 0
        elif self.y > (gctrl.height - self.height) :
            self.y = (gctrl.height - self.height)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gctrl.surface.blit(self.object, (self.x, self.y))

    def draw(self, rect) :
        if self.object != None :
            gctrl.surface.blit(self.object, rect)

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= gctrl.width :
            return True
        else :
            return False

    def is_life(self) :
        if self.life_count > 0 :
            return True
        else :
            return False
    
    def set_life_count(self, count) :
        self.life_count = count
        if self.life_count > 0 :
            self.life = True

    def get_life_count(self) :
        return self.life_count
    
    def kill_life(self) :
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy_item) :
        if self.object != None and enemy_item.object != None :
            if self.ex > enemy_item.x :
                if (self.y > enemy_item.y and self.y < enemy_item.ey) or (self.ey > enemy_item.y and self.ey < enemy_item.ey) :
                    return True
        return False

if __name__ == '__main__' :
    print('game object')