import win32clipboard
from dataprov.base import *
import logging


class Clipboard(DataProv):
    """
    Clipboard data provider. Returns the data stored in the clipboard buffer.
    """
    def update_data(self, text):
        win32clipboard.OpenClipboard()
        try:
            DataProv.text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        except (TypeError, win32clipboard.error):
            try:
                DataProv.text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                logging.warning("can't read unicode data from clipboard")
            except (TypeError, win32clipboard.error):
                logging.error("can't access clipboard")
                DataProv.text = "ERROR"
        finally:
            win32clipboard.CloseClipboard()


class ClibpboardFactory(DataProvFactory):
    """
    Factory for the :class:`Clipboard` data provider.
    """
    def __init__(self):
        DataProvFactory.dataprov = Clipboard()
