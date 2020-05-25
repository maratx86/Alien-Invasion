import additional
import pygame


settings = additional.check_settings()


class ShellObject(pygame.sprite.Sprite):

    def __init__(self, shell_object_img, character):

        self.shell_speed = 7
        super().__init__()
        self.image = shell_object_img
        self.image.set_colorkey(settings.colours.transparency)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (character.rect.x + 75, character.rect.bottom)

    def update(self):
        if self.rect.top < settings.HEIGHT:
            self.rect.y += self.shell_speed
        else:
            count_of_shells = additional.read_temp_file(settings.files.temp_count_of_shells)[0]
            count_of_shells -= 1
            additional.write_temp_file(settings.files.temp_count_of_shells, count_of_shells)
            self.kill()
