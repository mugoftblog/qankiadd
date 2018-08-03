from config_importer import *
import os
import shutil
import time


def print_cfg(cfg):
    print("Config(\"%s\"[" % cfg.name)
    for field in cfg.field_cfgs:
        print("FieldCfg(\"%s\", %s, \"%s\", %s, %s)" %
              (field.name, field._shortkey, field.observable_field, field._addmode, field.dataprov_type))

    print("])")


CONFIG_PATH_IN = "../tests/support/test_config.xml"
CONFIG_PATH_OUT = "../tests/support/test_config_out.xml"


def __delete_config_out():
    # try to remove the output directory with all files inside
    if os.path.exists(CONFIG_PATH_OUT):
        print("Deleting output directory")
        shutil.rmtree(CONFIG_PATH_OUT, ignore_errors=True)
        t = 0
        # wait max 5 seconds until directory is deleted
        while os.path.exists(CONFIG_PATH_OUT) and t < 5:  # check if it exists
            t += 0.5
            time.sleep(0.5)

def test_cfg_read_write():
    """
    Preconditions:
        - configuration file with 1 configuation, 3 fields, "save all" hotkey,
        "clear all" hotkey, "quit" hotkey
        - input path to the configuration file is not the same as output path to the configuration file
    Procedure:
        - import configuration file from input path
        - export configuration file to the output path
    Explanation:
        all hotkeys and all configurations with all fields should be imported successfully
        and we don't care about case sensitivity.
    Expectation:
        - the size of the input configuration file and the size of the output configuration file are equal
    """
    cfg_importer = ConfigImproter(CONFIG_PATH_IN)

    cfg_importer.read()
    cfg_list = cfg_importer.cfg_list

    assert len(cfg_list) == 1

    for cfg in cfg_list:
        print_cfg(cfg)

    #change names of the fields inside first config
    cfg = cfg_list[0]

    i = 0
    for field in cfg.field_cfgs:
        field.name = "ChangedName " + str(i)
        i += 1

    # change name of the config file not to owerwrite exisiting test config

    __delete_config_out() # test if working correctly

    cfg_importer._path = CONFIG_PATH_OUT
    cfg_importer.write()

test_cfg_read_write()