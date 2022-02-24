import configparser
import os

CONFIG_DIR = os.path.join(os.environ['COLLABOS_SRC'], 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_DIR)
