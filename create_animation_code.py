import pygame
from animation import Animation
from additional import directories


def create_pause_object(x, y):
    pics = []
    for num in range(48):
        picture = directories['animation_dir'] + str(num + 1) + '.png'
        picture = pygame.image.load(picture).convert()
        pics.append(picture)

    return Animation(x, y, pics)
