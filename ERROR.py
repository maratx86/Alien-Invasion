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
    print('You can play in game all necessary libs exist')
else:
    print("\nSome library is missing...\a")
    raise SystemExit(10)