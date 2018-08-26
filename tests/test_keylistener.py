from keylistener import *
from config import *
from models import *
from dataprov.google import *
from tests.stubs.dataprov.google import *
import win32api
import win32con
import time
from threading import Thread
from tests.stubs.exporting.anki import *


################################################## COMMON ############################################################
def __shortkey_to_vk(shortkey):
    """
    This function maps names from the passed shorkety to the virtual codes
    :param shortkey: shortkey to map to virtual codes
    :return: shortkey where strings (shortkey names) are replaced by the related virtual codes
    """
    mod_to_vk = ()
    modifiers = shortkey[0]
    for mod in modifiers:
        mod_to_vk += (NAME_TO_VK_TABLE[mod],)

    ret = (mod_to_vk, NAME_TO_VK_TABLE[shortkey[1]])
    return ret


def __press_shortkey(shortkey):
    """
    This function simulate shortkey press
    :param shortkey: shortkey to be pressed
    :return:
    """
    shortkey_to_vk = __shortkey_to_vk(shortkey)

    modifiers_vk = shortkey_to_vk[0]
    key_vk = shortkey_to_vk[1]

    # first press modifiers
    for mod_vk in modifiers_vk:
        win32api.keybd_event(mod_vk, 0, 0, 0)
        time.sleep(0.05)

    # then press the key
    win32api.keybd_event(key_vk, 0, 0, 0)
    time.sleep(0.05)

    # key up for modifiers
    for mod_vk in modifiers_vk:
        win32api.keybd_event(mod_vk, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)

    # key up for the key
    win32api.keybd_event(key_vk, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)


SHORTKEY_RANDOM = (("ctrl",), "p")

# is_save_all_called = False
#
#
# def save_all_stub():
#     global is_save_all_called
#     is_save_all_called = True
#     print("Save ALL fields")


############################################ test SIMPLE ##############################################################
SHORTKEY_QUESTION_SIMPLE = (("ctrl", "shift"), "b")
SHORTKEY_ANSWER_SIMPLE = (("",), "")  # just make it empty as this key will not be used during the test

