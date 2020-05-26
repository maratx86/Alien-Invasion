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
        lib = 'local settings'
        import settings
        return True
    except ImportError:
        print('\n>>>> Library "{}" not installed <<<<'.format(lib))
        return False


if check_lib():
    import pygame
    from button import Button
    from character import Character
    import settings
    import random
    import os
    import additional
    import game_functions
    import create_animation_code
else:
    print("\nSome library is missing...\a")
    raise SystemExit(10)


settings = additional.check_settings()

additional.write_temp_file(settings.files.temp_count_of_shells, 0)
directories = additional.directory_finder()

settings.fonts = pygame.font.get_fonts()


def game_making(mode):
    from statistic import Stat
    global directories
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    game_name = settings.game_name
    if settings.show_sreen: game_name += ' ({}x{})'.format(settings.WIDTH, settings.HEIGHT)
    if settings.show_mode: game_name += ' Mode {}'.format(mode)

    pygame.init()
    starting_time = pygame.time.get_ticks()
    pygame.display.set_caption(game_name)
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()

    loading_font = pygame.font.Font(None, 75)
    loading_table = loading_font.render(settings.loading_text, 1, settings.colours.loading)
    loading_coord = loading_table.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
    screen.fill(settings.colours.DarkGrey)
    screen.blit(loading_table, loading_coord)
    pygame.display.flip()

    character_left_img = pygame.image.load(directories["media_dir"] + "{}_character.png".format(mode)).convert()
    character_right_img = pygame.image.load(directories["media_dir"] + "{}_character.png".format(mode)).convert()
    character_death_img = pygame.image.load(directories["media_dir"] + "{}_character_Death.png".format(mode)).convert()
    fall_object_img = pygame.image.load(directories["media_dir"] + "{}_fall_object.png".format(mode)).convert()
    shell_object_img = pygame.image.load(directories["media_dir"] + "{}_shell.png".format(mode)).convert()
    background_img = pygame.image.load(directories["media_dir"] + "{}_background.png".format(mode)).convert()
    reason_pic_died = pygame.image.load(directories["media_dir"] + "died.png").convert()
    blackscreen = pygame.image.load(directories["media_dir"] + "gameover_black.png").convert()

    background_music = directories["media_dir"] + "{}_background_music.mp3".format(mode)

    music_volume = settings.sounds_volume / 100

    pygame.mixer.init()
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.pause()
    pygame.event.wait()

    hit_sound = directories["media_dir"] + "hit.ogg"
    hit_sound = pygame.mixer.Sound(hit_sound)
    hit_sound.set_volume(0.75*music_volume)
    
    complete_sound = directories["media_dir"] + "complete.ogg"
    complete_sound = pygame.mixer.Sound(complete_sound)
    complete_sound.set_volume(0.75 * music_volume)
    
    end_music = directories["media_dir"] + "{}_end_music.ogg".format(mode)
    end_music = pygame.mixer.Sound(end_music)
    end_music.set_volume(0.75 * music_volume)

    level_mode = 0
    last_shell = 0
    CURRENT_SCORE = 0
    falling_speed = 5
    action_speed = 5
    count_of_collision = 0
    action_from_obj = False

    class FallObject(pygame.sprite.Sprite):
        def __init__(self, fall_object_img, falling_speed = settings.start.falling_object_speed,
                     action_speed = settings.start.action_object_speed,  num_w = 0, row = 0):
            super().__init__()
            self.falling_speed = falling_speed
            self.action_speed = action_speed
            self.image = fall_object_img
            self.image.set_colorkey(settings.colours.transparency)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = (num_w, row)

        def update(self):
            nonlocal down, down_flag, direction, direction_flag, count_of_collision, action_from_obj
            action_from_obj = False
            if down:
                if self.rect.bottom < settings.HEIGHT - 5:
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
            
            if self.rect.right >= settings.WIDTH or self.rect.left <= 0:
                if settings.double_wall:
                    count_of_collision += 1
                    if count_of_collision % (2 * number_of_row) == 0:
                        down_flag = True
                        count_of_collision = 0
                else:
                    down_flag = True
                direction_flag = True
            if self.rect.top <= 0:
                self.kill()
                character.lives = 0

            if death_flag: self.kill()

    def generate_wariors(test = False, level = 0):
        nonlocal number_of_row, number_of_war
        if test:
            fall_object = FallObject(fall_object_img, falling_speed, action_speed,  settings.WIDTH//2, settings.HEIGHT//2 + 200)
            fall_objects.add(fall_object)
            all_sprites.add(fall_objects)
            return 1

        number_of_war = settings.WIDTH // 200
        number_of_row = settings.HEIGHT // 2 // 150
        if not test:
            if settings.start.increaze_falling_speed: falling_speed = settings.start.falling_object_speed + level
            else: falling_speed = settings.start.falling_object_speed
            action_speed = settings.start.action_object_speed + level
            for i_r in range(number_of_row):
                for i_w in range(number_of_war):
                    fall_object = FallObject(fall_object_img, falling_speed,
                                             action_speed, 200*(i_w+1), settings.HEIGHT - 100 * (i_r + 1))
                    fall_objects.add(fall_object)
            all_sprites.add(fall_objects)
            return number_of_war * number_of_row

    all_sprites = pygame.sprite.Group()
    character = Character(0, character_right_img, character_left_img, character_death_img)
    all_sprites.add(character)

    fall_objects = pygame.sprite.Group()
    shell_objects = pygame.sprite.Group()

    stat = Stat()

    if settings.start.show_animation:
        factor = 100
        pause_animation_1 = create_animation_code.create_pause_object(settings.WIDTH//4 - factor, settings.HEIGHT//4)
        pause_animation_2 = create_animation_code.create_pause_object(3*settings.WIDTH // 4 + factor, 3*settings.HEIGHT // 4)
        pause_objects = pygame.sprite.Group(pause_animation_1, pause_animation_2)

    kill_fall_object = 0
    
    number_of_war = settings.WIDTH // 200
    number_of_row = settings.HEIGHT // 2 // 150

    start_button = Button(screen, (0, 0, 0),
                       (settings.WIDTH - settings.start_button_width) // 2,
                       (settings.HEIGHT - settings.start_button_height) // 2,
                       settings.start_button_width, settings.start_button_height, 100,
                          settings.start_button_text, settings.colours.white)

    def new_game(level = 0):
        nonlocal all_sprites, character, all_sprites, fall_objects, shell_objects, kill_fall_object, down, count_of_wariors, count_of_alive
        additional.write_temp_file(settings.files.temp_count_of_shells, 0)
        all_sprites = pygame.sprite.Group()
        # character = Character(level, character_right_img, character_left_img, character_death_img)
        all_sprites.add(character)
        fall_objects = pygame.sprite.Group()
        shell_objects = pygame.sprite.Group()
        kill_fall_object = 0
        down = False
        
        if level != 0:
            count_of_wariors = generate_wariors(False, level)
            additional.write_log_file('The Player has reached level {}'.format(level))
            return count_of_wariors
        else: additional.write_log_file('Game was started with 0 level')

    death_flag = False
    running = True
    count_of_wariors = generate_wariors(False)
    count_of_alive = count_of_wariors
    freaze_game = True
    pause_flag = False
    start_game_time = pygame.time.get_ticks()
    down = False
    down_flag = False
    change_mode = False

    direction = False
    direction_flag = False

    advise_font = pygame.font.Font(None, 25)
    advise_table = advise_font.render('Press ESC to pause', 1, settings.colours.DeepPink)
    advise_coord = advise_table.get_rect(center=(settings.WIDTH - 100, settings.HEIGHT - 10))

    def change_smth(return_dict):
        nonlocal running, character, freaze_game, death_flag, shell_objects, stat, all_sprites, \
            CURRENT_SCORE, pause_flag, start_game_time, last_shell
        for var, val in return_dict.items():
            if var == 'running': running = val
            elif var == 'character': character = val
            elif var == 'freaze_game': freaze_game = val
            elif var == 'pause_flag': pause_flag = val
            elif var == 'death_flag': death_flag = val
            elif var == 'shell_objects': shell_objects = val
            elif var == 'all_sprites': all_sprites = val
            elif var == 'stat': stat = val
            elif var == 'start_game_time': start_game_time = val
            elif var == 'current_score': start_game_time = pygame.time.get_ticks() - val * 100
            elif var == 'last_shell': last_shell = val

    additional.write_log_file('Game window was opened')

    while running:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            return_dict = game_functions.check_event(pygame, event, stat, freaze_game,
                                                     pause_flag, death_flag, character, start_button, shell_objects,
                                                     all_sprites, shell_object_img, CURRENT_SCORE, last_shell)
            if return_dict != {}: change_smth(return_dict)

        if not freaze_game:
            action_from_obj = True
            hits_shell = pygame.sprite.groupcollide(shell_objects, fall_objects, True, True, pygame.sprite.collide_mask)
            hits_character = pygame.sprite.spritecollide(character, fall_objects, True, pygame.sprite.collide_mask)

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
                score_table = first_font.render('Your reached score : {}'.format(CURRENT_SCORE), 1,
                                                settings.colours.black, settings.colours.orange)

                if settings.sounds:
                    length = pygame.mixer.Sound.get_length(end_music)
                else:
                    length = settings.character_death_time
                seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                if length <= seconds:
                    freaze_game = True
                    stat.add_max_score(CURRENT_SCORE)
                    stat.add_level(character.level)
            else:
                if hits_character:
                    character.lives = 0
                if hits_shell:
                    kill_fall_object += 1
                    count_of_shells = additional.read_temp_file(settings.files.temp_count_of_shells)[0]
                    if count_of_shells > 0:
                        count_of_shells -= 1
                    else:
                        count_of_shells = 0
                    additional.write_temp_file(settings.files.temp_count_of_shells, count_of_shells)

                    character.killed_objects += 1
                    if not character.killed_objects == count_of_wariors and settings.sounds: hit_sound.play()
                    count_of_alive -= 1
                if character.lives == 0:
                    character.death()
                    if settings.sounds:
                        pygame.mixer.music.pause()
                        end_music.play()
                    start_ticks = pygame.time.get_ticks()
                    blackscreen.set_alpha(200)
                    last = ''
                    character.character_left_img = character_death_img
                    character.character_right_img = character_death_img
                    death_flag = True
                    if character.lives == 0:
                        reason_pic = reason_pic_died
                        additional.write_log_file('Game over at level {}'.format(character.level + 1))

            all_sprites.update()
            if not death_flag:
                screen.blit(background_img, (0, 0))
            else:
                screen.blit(background_img, (0, 0))
                screen.blit(blackscreen, (0, 0))
                reason_pic.set_colorkey(settings.colours.transparency)
                screen.blit(reason_pic, (0, 0))
                screen.blit(score_table, (settings.HEIGHT // 2, settings.WIDTH // 2 - 500))

            all_sprites.draw(screen)

            if not death_flag:
                # SCORE TABLE ADDING
                CURRENT_SCORE = (pygame.time.get_ticks() - start_game_time) // 100
                first_font = pygame.font.Font(None, 50)
                score_table = first_font.render('Score : {}'.format(CURRENT_SCORE), 1, settings.colours.black, settings.colours.orange)
                second_font = pygame.font.Font(None, 50)
                level_table = second_font.render('Level : {}'.format(character.level), 1, settings.colours.black, settings.colours.orange)

                screen.blit(score_table, (20, 30))
                screen.blit(level_table, (settings.WIDTH//2 + 200, 30))

                screen.blit(advise_table, advise_coord)

                if direction_flag:
                    direction = not direction
                    direction_flag = False
                if down_flag:
                    down_flag = False
                    down = not down
            if (character.killed_objects == count_of_wariors or count_of_alive == 0 or action_from_obj) \
                    and not death_flag:
                if settings.sounds: complete_sound.play()
                character.killed_objects = 0
                character.level += 1
                count_of_alive = new_game(character.level + 1)
        else:
            if pause_flag:
                pause_font = pygame.font.Font(None, 75)
                pause_table = pause_font.render(settings.pause_button_text, 1, settings.colours.MistyRose)
                pause_coord = pause_table.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))

                first_font = pygame.font.Font(None, 50)
                score_table = first_font.render('Your score now : {}'.format(CURRENT_SCORE), 1, settings.colours.MistyRose)
                score_coord = score_table.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 100))

                second_font = pygame.font.Font(None, 50)
                level_table = second_font.render('Level now : {}'.format(character.level), 1, settings.colours.MistyRose)
                level_coord = level_table.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 150))
                if settings.start.show_animation: pause_objects.update()
                screen.blit(background_img, (0, 0))
                all_sprites.draw(screen)
                screen.blit(blackscreen, (0, 0))
                if settings.start.show_animation: pause_objects.draw(screen)
                screen.blit(pause_table, pause_coord)
                screen.blit(score_table, score_coord)
                screen.blit(level_table, level_coord)

            else:
                if death_flag:
                    if settings.sounds: pygame.mixer.music.pause()
                    count_of_wariors = generate_wariors(False)
                    character.kill()
                    character = Character(0, character_right_img, character_left_img, character_death_img)
                    all_sprites.add(character)
                death_flag = False
                blackscreen.set_alpha(200)
                
                main_first_font = pygame.font.Font(None, 50)
                main_score_table = main_first_font.render('Your best score : {}'.format(stat.max_score), 1, settings.colours.black, settings.colours.orange)
                main_second_font = pygame.font.Font(None, 50)
                main_level_table  = main_second_font.render('Your best level : {}'.format(stat.max_level), 1, settings.colours.black, settings.colours.orange)

                screen.blit(background_img, (0, 0))
                screen.blit(blackscreen, (0, 0))
                
                screen.blit(main_score_table, (int(settings.WIDTH*0.65), settings.HEIGHT//2 - 40))
                screen.blit(main_level_table, (int(settings.WIDTH*0.65), settings.HEIGHT//2))

                start_button = Button(screen, settings.colours.black,
                                      (settings.WIDTH - settings.start_button_width) // 2,
                                      (settings.HEIGHT - settings.start_button_height) // 2,
                                      settings.start_button_width, settings.start_button_height, 100,
                                      settings.start_button_text, settings.colours.white)
                all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()

    if change_mode: game_making(mode)


if __name__ == '__main__':
    try: game_making(random.randint(1, 3))
    except pygame.error: additional.write_log_file('Game was closed after showing statistics')
else: additional.write_log_file('Attempt to open main file from non-main')
