import win32clipboard
from dataprov.base import *


def delegate_clipboard(field):
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard() #TODO try catch
    field.set_text(text)


class Clipboard(DataProv):
    def update_data(self, text):
        win32clipboard.OpenClipboard()
        try:
            DataProv.text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        except (TypeError, win32clipboard.error):
            print("TEST")
            try:
                DataProv.text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                print("LOG: WARNING: Clipboard::update_data can't read unicode data from clipboard")
            except (TypeError, win32clipboard.error):
                print("LOG: ERROR: Clipboard::update_data can't access clipboard")
                DataProv.text = "ERROR"
        finally:
            win32clipboard.CloseClipboard()


class ClibpboardFactory(DataProvFactory):
    def __init__(self):
        DataProvFactory.dataprov = Clipboard()
