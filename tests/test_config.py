from config_importer import *


def print_cfg(cfg):
    print("Config(\"%s\"[" % cfg.name)
    for field in cfg.field_cfgs:
        print("FieldCfg(\"%s\", %s, \"%s\", %s, %s)" %
              (field.name, field._shortkey, field.observable_field, field._addmode, field.dataprov_type))

    print("])")


config_path_in = "../tests/support/test_config.xml"
config_path_out = "../tests/support/test_config_out.xml"


def test_cfg_read_write():
    cfg_importer = ConfigImproter(config_path_in)

    cfg_importer.read()
    cfg_list = cfg_importer.cfg_list

    assert len(cfg_list) != 0

    for cfg in cfg_list:
        print_cfg(cfg)

    #change names of the fields inside first config
    cfg = cfg_list[0]

    i = 0
    for field in cfg.field_cfgs:
        field.name = "ChangedName " + str(i)
        i += 1

    # change name of the config file not to owerwrite exisiting test config
    cfg_importer._path = config_path_out
    cfg_importer.write()

test_cfg_read_write()