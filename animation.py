import pygame
from additional import check_settings

settings = check_settings()


class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, pics, start_pic=0):
        super().__init__()
        self.pics = tuple(pics)
        self.len_pics = len(pics)
        self.image = pics[0]
        self.number_image = start_pic
        self.image.set_colorkey(settings.colours.transparency)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.len_pics > self.number_image + 1:
            self.number_image += 1
        else:
            self.number_image = 0
        self.image = self.pics[self.number_image]
        self.image.set_colorkey(settings.colours.transparency)


class MovingAnimation(Animation):
    def __init__(self, x, y, pics):
        super().__init__(x, y, pics)

    def update(self):
        if self.len_pics > self.number_image + 1:
            self.number_image += 1
        else:
            self.number_image = 0
        self.image = self.pics[self.number_image]
        self.image.set_colorkey(settings.colours.transparency)

        self.rect.center()
