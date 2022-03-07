import configparser
import os

os.environ['COLLABOS_SRC'] = "D:\\TMA project\\collabos"

CONFIG_DIR = os.path.join(os.environ['COLLABOS_SRC'], 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_DIR)

