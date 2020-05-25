import pygame
import additional
from os import environ

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

settings = additional.check_settings()


class Column(pygame.sprite.Sprite):
    '''
    This class for creating columns
    '''
    def __init__(self, x, height, colour):
        self.width = settings.statistic.width
        super().__init__()
        self.image = pygame.Surface((self.width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, settings.statistic.HEIGHT - settings.statistic.skip_edge - height//2)


class ShowStat():
    '''
    This class for showing statistics in pygame window
    '''

    def __init__(self):
        self.self = 5

    def show(self, stat):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((settings.statistic.WIDTH, settings.statistic.HEIGHT))
        pygame.display.set_caption("Alien Invasion >>> Statistics")
        clock = pygame.time.Clock()

        work_HEIGHT = settings.statistic.HEIGHT - 2 * settings.statistic.skip_edge
        work_WIDTH = settings.statistic.WIDTH - 2 * settings.statistic.skip_edge

        number_of_score = len(stat.score)
        _one_ = work_HEIGHT / stat.max_score
        _skip_column_ = work_WIDTH / number_of_score

        _one_level_ = work_HEIGHT / stat.max_level

        all_sprites = pygame.sprite.Group()
        sprites_of_score = pygame.sprite.Group()
        sprites_of_level = pygame.sprite.Group()
        addit = _skip_column_ // 2

        for i in range(number_of_score):
            col_1 = Column(int(settings.statistic.skip_edge + _skip_column_ * i + addit),
                           int(stat.score[i] * _one_), settings.statistic.colour_column_score)
            col_2  = Column(int(settings.statistic.skip_edge + _skip_column_ * i + addit + 7),
                            int(stat.levels[i] * _one_level_), settings.statistic.colour_column_level)
            sprites_of_score.add(col_1)
            sprites_of_level.add(col_2)

        all_sprites.add(sprites_of_score)
        all_sprites.add(sprites_of_level)

        running = True
        while running:
            clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(settings.statistic.colour_background)

            all_sprites.draw(screen)
            pygame.display.flip()

        pygame.quit()

