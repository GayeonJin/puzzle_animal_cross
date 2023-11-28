#!/usr/bin/python

import os
import sys

import pygame
from time import sleep

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
    gctrl.draw_string(str, 0, 0, ALIGN_CENTER, 40, COLOR_BLACK)

    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global board

    cursor = cursor_object(board)

    cursor.x = 0
    cursor.y = 0

    board.shuffle()
    state = STATE_IDLE
    next_state = STATE_CHECK_ALL

    game_exit = False
    while not game_exit :

        state = next_state

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                game_exit = True

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
        gctrl.clock.tick(FPS)

def test_game() :
    global board

    cursor = cursor_object(board)

    cursor.x = 0
    cursor.y = 0

    board.shuffle()
    state = STATE_IDLE

    test_exit = False
    while not test_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                test_exit = True

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
        gctrl.clock.tick(FPS)

def start_game() :
    # Clear gamepad
    gctrl.surface.fill(COLOR_WHITE)

    gctrl.draw_string(TITLE_STR, 0, 0, ALIGN_CENTER, 30, COLOR_BLACK)

    help_str = ['r : run game',
                't : test game',
                'x : exit']

    for i, help in enumerate(help_str) :
        y_offset = 150 - i * 25
        gctrl.draw_string(help, 0, y_offset, ALIGN_CENTER | ALIGN_BOTTOM, 25, COLOR_BLUE)

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
        gctrl.clock.tick(FPS)    
       
def init_game() :
    global board

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
