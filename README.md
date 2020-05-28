# Alien-Invasion
Pygame Project 

The Alien Invasion game consists in the battle of your ship with foreign wariors who want to kill you. If they reach your "front", then you will immediately die at the hands of the enemy. To survive, you need to destroy the entire enemy fleet by shooting at it (spacebar) and moving (left / right keys)

Until you have started the game, you can look at the statistics by pressing the F5 button, and you will be presented with a statistics window, and after closing this window, you will get a new game window and the appearance of the character and enemies can change there, this is done for greater interactivity .

You can also pause the game by pressing the ESC key.

For an emergency exit from the game with saving statistics, press the DEL key.

You can turn off the sound by setting the sounds setting to False, and you can also adjust the volume by setting the sounds_volume variable from 0 to 100 (initially 25)


# Description of used modules

alien.py - the main game file with the main code.

button.py - file for storing the structure of the Button class. This class is used to create a button on the home screen. It contains methods for writing text on a button, rendering on the screen, and for checking its click.
bullet.py - file for storing the structure of the ShellObject class. This class is used to create bullets. It contains a method for updating.
character.py is a file for storing the structure of the Character class. This class is used to create a player’s ship. It contains methods for updating the position, and side classes for changing the position itself (go left / right, jump), as well as a method for displaying the death of a player.
game_functions.py - file for storing the event handling function from the keyboard.
settings.py - file for storing the structure of the Settings, Colors, StartSettings, StatisticSettings class, which contain the basic settings for controlling the game (Screen expansion, speed of objects, colors, etc.).
statistic.py - file for storing the structure of the Stat class. This class is used for statistics. It contains methods for adding statistics, such as points per game and level, and it also contains a method of overwriting a file to save the results for the next game.
show_statistic.py - a file for displaying game statistics in the form of diagrams with points and achieved levels, contains methods. It contains 2 classes, one displays the Pygame window, and the other creates the desired number of columns using the saved data from the Stat () class.
additional.py - an additional module with auxiliary functions.
statistics_reset.py - an additional file for resetting statistics.
animation.py is a file for storing the structure of the Animation class, which allows you to combine several images into one object and displays them sequentially (like GIF).
create_animation_code.py - a file in which all images are unloaded and translates into an object and returns it.
