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


def __delete_config(path):
    # try to remove the output directory with all files inside
    if os.path.exists(path):
        print("Deleting output directory")
        shutil.rmtree(path, ignore_errors=True)
        t = 0
        # wait max 5 seconds until directory is deleted
        while os.path.exists(path) and t < 5:  # check if it exists
            t += 0.5
            time.sleep(0.5)


############################################ test SIMPLE ##############################################################
CONFIG_SIMPLE_PATH_IN = "../tests/support/test_config_simple.xml"
CONFIG_SIMPLE_PATH_OUT = "../tests/support/test_config_simple_out.xml"


def test_cfg_simple():
    """
    Preconditions:
        - configuration file with 2 configuations, "save all" hotkey,
        "clear all" hotkey, "quit" hotkey
    Procedure:
        - import configuration file from input path
        - export configuration file to the output path
        - compare two files
    Explanation:
        all hotkeys and all configurations with all fields should be imported successfully
        and we don't care about case sensitivity.
    Expectation:
        - the size of the input configuration file and the size of the output configuration file are equal
    """
    cfg_importer = ConfigImproter(CONFIG_SIMPLE_PATH_IN)

    cfg_importer.read()
    cfg_list = cfg_importer.cfg_list

    assert len(cfg_list) == 2, "two imported configurations are expected, but got %u" % len(cfg_list)

    for cfg in cfg_list:
        print_cfg(cfg)

    #change names of the fields inside first config
    cfg = cfg_list[0]

   # i = 0
   # for field in cfg.field_cfgs:
    #    field.name = "ChangedName " + str(i)
   #     i += 1

    # change name of the config file not to owerwrite exisiting test config

    __delete_config(CONFIG_SIMPLE_PATH_OUT)

    cfg_importer._path = CONFIG_SIMPLE_PATH_OUT
    cfg_importer.write()

    statinfo_in = os.stat(CONFIG_SIMPLE_PATH_IN)
    statinfo_out = os.stat(CONFIG_SIMPLE_PATH_OUT)

    assert statinfo_in.st_size == statinfo_out.st_size, "the size of the exported file (%u) is not equal" \
                                                        " to the size of the imported file (%u)" % \
                                                        (statinfo_out.st_size, statinfo_in.st_size)


############################################ test WRONG ELEMENTS ####################################################
CONFIG_WRONG_ELEMS_PATH_IN = "../tests/support/test_config_wrong_elems.xml"
CONFIG_WRONG_ELEMS_PATH_EXPECT = "../tests/support/test_config_wrong_elems_expect.xml"
CONFIG_WRONG_ELEMS_PATH_OUT = "../tests/support/test_config_wrong_elems_out.xml"


def test_cfg_wrong_elems():
    """
    Preconditions:
        - configuration file which contains not existing attributes + not existing elements
    Procedure:
        - import configuration file from input path
        - export configuration file to the output path
        - compare exported comfiguration file with the expected configuration file
    Explanation:
        all not existing attributes and elements have to be ignored during importing
    Expectation:
        - the size of the exported comfiguration file is equal to the size of the expected configuration file
    """

    cfg_importer = ConfigImproter(CONFIG_WRONG_ELEMS_PATH_IN)

    cfg_importer.read()
    cfg_list = cfg_importer.cfg_list

    assert len(cfg_list) == 1, "two imported configurations are expected, but got %u" % len(cfg_list)

    for cfg in cfg_list:
        print_cfg(cfg)

    # change names of the fields inside first config
    cfg = cfg_list[0]

    # i = 0
    # for field in cfg.field_cfgs:
    #    field.name = "ChangedName " + str(i)
    #     i += 1

    # change name of the config file not to owerwrite exisiting test config

    __delete_config(CONFIG_WRONG_ELEMS_PATH_OUT)

    cfg_importer._path = CONFIG_WRONG_ELEMS_PATH_OUT
    cfg_importer.write()

    statinfo_expect = os.stat(CONFIG_WRONG_ELEMS_PATH_EXPECT)
    statinfo_out = os.stat(CONFIG_WRONG_ELEMS_PATH_OUT)

    assert statinfo_expect.st_size == statinfo_out.st_size, "the size of the exported file (%u) is not equal" \
                                                        " to the size of the exported file (%u)" % \
                                                        (statinfo_out.st_size, statinfo_expect.st_size)


############################################ TESTS EXECUTION ##########################################################
test_cfg_simple()
test_cfg_wrong_elems()