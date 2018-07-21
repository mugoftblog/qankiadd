from keylistener import *
from config import *
from models import *
from dataprov.google import *
from tests.stubs.dataprov.google import *
import win32api
import win32con
import time
from threading import Thread

HOTKEY_QUESTION = ("ctrl", "b")
HOTKEY_ANSWER = ("", "")

cfg_simple = Config("Simple",
                 [FieldCfg("Question", HOTKEY_QUESTION, None, AddMode.Ignore, DataProvType.GoogleTranslate),
                  FieldCfg("Answer", HOTKEY_ANSWER, "Question", AddMode.Ignore, DataProvType.GoogleTranslate),
                 ],
                False)

TEXT_NORMAL = "Normal text"


def press_keys():  # win32con.KEYEVENTF_EXTENDEDKEY
    # time.sleep(1)
    # win32api.keybd_event(vk_code['ctrl'], 0, 1, 0)
    # time.sleep(0.05)
    # win32api.keybd_event(0x42, 0, 1, 0)
    # time.sleep(0.05)
    # win32api.keybd_event(vk_code['ctrl'], 0, 2, 0)
    # time.sleep(0.05)
    # win32api.keybd_event(0x42, 0, 2, 0)

    time.sleep(1)
    win32api.keybd_event(vk_code['ctrl'], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(vk_code['q'], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(vk_code['q'], 0,  win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    win32api.keybd_event(vk_code['ctrl'], 0, win32con.KEYEVENTF_KEYUP, 0)



        #win32api.keybd_event(win32con.MOD_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        #win32api.keybd_event(0x42, 0, win32con.KEYEVENTF_KEYUP, 0)

    print("Pressed")



def test_keylistener_normal():

    model_mng = ModelManager(cfg_simple)

    field = model_mng.get_field("Question")

    assert field is not None

    field.set_text(TEXT_NORMAL)

    dataprov = GoogleStub()
    dataprov.update_data(TEXT_NORMAL)
    text_dataprov = dataprov.get_text()

    assert field.get_text() == text_dataprov, "Expect to see text \n \"%s\" \n but see\n \"%s\" " % \
                            (text_dataprov, field.get_text())

    keylisten = Keylistener()

    for field in model_mng.get_fields():
        keylisten.register_observer(field)

    thread = Thread(target= press_keys)
    thread.start()

    keylisten.start_listening()
    print("Joint")
    thread.join()


test_keylistener_normal()



