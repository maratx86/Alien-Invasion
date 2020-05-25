def check_lib():
    try:
        lib = "pygame"
        import pygame
        lib = "random"
        import random
        lib = "os"
        import os
        lib = "sys"
        import sys
        lib = 'local statistic'
        from statistic import Stat
        lib = 'local button'
        from button import Button
        lib = 'local character'
        from character import Character
        lib = 'local show_statistic'
        import show_statistic
        return True
    except ImportError:
        print('\n>>>> Library "{}" not installed <<<<'.format(lib))
        return False


if check_lib():
    import pygame
    from statistic import Stat
    from button import Button
    from character import Character
    import show_statistic
    import random
    import os
    import additional
    import game_functions
else:
    print("\nSome library is missing...\a")
    raise SystemExit(10)


additional.write_temp_file('count_of_shell.ai', 0)
directories = additional.directory_finder()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 255, 255)
PINK = (255, 100, 180)
ORANGE = (255, 100, 10)
YELLOW = (255, 255, 0)

save_stat_flag = True
WIDTH = 1080
HEIGHT = 720
FPS = 30

settings_dict = additional.check_settings()
for key, value in settings_dict.items():
    if key == 'save_stat': save_stat_flag = value
    elif key == 'WIDTH' : WIDTH = value
    elif key == 'HEIGHT' : HEIGHT = value
    elif key == 'FPS' : FPS = value


class ShellObject(pygame.sprite.Sprite):

    def __init__(self, shell_object_img, character):

        self.shell_speed = 7
        super().__init__()
        self.image = shell_object_img
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (character.rect.x + 75, character.rect.bottom)

    def update(self):
        if self.rect.top < HEIGHT:
            self.rect.y += self.shell_speed
        else:
            count_of_shells = additional.read_temp_file('count_of_shell.ai')[0]
            count_of_shells -= 1
            additional.write_temp_file('count_of_shell.ai', count_of_shells)
            self.kill()


