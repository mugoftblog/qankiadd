from models import *
from config import *

from dataprov.dataprov_factory import *

#fields hotkeys
HOTKEY_QUESTION = ("ctrl", "b")
HOTKEY_ANSWER = ("ctrl", "spacebar")


text_test_normal = "Test"
text_test_special_chars = "Ein Beiespiel: königsee ärzte übersetzer"

def print_cfg(cfg):
    for field in cfg.field_cfgs:
        print("FieldCfg(\"%s\", HOTKEY, \"%s\")" % (field.name, field.observable_name))

def get_cfg():
    cfg = Config("Foreign Language",
                 [FieldCfg("Question", HOTKEY_QUESTION, "WrongName", Addmode.I, DataProvTypes.MANUAL),  #observer with specified name doesn't exit
                  FieldCfg("Definition", HOTKEY_QUESTION, "Definition", Addmode.I, DataProvTypes.MANUAL),  #observer name is the same as field name
                  FieldCfg("Answer", HOTKEY_ANSWER, "Question", Addmode.I, DataProvTypes.GOOGLETRANS),
                  FieldCfg("Answer", HOTKEY_ANSWER, "Question", Addmode.I, DataProvTypes.GOOGLETRANS),  #field name is the same, as previous field name
                  FieldCfg("Picture", HOTKEY_ANSWER, "Sound", Addmode.I, DataProvTypes.GOOGLETRANS),
                  FieldCfg("Sound", HOTKEY_ANSWER, "Picture", Addmode.I, DataProvTypes.GOOGLETRANS)
                  ],
                 False)
    return cfg

def test_models_unique():
    "After Model Manager is created all config names should be unique"
    print("\n    test_models_unique")
    cfg = get_cfg()
    model_mng = ModelManager(cfg)

    assert cfg.field_cfgs[0].observable_name is not "", "Still wrong observable name %s" % cfg.field_cfgs[0].observable_name

    names_set = set()

    i = 0
    for cfg_field in cfg.field_cfgs:
        assert cfg_field.name not in names_set, "Cfg %u should contain unique name" % i
        names_set.add(cfg_field.name)
        i+=1

    assert cfg.field_cfgs[1].observable_name != cfg.field_cfgs[1].name,\
           "Field \"%s\" has the same name as observable_name" % \
           cfg.field_cfgs[1].name

    assert cfg.field_cfgs[5].observable_name == "", "Observable name should be reseted. otherwise recursion (both fields add each other as observers)"

    print_cfg(cfg)

def test_models_set_text():
    """Text should be correctly set to the field: all observers should be updated,
    in case text is too long it should be shortened"""
    print("\n    test_models_set_text")
    cfg = get_cfg()
    model_mng = ModelManager(cfg)

    field = model_mng.get_field("Question")
    assert field != None

    field.set_text(text_test_normal)

    assert field.get_text() == text_test_normal, "Expect to see text \n \"%s\" \n but see\n \"%s\" " % \
                                                 (text_test_normal, field.get_text())

    text_test_long = "A" * (field.get_text_max() + 1)
    field.set_text(text_test_long)

    #set text should be shortened to the max length
    assert field.get_text() == text_test_long[:field.get_text_max()]
    #set text should be set to all observers


    observable_field = model_mng.get_field("Question")
    observer_field = model_mng.get_field("Answer")
    assert observable_field.get_text() == observer_field.get_text(),\
           "Observer field \"%s\" should contain the same text as Observable field \"%s\":\n Text1: %s\n Text2: %s" % \
           (observer_field.cfg.name, observable_field.cfg.name,observer_field.get_text(), observable_field.get_text())


def test_models_dataproviders():
    print("\n    test_models_dataproviders")
    cfg = get_cfg()
    model_mng = ModelManager(cfg)
    field = model_mng.get_field("Picture")
    assert field != None

    dataprov = get_dataprov_factory(field.cfg.dataprov_type)

    assert dataprov != None


    dataprov.update_data(text_test_normal)
    text = dataprov.get_data()
    print(text)

    field.set_text(text_test_normal)

test_models_unique()
test_models_set_text()
test_models_dataproviders()