import pygame
from animation import Animation
from additional import directories


def create_pause_object(x, y):
    pics = []
    way = directories['animation_dir'] + 'pause' + directories['slash']
    for num in range(48):
        picture = way + '{}.png'.format(num + 1)
        picture = pygame.image.load(picture).convert()
        pics.append(picture)

    return Animation(x, y, pics)


def create_start_pic(x, y):
    pics = []
    way = directories['animation_dir'] + 'start' + directories['slash']
    for num in range(4):
        picture = way + '{}.png'.format(num + 1)
        picture = pygame.image.load(picture).convert()
        pics.append(picture)

    return Animation(x, y, pics)


def create_edge_pic(x, y, flag = True):
    pics = []
    way = directories['animation_dir'] + 'edge' + directories['slash']

    for num in range(46):
        picture = way + '{}.png'.format(num + 1)
        picture = pygame.image.load(picture).convert()
        if flag: picture = pygame.transform.rotate(picture, 180)
        pics.append(picture)

    return Animation(x, y, pics)