def game_making(mode):
    from statistic import Stat
    global WIDTH, HEIGHT, directories
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    game_name = "Alien Invasion ({}x{}) Mode {}".format(WIDTH, HEIGHT, mode)
    сharacter_position = (WIDTH // 2, 100)

    pygame.init()
    starting_time = pygame.time.get_ticks()
    pygame.display.set_caption(game_name)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    character_left_img = pygame.image.load(directories["media_dir"] + "{}_character.png".format(mode)).convert()
    character_right_img = pygame.image.load(directories["media_dir"] + "{}_character.png".format(mode)).convert()
    character_death_img = pygame.image.load(directories["media_dir"] + "{}_character_Death.png".format(mode)).convert()
    fall_object_img = pygame.image.load(directories["media_dir"] + "{}_fall_object.png".format(mode)).convert()
    shell_object_img = pygame.image.load(directories["media_dir"] + "{}_shell.png".format(mode)).convert()
    background_img = pygame.image.load(directories["media_dir"] + "{}_background.png".format(mode)).convert()
    reason_pic_died = pygame.image.load(directories["media_dir"] + "died.png").convert()
    blackscreen = pygame.image.load(directories["media_dir"] + "gameover_black.png").convert()

    background_music = directories["media_dir"] + "{}_background_music.mp3".format(mode)

    pygame.mixer.init()
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    pygame.event.wait()

    hit_sound = directories["media_dir"] + "hit.ogg"
    hit_sound = pygame.mixer.Sound(hit_sound)
    
    complete_sound = directories["media_dir"] + "complete.ogg"
    complete_sound = pygame.mixer.Sound(complete_sound)
    
    end_music = directories["media_dir"] + "{}_end_music.ogg".format(mode)
    end_music = pygame.mixer.Sound(end_music)
    
    level_mode = 0
    COUNT_OF_LIVES = 1
    CURRENT_SCORE = 0
    max_count_of_shells = 10
    falling_speed = 5
    action_speed = 5
    count_of_collision = 0
    action_from_obj = False

    

    class FallObject(pygame.sprite.Sprite):
        falling_speed = 5

        def __init__(self, fall_object_img, falling_speed = 5, action_speed = 5,  num_w = 0, row = 0):
            self.falling_speed = falling_speed
            self.action_speed = action_speed
            self.image = fall_object_img
            super().__init__()
            self.image.set_colorkey(BLACK)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = (num_w, row)

        def update(self):
            global HEIGHT
            nonlocal down, down_flag, direction, direction_flag, count_of_collision, action_from_obj
            action_from_obj = False
            if down:
                if self.rect.bottom < HEIGHT - 5:
                    self.rect.y -= self.falling_speed
                else:
                    character.lives = 0
                    self.kill()
                down_flag = True
                if direction: self.rect.x += self.action_speed
                else: self.rect.x -= self.action_speed
            else:
                if direction: self.rect.x += self.action_speed
                else: self.rect.x -= self.action_speed
            
            if self.rect.right >= WIDTH or self.rect.left <= 0:
                count_of_collision += 1
                if count_of_collision % (2*number_of_row) == 0:
                    down_flag = True
                    count_of_collision = 0
                direction_flag = True
         
            if self.rect.top <= character.rect.bottom:
                self.kill()
                character.lives = 0

            if death_flag: self.kill()

    
    class SoundInd(pygame.sprite.Sprite):
        def __init__(self, sound_on, sound_off):
            super().__init__(self)
            self.sound_off = sound_off
            self.sound_on = sound_on
            self.image = sound_on
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (character.rect.x + 75, character.rect.bottom)

        def update(self):
            0
    
    def make_harder():
        global falling_speed
        falling_speed += 1

    def generate_wariors(test = False, level = 0):
        global number_of_row, number_of_war
        if test:
            fall_object = FallObject(fall_object_img, falling_speed, action_speed,  WIDTH//2, HEIGHT//2 + 200)
            fall_objects.add(fall_object)
            all_sprites.add(fall_objects)
            return 1

        number_of_war = WIDTH // 200
        number_of_row = HEIGHT // 2 // 150
        if not test:
            for i_r in range(number_of_row):
                for i_w in range(number_of_war):
                    fall_object = FallObject(fall_object_img, falling_speed + level, action_speed + level, 200*(i_w+1), HEIGHT - 100 * (i_r + 1))
                    fall_objects.add(fall_object)
                    
            all_sprites.add(fall_objects)
            return number_of_war * number_of_row

    all_sprites = pygame.sprite.Group()
    character = Character(0, character_right_img, character_left_img, character_death_img, сharacter_position, WIDTH, HEIGHT, max_count_of_shells)
    all_sprites.add(character)

    fall_objects = pygame.sprite.Group()
    shell_objects = pygame.sprite.Group()

    stat = Stat()
    
    kill_fall_object = 0
    
    number_of_war = WIDTH // 200
    number_of_row = HEIGHT // 2 // 150
    
    button_width = 250
    button_height = 100
    start_button = Button(screen, (0, 0, 0),
                       (WIDTH - button_width) // 2,
                       (HEIGHT - button_height) // 2,
                       button_width, button_height, 100, 'Start game', (255, 255, 255))

    def new_game(level = 0):
        global all_sprites, character, all_sprites, fall_objects, shell_objects, kill_fall_object, down, count_of_wariors, count_of_alive
        additional.write_temp_file('count_of_shell.ai', 0)
        all_sprites = pygame.sprite.Group()
        character = Character(level, character_right_img, character_left_img, character_death_img, сharacter_position, WIDTH, HEIGHT, max_count_of_shells)
        all_sprites.add(character)
        fall_objects = pygame.sprite.Group()
        shell_objects = pygame.sprite.Group()
        kill_fall_object = 0
        down = False
        
        if level != 0:
            count_of_wariors = generate_wariors(False, level)
            return count_of_wariors

    death_flag = False
    running = True
    count_of_wariors = generate_wariors(False)
    count_of_alive = count_of_wariors
    freaze_game = True
    pause_flag = False
    start_game_time = 0
    down = False
    down_flag = False
    change_mode = False

    direction = False
    direction_flag = False

    def change_smth(return_dict):
        ['running', 'character', 'freaze_game', 'death_flag', 'shell_objects', 'stat']
        nonlocal running, character, freaze_game, death_flag, shell_objects, stat, all_sprites, CURRENT_SCORE, pause_flag
        for var, val in return_dict.items():
            if var == 'running': running = val
            elif var == 'character': character = val
            elif var == 'freaze_game': freaze_game = val
            elif var == 'pause_flag': pause_flag = val
            elif var == 'death_flag': death_flag = val
            elif var == 'shell_objects': shell_objects = val
            elif var == 'all_sprites': all_sprites = val
            elif var == 'stat': stat = val
            elif var == 'current_score': CURRENT_SCORE = val


    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            return_dict = game_functions.check_event(event, stat, settings_dict, freaze_game,
                                                     pause_flag, death_flag, character, start_button, shell_objects,
                                                     all_sprites, shell_object_img, CURRENT_SCORE)
            if return_dict != {}: change_smth(return_dict)

        if not freaze_game:
            action_from_obj = True
            hits_shell = pygame.sprite.groupcollide(shell_objects, fall_objects, True, pygame.sprite.collide_mask)

            if death_flag:
                if last == 'left':
                    character.go_left()
                elif last == 'right':
                    character.go_right()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            character.go_left()
                            last = 'left'
                        elif event.key == pygame.K_RIGHT:
                            character.go_right()
                            last = 'right'

                Character.jump(character)

                first_font = pygame.font.Font(None, 50)
                score_table = first_font.render('Your reached score : {}'.format(CURRENT_SCORE), 1, BLACK, ORANGE)

                leight = pygame.mixer.Sound.get_length(end_music)
                seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                if leight <= seconds:
                    freaze_game = True
                    if len(stat.temp_score) > 0: CURRENT_SCORE = stat.plus_temp()
                    stat.add_max_score(CURRENT_SCORE)
                    stat.add_level(character.level)
            else:
                if hits_shell:
                    kill_fall_object += 1
                    count_of_shells = additional.read_temp_file('count_of_shell.ai')[0]
                    if count_of_shells > 0:
                        count_of_shells -= 1
                    else:
                        count_of_shells = 0
                    additional.write_temp_file('count_of_shell.ai', count_of_shells)

                    character.killed_objects += 1
                    if not character.killed_objects == count_of_wariors: hit_sound.play()
                    count_of_alive -= 1
                if (character.lives == 0):
                    character.death()
                    pygame.mixer.music.pause()
                    end_music.play()
                    start_ticks = pygame.time.get_ticks()
                    blackscreen.set_alpha(200)
                    last = ''
                    character.character_left_img = character_death_img
                    character.character_right_img = character_death_img
                    death_flag = True
                    if character.lives == 0:
                        reason_die = 'YOU DIE'
                        reason_pic = reason_pic_died

                    
            # screen.fill(WHITE)
            all_sprites.update()
            if not death_flag:
                screen.blit(background_img, (0, 0))
            else:
                screen.blit(background_img, (0, 0))
                screen.blit(blackscreen, (0, 0))
                reason_pic.set_colorkey(BLACK)
                screen.blit(reason_pic, (0, 0))
                screen.blit(score_table, (HEIGHT // 2, WIDTH // 2 - 500))
                # screen.blit(died_reason_table, (HEIGHT // 2 - 150, WIDTH // 2 - 150))

            all_sprites.draw(screen)

            if not death_flag:
                # SCORE TABLE ADDING
                CURRENT_SCORE = (pygame.time.get_ticks() - start_game_time) // 100
                first_font = pygame.font.Font(None, 50)
                score_table = first_font.render('Score : {}'.format(CURRENT_SCORE), 1, BLACK, ORANGE)
                second_font = pygame.font.Font(None, 50)
                level_table = second_font.render('Level : {}'.format(character.level), 1, BLACK, ORANGE)

                screen.blit(score_table, (20, 30))
                screen.blit(level_table, (WIDTH//2 + 200, 30))
                if direction_flag:
                    direction = not direction
                    direction_flag = False
                if down_flag:
                    down_flag = False
                    down = not down
            if (character.killed_objects == count_of_wariors or count_of_alive == 0 or action_from_obj) and not death_flag: 
                complete_sound.play()
                character.killed_objects = 0
                character.level += 1
                count_of_alive = new_game(character.level + 1)
        else:
            # print(pause_flag)
            if pause_flag:
                '''pause actions'''
            else:
                if death_flag:
                    pygame.mixer.music.pause()
                    count_of_wariors = generate_wariors(False)
                    character.kill()
                    character = Character(0, character_right_img, character_left_img, character_death_img, сharacter_position, WIDTH, HEIGHT, max_count_of_shells)
                    all_sprites.add(character)
                death_flag = False
                blackscreen.set_alpha(200)
                
                main_first_font = pygame.font.Font(None, 50)
                main_score_table = main_first_font.render('Your best score : {}'.format(stat.max_score), 1, BLACK, ORANGE)
                main_second_font = pygame.font.Font(None, 50)
                main_level_table  = main_second_font.render('Your best level : {}'.format(stat.max_level), 1, BLACK, ORANGE)

                screen.blit(background_img, (0, 0))
                screen.blit(blackscreen, (0, 0))
                
                screen.blit(main_score_table, (int(WIDTH*0.65), HEIGHT//2 - 40))
                screen.blit(main_level_table, (int(WIDTH*0.65), HEIGHT//2))
                
                
                button_width = 250
                button_height = 100
                start_button = Button(screen, (0, 0, 0),
                                      (WIDTH - button_width) // 2,
                                      (HEIGHT - button_height) // 2,
                                      button_width, button_height, 100, 'Start game', (255, 255, 255))
                all_sprites.draw(screen)
        
            
            
        pygame.display.flip()
    pygame.quit()
    if change_mode: game_making(mode)
    return CURRENT_SCORE


if __name__ == '__main__':
    try: game_making(random.randint(1, 3))
    except pygame.error: print('end')
else: print()
