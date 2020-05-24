import pygame
from os import environ

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PeachPuff = (255, 218, 185)


class Column(pygame.sprite.Sprite):
    '''
    This class for creating columns
    '''
    def __init__(self, x, height, HEIGHT, skip, colour):
        self.width = 5
        super().__init__()
        self.image = pygame.Surface((self.width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, HEIGHT - skip - height//2)


class ShowStat():
    '''
    This class for showing statistics in pygame window
    '''

    def __init__(self):
        self.self = 5

    def show(self, stat, WIDTH, HEIGHT):
        environ['SDL_VIDEO_CENTERED'] = '1'
        FPS = 30

        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Alien Invasion >>> Statistics")
        clock = pygame.time.Clock()

        skip = 20

        work_HEIGHT = HEIGHT - 2*skip
        work_WIDTH = WIDTH - 2*skip

        number_of_score = len(stat.score)
        _one_ = work_HEIGHT / stat.max_score
        _skip_column_ = work_WIDTH / number_of_score

        _one_level_ = work_HEIGHT / stat.max_level

        all_sprites = pygame.sprite.Group()
        sprites_of_score = pygame.sprite.Group()
        sprites_of_level = pygame.sprite.Group()
        addit = _skip_column_ // 2

        for i in range(number_of_score):
            col_1 = Column(int(skip + _skip_column_ * i + addit), int(stat.score[i] * _one_), HEIGHT, skip, BLACK)
            col_2  = Column(int(skip + _skip_column_ * i + addit + 7), int(stat.levels[i] * _one_level_), HEIGHT, skip, GREEN)
            sprites_of_score.add(col_1)
            sprites_of_level.add(col_2)

        all_sprites.add(sprites_of_score)
        all_sprites.add(sprites_of_level)

        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(PeachPuff)

            all_sprites.draw(screen)
            pygame.display.flip()

        pygame.quit()

