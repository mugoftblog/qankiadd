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
from gui import *
from keylistener import *
from models import *



# TODO more elegant way to have singleton of the Application
gui_obj = None
keylstnr_obj = None

def start_app(cfg):
    global gui_obj
    gui_obj = Gui(cfg)
    global keylstnr_obj
    keylstnr_obj = Keylistener(gui_obj)
    keylstnr_obj.register_keys()
    keylstnr_obj.start_listening()


"""def ensure_config_file(config_dir: str) -> str:
    Ensure configuration file exists.
    import homeassistant.config as config_util
    config_path = config_util.ensure_config_exists(config_dir)

    if config_path is None:
        print('Error getting configuration path')
        sys.exit(1)

    return config_path"""


def main():
    logging.basicConfig(filename='qankiadd.log', level=logging.INFO)
    print('Please select the configuration:')
    i = 0
    for cfg in configurations:
        print("%u. %s" % (i, cfg.name))
        i += 1

    # i = int(input(""))
    i = 0

    if i >= 0 and i < len(configurations):
        print("Process is started")
        cfg = configurations[i]
        model = ModelManager(cfg)
        #start_app(cfg)
    else:
        print("Wrong value is entered")


if __name__ == '__main__':
    main()
