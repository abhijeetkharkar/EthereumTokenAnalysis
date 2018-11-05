import configparser


def init():
    global CONFIGURATION
    CONFIGURATION = configparser.ConfigParser()
    CONFIGURATION.read('config_files/general_config.ini')
