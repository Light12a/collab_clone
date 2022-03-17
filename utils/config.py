import configparser
import os
import pathlib

os.environ['COLLABOS_SRC'] = str(pathlib.Path(__file__).parent.parent.resolve())

CONFIG_DIR = os.path.join(os.environ['COLLABOS_SRC'], 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_DIR)

