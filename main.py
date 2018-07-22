#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Ivan Gushchin"
__copyright__ = ""
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Ivan Gushchin"
__email__ = "mug0ft10@gmail.com"


import logging
from config import *
from config_importer import *
from exporting.anki import *
from keylistener import *
from models import *

LOG_FORMAT = "[%(asctime)s  - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='debug.log', format=LOG_FORMAT, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
# logging.basicConfig(filename='qankiadd.log', level=logging.INFO)
# logging.basicConfig(filename='qankiadd.log', level=logging.ERROR)
# logging.basicConfig(filename='qankiadd.log', level=logging.WARNING)

CONFIG_PATH_IN = "config.xml"

# TODO more elegant way to have singleton of the Application
keylstnr = None

def start_app(cfg):
    global keylstnr
    keylstnr = Keylistener()
    #keylstnr.register_keys()
    #keylstnr.start_listening()


def ensure_config_file(path):
    # Ensure configuration file exists.
    if not os.path.isfile(path):
        logging.error('Error getting configuration file: \"%s\"' % path)
        sys.exit(1)


def main():
    # set up logger
    # read configuration file
    cfg_importer = ConfigImproter(CONFIG_PATH_IN)
    cfg_importer.read()
    cfg_list = cfg_importer.cfg_list

    print('Please select the configuration:')
    i = 0
    for cfg in cfg_list:
        print("%u. %s" % (i, cfg.name))
        i += 1

    try:
        i = int(input(""))
    except ValueError as e:
        logging.error(e)
        sys.exit(1)

    if i >= 0 and i < len(cfg_list):
        print("Program is started")
        cfg = cfg_list[i]

        anki = AnkiExporter()
        model_mngr = ModelManager(cfg, anki)

        keylisten = Keylistener()
        keylisten.register_observer(model_mngr)
        for field in model_mngr.get_fields():
            keylisten.register_observer(field)

        keylisten.start_listening()
    else:
        logging.error("Wrong configuration index is entered: %s" % i)
        sys.exit(1)


if __name__ == '__main__':
    main()
