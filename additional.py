import os


'''
This module using for additional functions and contain this functions
    check_int
        return for you True if number may to tranform into int()
    directory_finder
        return you dictionary with all necessary paths
    check_settings
        import all necessary data from "settings" file
'''


def check_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def directory_finder():
    from sys import platform

    if platform == "win32":
        _os_ = "windows"
        main_dir = os.getcwd()
        media_dir = main_dir + "\\media\\"
        shop_dir = media_dir + "shop\\"
        mode_dir = media_dir + "mode\\"
        slash = '\\'
        temp_dir = os.getenv('TEMP')
        if temp_dir == None: temp_dir = os.getenv('TMP')
        temp_dir += slash
    # ~ elif platform == "darwin": _os_ = "OS X"
    else:
        _os_ = "linux or MacOS"
        main_dir = os.getcwd()
        media_dir = main_dir + "/media/"
        shop_dir = media_dir + "shop/"
        mode_dir = media_dir + "mode/"
        slash = "/"
        temp_dir = os.getenv('TEMP')
        if temp_dir == None: temp_dir = os.getenv('TMP')
        temp_dir += slash
    directories = {
        "os":_os_,
        "platform": platform,
        "slash": slash,
        "temp_dir": temp_dir,
        "main_dir": main_dir,
        "media_dir": media_dir,
        "shop_dir": shop_dir,
        "mode_dir": mode_dir
    }
    return directories


def check_settings():
    f = open('settings')
    data = f.read()
    f.close()
    data = data.split('\n')

    keys_name = ['save_stat', 'WIDTH', 'HEIGHT', 'FPS']
    settings_dict = {}
    for i in range(len(data)):
        temp = data[i].split(' ')
        first_word = temp[0]
        if data[i] != '':
            if data[i].split(' ')[-1] == 'Yes': settings_dict[keys_name[i]] = True
            else: settings_dict[keys_name[i]] = False
            if first_word in keys_name:
                for one in keys_name:
                    if one == first_word:
                        num = temp[-1]
                        if check_int(num): settings_dict[first_word] = int(num)
                        else: print('Settings not correct')

    return settings_dict

