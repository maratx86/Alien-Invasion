import pygame
import show_statistic
import random
import additional
from alien import ShellObject, game_making

settings = additional.check_settings()

def check_event(event, stat, freaze_game, pause_flag, death_flag, character,
                start_button, shell_objects, all_sprites, shell_object_img, CURRENT_SCORE):
    ['running', 'character', 'freaze_game', 'death_flag', 'shell_objects', 'stat']
    return_dict = {}
    if event.type == pygame.QUIT:
        # ~ running = False
        return_dict['running'] = False
        if settings.saving_after_quit: stat.rewrite_file()
        else: print('Your flag save statistic is turned off, your progress was not saved')

    if freaze_game:
        if pause_flag:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # return_dict['current_score'] = 0
                    return_dict['pause_flag'] = False
                    return_dict['freaze_game'] = False
                    print('unpaused game')
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    ss = show_statistic.ShowStat()
                    ss.show(stat)
                    stat.rewrite_file()
                    game_making(random.randint(1, 3))
                if event.key == pygame.K_SPACE:
                    start_game_time = pygame.time.get_ticks()
                    character.lives = 1
                    pygame.mixer.music.unpause()
                    character.rect.center = settings.character_position
                    return_dict['freaze_game'] = False
                    return_dict['character'] = character
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.pressed(pygame.mouse.get_pos()):
                    start_game_time = pygame.time.get_ticks()
                    character.lives = 1
                    pygame.mixer.music.unpause()
                    character.rect.center = settings.character_position
                    # ~ freaze_game = False
                    return_dict['freaze_game'] = False
                    return_dict['character'] = character

    else:
        if death_flag:
            0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    character.go_left()
                    return_dict['character'] = character
                if event.key == pygame.K_RIGHT:
                    character.go_right()
                    return_dict['character'] = character
                if event.key == pygame.K_SPACE:
                    count_of_shells = additional.read_temp_file('count_of_shell.ai')[0]
                    if count_of_shells < settings.max_count_of_shells:
                        count_of_shells += 1
                        additional.write_temp_file('count_of_shell.ai', count_of_shells)
                        shell_object = ShellObject(shell_object_img, character)
                        shell_objects.add(shell_object)
                        all_sprites.add(shell_objects)
                        # ~ ['shell_objects', 'all_sprites']
                        return_dict['shell_objects'] = shell_objects
                        return_dict['all_sprites'] = all_sprites
                        return_dict['character'] = character
                if event.key == pygame.K_ESCAPE:
                    stat.add_temp_score(CURRENT_SCORE)
                    # ~ pause_flag = True
                    # ~ freaze_game = True
                    return_dict['pause_flag'] = True
                    return_dict['freaze_game'] = True
                    return_dict['stat'] = stat
                if event.key == pygame.K_ESCAPE:
                    stat.add_temp_score(CURRENT_SCORE)
                    # ~ pause_flag = True
                    # ~ freaze_game = True
                    return_dict['pause_flag'] = True
                    return_dict['freaze_game'] = True

                    return_dict['stat'] = stat
                if event.key == pygame.K_DELETE:
                    print('DEL save data')
                    stat.add_max_score(CURRENT_SCORE)
                    stat.add_level(character.level)
                    # ~ running = False
                    return_dict['running'] = False
                    return_dict['stat'] = stat
                    stat.rewrite_file()
                start_no_move_time = pygame.time.get_ticks()

    return return_dict
