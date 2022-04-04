import configparser
import os
import pathlib

# os.environ['COLLABOS_SRC'] = str(pathlib.Path(__file__).parent.parent.resolve())
os.environ['COLLABOS_SRC'] = "D:\\Collabos\\backend\\collabos"

CONFIG_DIR = os.path.join(os.environ['COLLABOS_SRC'], 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_DIR)

