import pygame


class Character(pygame.sprite.Sprite):
    count_of_shells = 0
    count_of_jumps = 0

    '''
    This class for creating character, there are this methods
        update
            Additing number in temp_score (Using for stopping and continuing game)
        move
            For moving character in the screen
        go_left
            For going to left
        go_right
            For going to right
        jump
            For jumping moves
        death
            For changing character`s image
    '''

    def __init__(self, level, character_right_img, character_left_img, character_death_img, Character_position, WIDTH,
                 HEIGHT, max_count_of_shells):
        self.jumping_range = 30
        self.character_right_img = character_right_img
        self.character_left_img = character_left_img
        self.character_death_img = character_death_img
        super().__init__()
        self.image = character_right_img
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = Character_position
        self.lives = 1
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.flag_int_shell = 0
        self.max_count_of_shells = max_count_of_shells

        self.level = level
        self.killed_objects = 0

    def update(self):
        if self.rect.left >= self.WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.WIDTH

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.go_right()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.go_left()

    def move(self, direction):
        if direction == "Left":
            self.rect.x -= 5
            self.image = self.character_left_img
            self.image.set_colorkey((0, 0, 0))
        if direction == "Right":
            self.rect.x += 5
            self.image = self.character_right_img
            self.image.set_colorkey((0, 0, 0))
        if direction == "Jump Up":
            self.rect.y -= 4
        if direction == "Jump Down":
            self.rect.y += 4

    def go_left(self):
        self.move("Left")

    def go_right(self):
        self.move("Right")

    def jump(self):
        if self.count_of_jumps == 0:
            self.count_of_jumps = self.jumping_range
        if self.count_of_jumps > (self.jumping_range + 1) / 2:
            self.move("Jump Up")
            self.count_of_jumps -= 1
        if self.count_of_jumps <= (self.jumping_range + 1) / 2:
            self.move("Jump Down")
            self.count_of_jumps -= 1

    def death(self):
        self.image = self.character_death_img
        self.image.set_colorkey((0, 0, 0))