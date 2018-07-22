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

HOTKEY_RANDOM = ("ctrl", "p")

# is_save_all_called = False
#
#
# def save_all_stub():
#     global is_save_all_called
#     is_save_all_called = True
#     print("Save ALL fields")


############################################ test SIMPLE ##############################################################
HOTKEY_QUESTION_SIMPLE = ("ctrl", "b")
HOTKEY_ANSWER_SIMPLE = ("", "")

cfg_simple = Config("Simple",
                [FieldCfg("Question", HOTKEY_QUESTION_SIMPLE, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Answer", HOTKEY_ANSWER_SIMPLE, None, AddMode.Ignore, DataProvType.Googletranslate),
                 ],
                False)


def _press_keys_simple():
    # press the key which notifies field "Questio"
    time.sleep(1)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_QUESTION_SIMPLE[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_QUESTION_SIMPLE[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_QUESTION_SIMPLE[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_QUESTION_SIMPLE[1]], 0, win32con.KEYEVENTF_KEYUP, 0)

    # press some random key
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[1]], 0, win32con.KEYEVENTF_KEYUP, 0)

    # press the key to stop keys listening
    time.sleep(0.2)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[1]], 0, win32con.KEYEVENTF_KEYUP, 0)


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
    model_mng = ModelManager(cfg_simple, AnkiExporterStub())

    # Register observers for keylistener (in case observer has a valid key)
    keylisten = Keylistener()
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
HOTKEY_QUESTION_WRONG_KEY = ("ctrl", "ää")
HOTKEY_ANSWER_WRONG_KEY = ("ctrl", "ctrl")
HOTKEY_OTHER_WRONG_KEY = ("ä", "a")
HOTKEY_IMAGE_WRONG_KEY = (KEY_QUIT_TUPLE_STR[0], KEY_QUIT_TUPLE_STR[1])
HOTKEY_SOUND_WRONG_KEY = (KEY_SAVE_TUPLE_STR[0], KEY_SAVE_TUPLE_STR[1])

cfg_wrong_key = Config("Simple",
                [FieldCfg("Question", HOTKEY_QUESTION_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Answer", HOTKEY_ANSWER_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Other", HOTKEY_OTHER_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Image", HOTKEY_IMAGE_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 FieldCfg("Sound", HOTKEY_SOUND_WRONG_KEY, None, AddMode.Ignore, DataProvType.Googletranslate),
                 ],
                False)


def _press_keys_wrong_key():
    # press the key which notifies field "Answer"
    time.sleep(1)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_ANSWER_WRONG_KEY[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_ANSWER_WRONG_KEY[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_ANSWER_WRONG_KEY[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_ANSWER_WRONG_KEY[1]], 0, win32con.KEYEVENTF_KEYUP, 0)

    # press some random key
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[HOTKEY_RANDOM[1]], 0, win32con.KEYEVENTF_KEYUP, 0)

    # press the key to save all fields
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_SAVE_TUPLE_STR[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_SAVE_TUPLE_STR[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_SAVE_TUPLE_STR[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_SAVE_TUPLE_STR[1]], 0, win32con.KEYEVENTF_KEYUP, 0)

    # press the key to stop keys listening
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[0]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[1]], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[0]], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(NAME_TO_VK_TABLE[KEY_QUIT_TUPLE_STR[1]], 0, win32con.KEYEVENTF_KEYUP, 0)


def test_keylistener_wrong_key():
    """
        Preconditions:
            fields:
            - 1st field contains invalid vk name
            - 2nd has the same name for modifier and vk
            - 3rd has invalid modifier name
            - 4th has reserved hotkey (for quiting app)
            - 5th has already used hotkey (for saving, from model manager)
        Procedure:
            - start keylistener and register all fields as observers
            - press shortkey of the second field
            - press random shortkey
            - press shortkey for saving all fields
            - press shortkey to stop key listening
        Explanation:
            As all shortkeys are invalid text of the fields should not be changed
        Expectation:
            - only model manager should be registered by keylistener
            - the text of all fields is emply
            - "save all fields" command should be executed successfully
            - keylistener is stopped
        """
    print("\n    test_keylistener_wrong_key")
    anki_stub = AnkiExporterStub()
    model_mng = ModelManager(cfg_wrong_key, anki_stub)
    # global is_save_all_called
    # is_save_all_called = False
    # model_mng.save_all = save_all_stub

    # Register observers for keylistener (in case observer has a valid key)
    keylisten = Keylistener()
    keylisten.register_observer(model_mng)
    for field in model_mng.get_fields():
        keylisten.register_observer(field)

    assert len(keylisten._observers) == 1, "Only model manager should be registered"

    # Run thread which presses field hotkey and at the end quit hotkey
    thread = Thread(target=_press_keys_wrong_key)
    thread.start()

    keylisten.start_listening()
    thread.join()

    for field in model_mng.get_fields():
        assert field.get_text() == "", "Expect to see text \n \"%s\" \n but see\n \"%s\" " % \
                                                  ("", field.get_text())


    assert anki_stub._write_calls_n == 1, "KEY_SAVE_TUPLE_STR shortkey was not handled correctly"


############################################ TESTS EXECUTION ##########################################################
test_keylistener_simple()
test_keylistener_wrong_key()



