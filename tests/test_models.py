from models import *
from config import *
from tests.stubs.exporting.anki import *
import win32clipboard

from dataprov.factory import *

#fields hotkeys
HOTKEY_QUESTION = ("ctrl", "b")
HOTKEY_ANSWER = ("ctrl", "spacebar")


text_test_normal = "Test"
text_test_special_chars = "Ein Beiespiel: königsee ärzte übersetzer"


############################################ test UNIQUE ##############################################################
cfg_not_unique = Config("Not unique names",
             [FieldCfg("Question", HOTKEY_QUESTION, "WrongName", AddMode.Ignore, None), # observer with specified name doesn't exit
              FieldCfg("Definition", HOTKEY_QUESTION, "Definition", AddMode.Ignore, AddMode.Append),  #observer name is the same as field name
              FieldCfg("Answer", HOTKEY_ANSWER, "Question", AddMode.Ignore, None),
              FieldCfg("Answer", HOTKEY_ANSWER, "Question", AddMode.Ignore, None),  #field name is the same, as previous field name
              FieldCfg("Picture", HOTKEY_ANSWER, "Sound", AddMode.Ignore, DataProvType.Googletranslate),
              FieldCfg("Sound", HOTKEY_ANSWER, "Picture", AddMode.Ignore, DataProvType.Googletranslate)
              ],
             False)


def test_models_unique():
    "After Model Manager is created all config names should be unique"
    print("\n    test_models_unique")
    model_mng = ModelManager(cfg_not_unique, AnkiExporterStub())

    assert cfg_not_unique.field_cfgs[0].observable_field is not "", "Still wrong observable name %s" % cfg_not_unique.field_cfgs[0].observable_field

    names_set = set()

    i = 0
    for cfg_field in cfg_not_unique.field_cfgs:
        assert cfg_field.name not in names_set, "Cfg %u should contain unique name" % i
        names_set.add(cfg_field.name)
        i += 1

    assert cfg_not_unique.field_cfgs[1].observable_field != cfg_not_unique.field_cfgs[1].name,\
           "Field \"%s\" has the same name as observable_field" % \
           cfg_not_unique.field_cfgs[1].name

    assert cfg_not_unique.field_cfgs[5].observable_field == "", "Observable name should be reseted. otherwise recursion (both fields add each other as observers)"

    print_cfg(cfg_not_unique)


############################################ test SET TEXT ############################################################
cfg_set_text = Config("Not unique names",
                 [FieldCfg("Question", HOTKEY_QUESTION, None, AddMode.Ignore, None),
                  FieldCfg("Answer", HOTKEY_ANSWER, "Question", AddMode.Ignore, None),
                  FieldCfg("Answer2", HOTKEY_ANSWER, "Question", AddMode.Ignore, None),
                 ],
                False)


def test_models_set_text():
    """Text should be correctly set to the field: all observers should be updated,
    in case text is too long it should be shortened"""
    print("\n    test_models_set_text")
    model_mng = ModelManager(cfg_set_text, AnkiExporterStub())

    field = model_mng.get_field("Question")
    assert field is not None

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

    observer_field = model_mng.get_field("Answer2")

    assert observable_field.get_text() == observer_field.get_text()


############################################ test GOOGLE TRANSLATOR ###################################################
cfg_googletrans = Config("Google Translator",
                 [FieldCfg("Question", HOTKEY_QUESTION, None, AddMode.Ignore, None),
                  FieldCfg("Answer", HOTKEY_ANSWER, "Question", AddMode.Ignore, DataProvType.Googletranslate),
                 ],
                False)


def test_models_googletrans():
    print("\n    test_models_googletrans")

    model_mng = ModelManager(cfg_googletrans, AnkiExporterStub())
    field = model_mng.get_field("Question")
    assert field is not None

    factory = get_dataprov_factory(DataProvType.Googletranslate)
    dataprov = factory.get_data_provider()

    assert dataprov is not None

    dataprov.update_data(text_test_normal)
    text = dataprov.get_text()

    assert text != text_test_normal, "after passing text to the data provider it has to be modified"

    field.set_text(text_test_normal)
    field = model_mng.get_field("Answer") #observer of the Question field

    assert text == field.get_text(), "text returned by the field has to be equal to the text returned by the dataprovider \
                                       as internally this field has to use the same dataprovider"


############################################ test CLIPBOARD ###########################################################
cfg_clipboard = Config("Clipboard",
                 [FieldCfg("Question", HOTKEY_QUESTION, None, AddMode.Ignore, None),
                  FieldCfg("Answer", HOTKEY_ANSWER, "Question", AddMode.Ignore, DataProvType.Clipboard),
                 ],
                False)


def test_models_clipboard():
    print("\n    test_models_clipboard")

    model_mng = ModelManager(cfg_clipboard, AnkiExporterStub())
    field = model_mng.get_field("Question")
    assert field is not None

    factory = get_dataprov_factory(DataProvType.Clipboard)
    dataprov = factory.get_data_provider()

    assert dataprov is not None
    text_clipboard = "Clipboard text"

    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(text_clipboard, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

    dataprov.update_data(text_test_normal)

    text = dataprov.get_text()

    assert text == text_clipboard, "after passing text to the data provider it has to be modified"

    field.set_text(text_test_normal)

    field = model_mng.get_field("Answer") #observer of the Question field

    assert text == field.get_text(), "text returned by the field has to be equal to the text returned by the dataprovider \
                                      as internally this field has to use the same dataprovider"

    #test for unicode data in clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(text_test_special_chars, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    dataprov.update_data("")
    text = dataprov.get_text()

    assert text_test_special_chars == text, "incorrect handling of the unicode text by clipboard data provider"

    #long text is passed to clipboard
    text_clipboard = "A" * (field.get_text_max() + 1)
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(text_clipboard, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    dataprov.update_data("")
    text = dataprov.get_text()

    assert text_clipboard == text, "incorrect handling of the long text by clipboard data provider"


############################################ TESTS EXECUTION ##########################################################
test_models_unique()
test_models_set_text()
test_models_googletrans()
test_models_clipboard()