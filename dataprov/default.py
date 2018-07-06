import win32clipboard


def delegate_clipboard(field):
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard() #TODO try catch
    field.set_text(text)