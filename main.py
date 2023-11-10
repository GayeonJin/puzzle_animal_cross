#!/usr/bin/python

import os
import sys
import csv

import pygame
import random
from time import sleep

from tkinter import filedialog
from tkinter import *

from gresource import *
from gobject import *

from board import *
from cursor import *

TITLE_STR = 'Animal Cross Puzzle'

STATE_IDLE = 0
STATE_CHECK_ALL = 9
STATE_CLEAR = 1
STATE_REMOVE = 2
STATE_MOVE_DOWN = 3
STATE_FILL = 4
STATE_COMBO = 5 

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

    gctrl.surface.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global clock
    global board

    cursor = cursor_object(board)

    cursor.x = 0
    cursor.y = 0

    board.shuffle()
    state = STATE_IDLE
    next_state = STATE_CHECK_ALL

    edit_exit = False
    while not edit_exit :

        state = next_state

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = CURSOR_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    direction = CURSOR_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    direction = CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = CURSOR_MOVE_RIGHT
                elif event.key == pygame.K_1 :
                    state = STATE_CLEAR
                elif event.key == pygame.K_5 :
                    state = STATE_COMBO                    
                elif event.key == pygame.K_9 :
                    state = STATE_CHECK_ALL
                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN :
                mouse_pos = pygame.mouse.get_pos()
                x, y = board.get_pos(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos()
                next_x, next_y = board.get_pos(mouse_pos)
                if x != None or y != None :
                    if board.swap((x, y), (next_x, next_y)) :
                        is_next = board.check_values((next_x, next_y))
                        is_cur = board.check_values((x, y))

                        if is_next or is_cur :
                            cursor.set_pos(next_x, next_y)
                            next_state = STATE_CLEAR 
                        else :
                            board.swap((x, y), (next_x, next_y)) 

        if state == STATE_CLEAR :
            # clear item and make effect
            board.clear()
            next_state = STATE_REMOVE
        if state == STATE_REMOVE :
            # remove item
            board.remove()
            next_state = STATE_MOVE_DOWN
        elif state == STATE_MOVE_DOWN :
            # move down block
            board.move_down()
            next_state = STATE_FILL
        elif state == STATE_FILL :
            # fill empty cells
            if board.fill_row() == False :
                next_state = STATE_CHECK_ALL
            else :
                next_state = STATE_FILL
        elif state == STATE_COMBO :
            # Check combo
            board.do_combo()
            next_state = STATE_IDLE                        
        elif state == STATE_CHECK_ALL :
            # check all reaa
            if board.check_area() == False :
                next_state = STATE_IDLE
            else :
                next_state = STATE_CLEAR

        state = 0

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw board
        board.draw()

        # Draw cursor
        cursor.draw_rect(COLOR_BLACK, 1)

        pygame.display.update()
        clock.tick(60)

def test_game() :
    global clock
    global board

    cursor = cursor_object(board)

    cursor.x = 0
    cursor.y = 0

    board.shuffle()
    state = STATE_IDLE

    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = CURSOR_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    direction = CURSOR_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    direction = CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = CURSOR_MOVE_RIGHT
                elif event.key == pygame.K_1 :
                    state = STATE_CLEAR
                elif event.key == pygame.K_2 :
                    state = STATE_REMOVE
                elif event.key == pygame.K_3 :
                    state = STATE_MOVE_DOWN
                elif event.key == pygame.K_4 :
                    state = STATE_FILL
                elif event.key == pygame.K_5 :
                    state = STATE_COMBO                    
                elif event.key == pygame.K_9 :
                    state = STATE_CHECK_ALL
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN :
                mouse_pos = pygame.mouse.get_pos()
                x, y = board.get_pos(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos()
                next_x, next_y = board.get_pos(mouse_pos)
                if x != None or y != None :
                    if board.swap((x, y), (next_x, next_y)) :
                        is_next = board.check_values((next_x, next_y))
                        is_cur = board.check_values((x, y))

                        if is_next or is_cur :
                            cursor.set_pos(next_x, next_y)
                        else :
                            board.swap((x, y), (next_x, next_y)) 

        if state == STATE_CLEAR :
            # clear item and make effect
            board.clear()        
        if state == STATE_REMOVE :
            # remove item
            board.remove()
        elif state == STATE_MOVE_DOWN :
            # move down block
            board.move_down()
        elif state == STATE_FILL :
            # fill empty cells
            board.fill_row()
        elif state == STATE_COMBO :
            # Check combo
            board.do_combo()                        
        elif state == STATE_CHECK_ALL :
            # check all reaa
            board.check_area()

        state = 0

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw board
        board.draw()

        # Draw cursor
        cursor.draw_rect(COLOR_BLACK, 1)

        pygame.display.update()
        clock.tick(60)

def start_game() :
    # Clear gamepad
    gctrl.surface.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render(TITLE_STR, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    gctrl.surface.blit(text_suf, text_rect)

    help_str = ['r : run game',
                't : test game',
                'x : exit']

    font1 = pygame.font.SysFont(None, 25)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.width / 2
        gctrl.surface.blit(text_suf1, text_rect1)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_r :
                    return 'run'
                elif event.key == pygame.K_t :
                    return 'test'
                elif event.key == pygame.K_x :
                    terminate()

        pygame.display.update()
        clock.tick(60)    
       
def init_game() :
    global clock
    global board

    pygame.init()
    clock = pygame.time.Clock()

    # board
    board = game_board(MAX_ROWS, MAX_COLS)
    for i, resource_key in enumerate(resource_tile_item) :
        board.add_objet(resource_key, game_object(0, 0, get_tile_resource(resource_key)))

    (pad_width, pad_height) = board.get_padsize()
    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

if __name__ == '__main__' :
    init_game()

    while True :
        mode = start_game()
        print(mode)
        if mode == 'run' :
            run_game()
        elif mode == 'test' :
            test_game()
