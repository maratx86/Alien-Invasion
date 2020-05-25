class Files():
    def __init__(self):
        self.temp_count_of_shells = 'count_of_shell.ai'


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

        self.transparency = self.black

class StatisticSettings:
    def __init__(self, settings):
        self.WIDTH = settings.WIDTH // 3
        self.HEIGHT = settings.HEIGHT

        self.skip_edge = 20
        self.width = 5

        self.colour_column_score = settings.colours.black
        self.colour_column_level = settings.colours.green
        self.colour_background = settings.colours.PeachPuff


class Settings:
    def __init__(self):
        self.game_name = ''
        self.saving_after_quit = False
        self.sounds = True
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.FPS = 30

        self.start_button_width = 250
        self.start_button_height = 100
        self.start_button_text = 'Start game'

        self.character_position = (self.WIDTH // 2, 100)
        self.max_count_of_shells = 3
        self.colours = Colours()

        self.statistic = StatisticSettings(self)

        self.files = Files()