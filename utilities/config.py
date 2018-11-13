import configparser


def init():
    global CONFIGURATION
    CONFIGURATION = configparser.ConfigParser()
    CONFIGURATION.read('utilities/general_config.ini')
