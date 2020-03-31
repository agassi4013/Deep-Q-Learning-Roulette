import configparser
import os

# Vars
config = configparser.ConfigParser()
configPath = os.path.expanduser('~') + '/.roulette'


def getConfig():
    """
        Will return a user config and set a default if necessary
    """

    # Generate a default config the first time
    if not os.path.isfile(configPath):
        setDefaultConfigFile()

    # Load existing config
    config.read(configPath)
    return config['MAIN']


def setDefaultConfigFile():
    """
        Set a user default config file
    """

    config['MAIN'] = {
        'bank': '1000'
    }

    # Save
    saveConfig()


def update(name, value):
    """
        Update a config value
    """

    # Set new value
    config['MAIN'][name] = str(value)

    # Save
    saveConfig()


def saveConfig():
    """
        Save user config to a file
    """

    with open(configPath, 'w') as configfile:
        config.write(configfile)
    os.chmod(configPath, 0o600)