cfg_simple = Config("Simple",
                [FieldCfg("Question", SHORTKEY_QUESTION_SIMPLE, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Answer", SHORTKEY_ANSWER_SIMPLE, None, AddMode.Ignore, DataProvType.Googletranslate),
                 ],
                False)


def _press_keys_simple():
    # press the key which notifies field "Question"
    __press_shortkey(SHORTKEY_QUESTION_SIMPLE)

    # press some random key
    __press_shortkey(SHORTKEY_RANDOM)

    # press the key to stop keys listening
    __press_shortkey(SHORTKEY_QUIT_DEFAULT)


def test_keylistener_simple():
    """
        Preconditions:
            2 fields:
            - first one has a valid shortkey
            - the second one has shorkey tuple consisting of empty strings
        Procedure:
            - start keylistener and register 2 fields as observers
            - press shortkey of the registered field
            - press random shortkey
            - press shortkey to stop key listening
        Explanation:
            After shortkey of the first field is pressed the text of this field has to be changed
            based on the dataprovider assigned to this field
        Expectation:
            - the text of the first field has to be changed based on the dataprovider assigned to this field
            - the text of the second field should not be changed
            - keylistener should be stopped at the end
        """
    print("\n    test_keylistener_simple")
    model_mng = ModelManager(cfg_simple, AnkiExporterStub(), SHORTKEY_SAVEALL_DEFAULT, SHORTKEY_CLEARALL_DEFAULT)

    # Register observers for keylistener (in case observer has a valid key)
    keylisten = Keylistener(SHORTKEY_QUIT_DEFAULT)
    keylisten.register_observer(model_mng)
    for field in model_mng.get_fields():
        keylisten.register_observer(field)

    # Fetch the text which we expect to see in the field after key is pressed
    dataprov = GoogleStub()
    dataprov.update_data("")
    text_dataprov = dataprov.get_text()

    # Run thread which presses field hotkey and at the end quit hotkey
    thread = Thread(target=_press_keys_simple)
    thread.start()

    keylisten.start_listening()
    thread.join()

    field = model_mng.get_field("Question")
    assert field is not None

    assert field.get_text() == text_dataprov, "Expect to see text \n \"%s\" \n but see\n \"%s\" " % \
                            (text_dataprov, field.get_text())

    field = model_mng.get_field("Answer")
    assert field is not None
    assert field.get_text() == "", "Expect to see text \n \"%s\" \n but see\n \"%s\" " % \
                                ("", field.get_text())


############################################ test WRONG KEY ###########################################################
SHORTKEY_QUESTION_WRONG_KEY = (("ctrl",), "ää")

SHORTKEY_ANSWER_WRONG_KEY = (("ctrl",), "SA")

SHORTKEY_OTHER_WRONG_KEY = (("ä",), "a")

SHORTKEY_IMAGE_WRONG_KEY = ((SHORTKEY_QUIT_DEFAULT[0][0], SHORTKEY_QUIT_DEFAULT[0][1]),
                            SHORTKEY_QUIT_DEFAULT[1])

SHORTKEY_SOUND_WRONG_KEY = ((SHORTKEY_SAVEALL_DEFAULT[0][0], SHORTKEY_SAVEALL_DEFAULT[0][1]),
                            SHORTKEY_SAVEALL_DEFAULT[1])

cfg_wrong_key = Config("Simple",
                [FieldCfg("Question", SHORTKEY_QUESTION_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Answer", SHORTKEY_ANSWER_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Other", SHORTKEY_OTHER_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Image", SHORTKEY_IMAGE_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Sound", SHORTKEY_SOUND_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 ],
                False)


def _press_keys_wrong_key():
    # press some random keyb
    __press_shortkey(SHORTKEY_RANDOM)

    # press the key to save all fields
    __press_shortkey(SHORTKEY_SAVEALL_DEFAULT)

    # press the key to stop keys listening
    __press_shortkey(SHORTKEY_QUIT_DEFAULT)


def test_keylistener_wrong_key():
    """
        Preconditions:
            fields:
            - 1st field has invalid vk name (NOT REGISTERED AS OBSERVER)
            - 2nd  has invalid vk name (NOT REGISTERED AS OBSERVER)
            - 3rd has invalid modifier name (REGISTERED AS OBSERVER)
            - 4th has reserved hotkey (for quiting app) (NOT REGISTERED AS OBSERVER)
            - 5th has already used hotkey (for saving, from model manager) (REGISTERED AS OBSERVER)
        Procedure:
            - start keylistener and register all fields as observers
            - press shortkey of the second field
            - press random shortkey
            - press shortkey for saving all fields
            - press shortkey to stop key listening
        Explanation:
            As all shortkeys are invalid text of the fields should not be changed
        Expectation:
            - only 2 fields and model manager should be registered by keylistener as observers (3 in total)
            - the text of the first 3 fields is empty
            - the text of the last 2 fields is not empty
            - "save all fields" command is executed successfully
            - keylistener is stopped
        """
    print("\n    test_keylistener_wrong_key")
    anki_stub = AnkiExporterStub()
    model_mng = ModelManager(cfg_wrong_key, anki_stub, SHORTKEY_SAVEALL_DEFAULT, SHORTKEY_CLEARALL_DEFAULT)
    # global is_save_all_called
    # is_save_all_called = False
    # model_mng.save_all = save_all_stub

    # Register observers for keylistener (in case observer has a valid key)
    keylisten = Keylistener(SHORTKEY_QUIT_DEFAULT)
    keylisten.register_observer(model_mng)
    for field in model_mng.get_fields():
        keylisten.register_observer(field)

    assert len(keylisten._observers) == 3, "Registered observers expected: 4 but got: %d" % len(keylisten._observers)

    # Run thread which presses field hotkey and at the end quit hotkey
    thread = Thread(target=_press_keys_wrong_key)
    thread.start()

    keylisten.start_listening()
    thread.join()

    fields = model_mng.get_fields()
    for field in fields[:3]:
        assert field.get_text() == "", "Expect to see text \n \"%s\" \n but see\n \"%s\" " % \
                                                  ("", field.get_text())

    for field in fields[3:len(fields)]:
        assert field.get_text() != "", "Expect to see not empty text but see\n \"%s\" " % \
                                                  ( field.get_text())

    assert anki_stub._write_calls_n == 1, "KEY_SAVE_TUPLE_STR shortkey was not handled correctly"


############################################ TESTS EXECUTION ##########################################################
test_keylistener_simple()
test_keylistener_wrong_key()



