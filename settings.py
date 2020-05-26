class Files():
    def __init__(self):
        self.temp_count_of_shells = 'count_of_shell.ai'
        self.temp_count_of_objects = 'count_of_objects.ai'
        self.log_file = 'log.ai.txt'


class Colours:
    def __init__(self):
        self.black = (0, 0, 0)
        self.PeachPuff = (255, 218, 185)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.light_blue = (0, 255, 255)
        self.pink = (255, 100, 180)
        self.orange = (255, 100, 10)
        self.yellow = (255, 255, 0)
        self.MistyRose = (255, 228, 225)
        self.HotPink = (255, 105, 180)
        self.DeepPink = (255, 20, 147)
        self.LightSalmon = (255, 160, 122)
        self.Crimson = (220, 20, 60)
        self.DarkGrey = (24, 24, 24)
        self.loading = (255, 160, 122)

        self.transparency = self.black


class StatisticSettings:
    def __init__(self, settings):
        self.WIDTH = settings.WIDTH // 3
        self.HEIGHT = settings.HEIGHT

        self.skip_edge = 50
        self.width = 5
        self.coord_width = 1

        self.colour_column_score = settings.colours.LightSalmon
        self.colour_column_level = settings.colours.Crimson
        self.colour_background = settings.colours.PeachPuff


class StartSettings:
    def __init__(self):
        self.falling_bullet_speed = 10
        self.falling_object_speed = 5
        self.action_object_speed = 5
        self.character_speed = 5
        self.increaze_falling_speed = True
        self.show_animation = True  # The game will load longer


class Settings:
    def __init__(self):
        self.game_name = 'Alien Invasion'
        self.show_sreen = True
        self.show_mode = True

        self.saving_after_quit = False
        self.double_wall = False  # True -> Falling Objects should collide 2 times with the wall (both left and right)
        self.sounds = True
        self.sounds_volume = 25  # Number from 1 to 100

        self.WIDTH = 1080
        self.HEIGHT = 720
        self.FPS = 30

        self.start_button_width = 250
        self.start_button_height = 100
        self.start_button_text = 'Start game'
        self.pause_button_text = 'The game was paused'
        self.loading_text = 'Game is loading...'

        self.character_position = (self.WIDTH // 2, 100)
        self.character_death_time = 3  # Time how much the character will jump after death (seconds)
        self.max_count_of_shells = 5

        self.colours = Colours()
        self.statistic = StatisticSettings(self)
        self.files = Files()
        self.start = StartSettings()
