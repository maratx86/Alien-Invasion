import show_statistic
import random
import additional
from alien import game_making
from bullet import ShellObject

settings = additional.check_settings()


def check_event(pygame, event, stat, freaze_game, pause_flag, death_flag, character,
                start_button, shell_objects, all_sprites, shell_object_img, CURRENT_SCORE, start_game_time):
    return_dict = {}
    if event.type == pygame.QUIT:
        return_dict['running'] = False
        if settings.saving_after_quit: stat.rewrite_file()
        else: print('Your flag save statistic is turned off, your progress was not saved')

    if freaze_game:
        if pause_flag:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_dict['current_score'] = stat.plus_temp()
                    return_dict['pause_flag'] = False
                    return_dict['freaze_game'] = False
                    print('Unpaused game')
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    if stat.max_score != 0 and stat.max_level != 0:
                        ss = show_statistic.ShowStat()
                        ss.show(stat)
                        game_making(random.randint(1, 3))
                    print('You have no statistic')
                elif event.key == pygame.K_SPACE:
                    start_game_time = pygame.time.get_ticks()
                    character.lives = 1
                    if settings.sounds: pygame.mixer.music.unpause()
                    character.rect.center = settings.character_position
                    return_dict['freaze_game'] = False
                    return_dict['character'] = character
                    return_dict['start_game_time'] = start_game_time
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.pressed(pygame.mouse.get_pos()):
                    start_game_time = pygame.time.get_ticks()
                    return_dict['start_game_time'] = start_game_time
                    character.lives = 1
                    if settings.sounds: pygame.mixer.music.unpause()
                    character.rect.center = settings.character_position
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
                elif event.key == pygame.K_RIGHT:
                    character.go_right()
                    return_dict['character'] = character
                elif event.key == pygame.K_SPACE:
                    count_of_shells = additional.read_temp_file(settings.files.temp_count_of_shells)[0]
                    if count_of_shells < settings.max_count_of_shells:
                        count_of_shells += 1
                        additional.write_temp_file(settings.files.temp_count_of_shells, count_of_shells)
                        shell_object = ShellObject(shell_object_img, character)
                        shell_objects.add(shell_object)
                        all_sprites.add(shell_objects)
                        return_dict['shell_objects'] = shell_objects
                        return_dict['all_sprites'] = all_sprites
                        return_dict['character'] = character
                elif event.key == pygame.K_ESCAPE:
                    stat.add_temp_score(CURRENT_SCORE)
                    return_dict['pause_flag'] = True
                    return_dict['freaze_game'] = True
                    return_dict['stat'] = stat

                elif event.key == pygame.K_DELETE:
                    print('DEL save data')
                    stat.add_max_score(CURRENT_SCORE)
                    stat.add_level(character.level)
                    # ~ running = False
                    return_dict['running'] = False
                    return_dict['stat'] = stat
                    stat.rewrite_file()

                '''
                # For testing death
                if event.key == pygame.K_KP_ENTER:
                    character.lives = 0
                    return_dict['character'] = character
                '''

    return return_dict
