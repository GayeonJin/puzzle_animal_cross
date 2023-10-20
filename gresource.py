#!/usr/bin/python

import sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

resource_path = ''

resource_img_item = {
    'id_background' : 'image/background.png',
    'id_boom' : 'image/boom.png'
}

resource_tile_item = {
    'id_bear' : 'image/bear.png',
    'id_cat' : 'image/cat.png',
    'id_cow' : 'image/cow.png',
    'id_fox' : 'image/fox.png',  
    'id_koala' : 'image/koala.png',
    'id_koki' : 'image/koki.png',
    'id_little_lion' : 'image/little-lion.png',
}

resource_sound = {
    'snd_shot' : 'sound/shot.wav',
    'snd_explosion' : 'sound/explosion.wav'
}

def get_img_resource(resource_id) :
    return resource_path + resource_img_item[resource_id]

def get_tile_resource(resource_id) : 
    return resource_path + resource_tile_item[resource_id]

def get_snd_resource(resource_id) :
    return resource_path + resource_sound[resource_id]

if __name__ == '__main__' :
    print('game resoure')