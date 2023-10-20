#!/usr/bin/python

import sys
import csv

import pygame
import random

from gresource import *
from gobject import *

MAX_ROWS = 10
MAX_COLS = 8

MAP_XOFFSET = 10
MAP_YOFFSET = 30

MAP_WIDTH = 30
MAP_HEIGHT = 30

BOARD_LEFT = 1
BOARD_RIGHT = 2
BOARD_UP = 4
BOARD_DOWN = 8

check_dirs = [BOARD_LEFT, BOARD_RIGHT, BOARD_UP, BOARD_DOWN]

SAME_THRESHOLD = 3

SOUND = True

board_dict = {
    1 : ['id_bear'],
    2 : ['id_cat'],
    3 : ['id_cow'],
    4 : ['id_fox'],  
    5 : ['id_koala'],
    6 : ['id_koki'],
    7 : ['id_little_lion'],    
}

debug_ctrl = {
    'check_area' : True,
    'checks_values' : True,
    'clear' : True,
    'remove' : True,
    'move_down' : True,
    'do_combo' : True 
}

class game_board :
    def __init__(self, rows, cols) :
        self.map = []

        self.rows = rows
        self.cols = cols
        
        for x in range(cols) :
            self.map.append([])
            for y in range(rows) :
                self.map[x].append(0)

        self.object = {}
        self.x_offset = MAP_XOFFSET
        self.y_offset = MAP_YOFFSET
        self.obj_width = MAP_WIDTH
        self.obj_height = MAP_HEIGHT

        self.remove_list = []

        self.combo = []
        self.combo_count = 0

        # effect resource
        self.effect_boot = pygame.image.load(get_img_resource('id_boom'))

        # sound resource
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))

    def add_objet(self, key, tile_object) :
        self.object[key] = tile_object
        self.obj_width = tile_object.width 
        self.obj_height = tile_object.height

    def get_size(self) :
        return self.rows, self.cols

    def get_padsize(self) :
        pad_width = 2 * self.x_offset + self.cols * self.obj_width 
        pad_height = 2 * self.y_offset + self.rows * self.obj_height
        return (pad_width, pad_height) 

    def get_pos(self, screen_xy) :
        for y in range(self.rows) :
            for x in range(self.cols) :
                rect = self.get_map_rect(x, y)
                if screen_xy[0] > rect.left and screen_xy[0] < rect.right :
                    if screen_xy[1] > rect.top and screen_xy[1] < rect.bottom :      
                        return (x, y)
                    
        return (None, None)

    def get_map_rect(self, x, y) :
        rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width , self.obj_height)

        # map[0][0] is left and bottom
        rect.x += x * self.obj_width
        rect.y += ((self.rows - 1) - y) * self.obj_height  
        return rect        

    def shuffle(self) :
        for x in range(self.cols) :
            for y in range(self.rows) :
                self.map[x][y] = random.randrange(1, 7)

    def get_map_type(self, x, y) :
        return self.map[x][y]

    def edit_map(self, x, y, map_type) :
        if map_type != None :
            self.map[x][y] = map_type 

    def check_neighbor(self, cur_pos, next_pos) :
        is_neighbor = False

        if cur_pos[0] == next_pos[0] :
            if (cur_pos[1] + 1) == next_pos[1] or (cur_pos[1] - 1) == next_pos[1] : 
                is_neighbor = True
        elif cur_pos[1] == next_pos[1] :
            if (cur_pos[0] + 1) == next_pos[0] or (cur_pos[0] - 1) == next_pos[0] :
                is_neighbor = True

        return is_neighbor

    def swap(self, cur_pos, next_pos) :
        if self.check_neighbor(cur_pos, next_pos) == True :
            value = self.map[cur_pos[0]][cur_pos[1]]
            self.map[cur_pos[0]][cur_pos[1]] = self.map[next_pos[0]][next_pos[1]]
            self.map[next_pos[0]][next_pos[1]] = value 
            return True
        else :
            return False
  
    def check_value(self, cur_pos, direction, value) :
        x = cur_pos[0]
        y = cur_pos[1]
        is_valid = False

        if direction == BOARD_LEFT :
            x -= 1
        elif direction == BOARD_RIGHT :
            x += 1
        elif direction == BOARD_UP :
            y -= 1
        elif direction == BOARD_DOWN :
            y += 1

        if (x >= 0 and x < self.cols) : 
            if (y >= 0 and y < self.rows) :
                is_valid = True

        if is_valid == True and (self.map[x][y] == value) :
            return True, (x, y)

        return False, (None, None)  

    def check_values(self, cur_pos) :
        candidate = []
        saved = []

        print('start check', cur_pos)
        candidate.append(cur_pos)
        value = self.map[cur_pos[0]][cur_pos[1]]
    
        if value == 0 :
            return False

        while len(candidate) > 0 :
            cur_pos = candidate.pop(0)

            if self.map[cur_pos[0]][cur_pos[1]] == value :
                if cur_pos not in saved :
                    saved.append(cur_pos)
                    
            for dir in check_dirs :
                result, pos = self.check_value(cur_pos, dir, value)
                if result == True :
                    if pos not in saved : 
                        candidate.append(pos)

            if debug_ctrl['checks_values'] == True :
                print('save', saved)
                print('candidate', candidate)

        if len(saved) < SAME_THRESHOLD :
            print('too small')
            return False
        
        same_x = 0
        same_y = 0
        if len(saved) == SAME_THRESHOLD :
            (x, y) = saved[0]
            for i in range(1, len(saved)) :
                (x1, y1) = saved[i]
                if x == x1 : 
                    same_x += 1
                if y == y1 :
                    same_y += 1

            print('same count', (same_x, same_y))
            if (same_x < SAME_THRESHOLD - 1) and (same_y < SAME_THRESHOLD - 1) :
                print('not continue')
                return False

        for save in saved :
            self.remove_list.append(save)

        if debug_ctrl['checks_values'] == True :    
            print('final check_values', saved)

        return True

    def check_area(self, col = 0, row = 0) :
        if col == 0 and row == 0 :
            col = self.cols
            row = self.rows

        remove_area = 0
        area_candidate = []
        for x in range(col) :
            for y in range(row) :
                area_candidate.append((x, y))

        while len(area_candidate) > 0 :
            pos = area_candidate.pop(0)
            if pos not in self.remove_list :
                if self.check_values(pos) == True :
                    remove_area += 1           

        if debug_ctrl['check_area'] == True :    
            print('remove areas :', remove_area)

    def clear(self) :
        if debug_ctrl['clear'] == True :
            print('clear', self.remove_list)

        for (x, y) in self.remove_list :
            self.map[x][y] = 0xFF

            if SOUND :
                self.snd_shot.play()   

    def remove(self) :
        if debug_ctrl['remove'] == True :
            print('remove', self.remove_list)

        remove_count = 0
        self.remove_columns = []
        while len(self.remove_list) > 0 :
            (x, y) = self.remove_list.pop(0)
            self.map[x][y] = 0

            remove_count += 1
            if x not in self.remove_columns :
                self.remove_columns.append(x)     

    def move_down(self, cols = []) :
        if cols == [] :
            cols = self.remove_columns

        for x in cols :        
            empty_y = []
            for y in range(self.rows) :
                if self.map[x][y] == 0 :
                    empty_y.append(y)
                else :
                    if len(empty_y) > 0 :
                        y1 = empty_y.pop(0)
                        self.map[x][y1] = self.map[x][y]
                        self.map[x][y] = 0
                        empty_y.append(y)

    def do_combo(self) :
        combo_count = 0
        while self.check_area() :
            self.remove()
            self.move_down()
            combo_count += 1

        if debug_ctrl['do_combo'] == True :
            print('do_combo : ', combo_count)

    def fill_row(self) :
        is_fill = False
        y = self.rows - 1
        for x in range(self.cols) :
            if self.map[x][y] == 0 :
                self.map[x][y] = random.randrange(1, 7)
                is_fill = True

        if is_fill == True :
            down_cols = range(self.cols)
            self.move_down(down_cols)
        else :
            print('there is no empty cell')

        return is_fill
        
    def draw(self) :
        rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width, self.obj_height)

        # map[0][0] is left and bottom
        rect.y += (self.rows - 1) * self.obj_height 
        for y in range(self.rows) :
            for x in range(self.cols) :
                if self.map[x][y] != 0 :
                    if self.map[x][y] != 0xFF :
                        keys = board_dict[self.map[x][y]]
                        if keys != None :
                            for key in keys :
                                if key != 0 :
                                    self.object[key].draw(rect)
                    else :
                        gctrl.gamepad.blit(self.effect_boot, rect)
                else :
                    pygame.draw.rect(gctrl.gamepad, COLOR_RED, rect, 1, 1)

                rect.x += self.obj_width
            rect.y -= self.obj_height
            rect.x = self.x_offset

if __name__ == '__main__' :
    print('game board object')
