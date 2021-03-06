"""
The module responsible for listening of the shortkeys pressed by a user and passing the information
about the pressed keys to the observers. This module can be used only under Windows OS.
"""

import ctypes
import logging
import sys
from ctypes import windll
from ctypes import wintypes

import win32con

byref = ctypes.byref


MOD_INVALID = 0x0000
""" Invalid modifier code. """

NAME_TO_MOD_TABLE = {
    'shift': win32con.MOD_SHIFT,
    'ctrl': win32con.MOD_CONTROL,
    'alt': win32con.MOD_ALT,
    'win': win32con.MOD_WIN,
}
""" Dictionary with {modifier name: modifier code} pairs. """

MOD_TO_NAME_TABLE = {}
""" Dictionary with {modifier code: modifier name} pairs. """
for name, mod in NAME_TO_MOD_TABLE.items():
    MOD_TO_NAME_TABLE[mod] = name


NAME_TO_VK_TABLE = {'backspace': 0x08,
                    'tab': 0x09,
                    'clear': 0x0C,
                    'enter': 0x0D,
                    'shift': 0x10,
                    'ctrl': 0x11,
                    'alt': 0x12,
                    'pause': 0x13,
                    'caps_lock': 0x14,
                    'esc': 0x1B,
                    'spacebar': 0x20,
                    'page_up': 0x21,
                    'page_down': 0x22,
                    'end': 0x23,
                    'home': 0x24,
                    'left_arrow': 0x25,
                    'up_arrow': 0x26,
                    'right_arrow': 0x27,
                    'down_arrow': 0x28,
                    'select': 0x29,
                    'print': 0x2A,
                    'execute': 0x2B,
                    'print_screen': 0x2C,
                    'ins': 0x2D,
                    'del': 0x2E,
                    'help': 0x2F,
                    '0': 0x30,
                    '1': 0x31,
                    '2': 0x32,
                    '3': 0x33,
                    '4': 0x34,
                    '5': 0x35,
                    '6': 0x36,
                    '7': 0x37,
                    '8': 0x38,
                    '9': 0x39,
                    'a': 0x41,
                    'b': 0x42,
                    'c': 0x43,
                    'd': 0x44,
                    'e': 0x45,
                    'f': 0x46,
                    'g': 0x47,
                    'h': 0x48,
                    'i': 0x49,
                    'j': 0x4A,
                    'k': 0x4B,
                    'l': 0x4C,
                    'm': 0x4D,
                    'n': 0x4E,
                    'o': 0x4F,
                    'p': 0x50,
                    'q': 0x51,
                    'r': 0x52,
                    's': 0x53,
                    't': 0x54,
                    'u': 0x55,
                    'v': 0x56,
                    'w': 0x57,
                    'x': 0x58,
                    'y': 0x59,
                    'z': 0x5A,
                    'numpad_0': 0x60,
                    'numpad_1': 0x61,
                    'numpad_2': 0x62,
                    'numpad_3': 0x63,
                    'numpad_4': 0x64,
                    'numpad_5': 0x65,
                    'numpad_6': 0x66,
                    'numpad_7': 0x67,
                    'numpad_8': 0x68,
                    'numpad_9': 0x69,
                    'multiply_key': 0x6A,
                    'add_key': 0x6B,
                    'separator_key': 0x6C,
                    'subtract_key': 0x6D,
                    'decimal_key': 0x6E,
                    'divide_key': 0x6F,
                    'F1': 0x70,
                    'F2': 0x71,
                    'F3': 0x72,
                    'F4': 0x73,
                    'F5': 0x74,
                    'F6': 0x75,
                    'F7': 0x76,
                    'F8': 0x77,
                    'F9': 0x78,
                    'F10': 0x79,
                    'F11': 0x7A,
                    'F12': 0x7B,
                    'F13': 0x7C,
                    'F14': 0x7D,
                    'F15': 0x7E,
                    'F16': 0x7F,
                    'F17': 0x80,
                    'F18': 0x81,
                    'F19': 0x82,
                    'F20': 0x83,
                    'F21': 0x84,
                    'F22': 0x85,
                    'F23': 0x86,
                    'F24': 0x87,
                    'num_lock': 0x90,
                    'scroll_lock': 0x91,
                    'left_shift': 0xA0,
                    'right_shift ': 0xA1,
                    'left_control': 0xA2,
                    'right_control': 0xA3,
                    'left_menu': 0xA4,
                    'right_menu': 0xA5,
                    'browser_back': 0xA6,
                    'browser_forward': 0xA7,
                    'browser_refresh': 0xA8,
                    'browser_stop': 0xA9,
                    'browser_search': 0xAA,
                    'browser_favorites': 0xAB,
                    'browser_start_and_home': 0xAC,
                    'volume_mute': 0xAD,
                    'volume_Down': 0xAE,
                    'volume_up': 0xAF,
                    'next_track': 0xB0,
                    'previous_track': 0xB1,
                    'stop_media': 0xB2,
                    'play/pause_media': 0xB3,
                    'start_mail': 0xB4,
                    'select_media': 0xB5,
                    'start_application_1': 0xB6,
                    'start_application_2': 0xB7,
                    'attn_key': 0xF6,
                    'crsel_key': 0xF7,
                    'exsel_key': 0xF8,
                    'play_key': 0xFA,
                    'zoom_key': 0xFB,
                    'clear_key': 0xFE,
                    '+': 0xBB,
                    ',': 0xBC,
                    '-': 0xBD,
                    '.': 0xBE,
                    '/': 0xBF,
                    '`': 0xC0,
                    ';': 0xBA,
                    '[': 0xDB,
                    '\\': 0xDC,
                    ']': 0xDD,
                    "'": 0xDE,
                    '`': 0xC0}
""" Dictionary with {key name: key code} pairs. """

VK_TO_NAME_TABLE = {}
""" Dictionary with {key code: key name} pairs. """
for name, vk in NAME_TO_VK_TABLE.items():
    VK_TO_NAME_TABLE[vk] = name


def shortkey_to_codes(shortkey):
    """
    This function maps key/modifier name from the passed shorkety to the virtual codes.

    :param shortkey: shortkey to map to virtual codes.
    :type shortkey: tuple (see :data:`.SHORTKEY_EXAMPLE`)
    :return: shortkey where strings (shortkey names) are replaced by the related virtual codes.
    """
    mod_code = 0
    for mod in shortkey[0]:
        code = NAME_TO_MOD_TABLE.get(mod, None)
        if code is not None:
            mod_code |= code
        else:
            mod_code = 0
            break

    key_code = NAME_TO_VK_TABLE.get(shortkey[1], None)

    ret = None
    if (mod_code != 0) and (key_code is not None):
        ret = (mod_code, key_code)

    return ret


SHORTKEY_QUIT_DEFAULT = (('ctrl', 'shift'), 'q')
""" Deault shortkey to quit the keylistener.  """
SHORTKEY_QUIT_DEFAULT_CODES = (NAME_TO_MOD_TABLE[SHORTKEY_QUIT_DEFAULT[0][0]] | NAME_TO_MOD_TABLE[SHORTKEY_QUIT_DEFAULT[0][1]],
                               NAME_TO_VK_TABLE[SHORTKEY_QUIT_DEFAULT[1]])


SHORTKEY_EXAMPLE = (('alt', 'ctrl', 'shift', 'win'), 'o')
""" Example of the shortkey with the correct format. Each shortkey must be a tuple \
and must have the following format: ((modifier_name1, modifier_name2, ..., modifier_nameN), key_name)"""


class KeylistenerObserver:
    def __init__(self, shortkeys):
        """
        Base observer class which should be inherited by sublasses to be able to register shortkeys and to start
        receiving the notification from :class:`.Keylistener` about the pressed shortkeys.

        :param shortkeys: The list of the shortkeys to register for listening.
        :type shortkeys: list of shortkeys (see :data:`.SHORTKEY_EXAMPLE`)
        """
        self._shortkeys = []
        if shortkeys is not None:
            if isinstance(shortkeys, list):
                for shortkey in shortkeys:
                    do_raise = False
                    if shortkey is not None:
                        if do_raise:
                            raise ValueError("wrong format of the input parameter")
                            break
                        if len(shortkey) == 2:
                            if isinstance(shortkey[0], tuple) and shortkey[0] and isinstance(shortkey[1], str) and \
                                    shortkey[1]:
                                self._shortkeys.append(shortkey)
                    else:
                        # if at least one of the shortkeys in the list is None raise the error
                        do_raise = True

    def key_pressed(self, shortkey):
        """
        This function is called whenever the registered shortkey is pressed. This function
        must be overwritten by subclasses.

        :param shortkey: the pressed registered shortkey.
        :type shortkey: tuple (see :data:`.SHORTKEY_EXAMPLE`)
        :return: None
        """
        raise NotImplementedError('subclasses must override NotifyKeyPressed(id)!')

    def get_keys(self):
        """
        Returns all shortkeys to register.

        :return: shortkeys to register
        :rtype: list of shortkeys (see :data:`.SHORTKEY_EXAMPLE`)
        """
        return self._shortkeys

    def compare_shortkeys(self, shortkey_expect, shortkey):
        """
        Compares two shortkeys

        :param shortkey_expect: first shortkey to compare
        :type shortkey: tuple (see :data:`.SHORTKEY_EXAMPLE`)
        :param shortkey: second shortkey to compare
        :type shortkey: tuple (see :data:`.SHORTKEY_EXAMPLE`)
        :return: True if the shortkeys the same False in case the shortkeys differ
        :rtype: bool
        """
        ret = True

        if len(shortkey[0]) != len(shortkey_expect[0]):
            # if tuple length differ from the expected tuple length
            ret = False
        else:
            for modifier in shortkey[0]:
                if modifier not in shortkey_expect[0]:
                    # if at least one of the modifiers not in the expected tuple
                    ret = False

        if ret:
            if shortkey[1] != shortkey_expect[1]:
                # if keyboard key is not the same as expected
                ret = False

        return ret


class Keylistener:
    def __init__(self, shortkey_quit):
        """
        The class is responsible for listening shortkeys pressed by a user.

        The class is responsible for listening shortkeys pressed. After the registered shortkey is pressed
        it extratcts necessery information from the message and pass this information to the observers,
        which further decide how to handle this shortkey press.
        """
        self._observers = []
        self._key_ids = []  # list of tuples in the format (key_id, lparam)
        self._key_id_last = 0

        if shortkey_quit is None:
            self._key_code_quit = SHORTKEY_QUIT_DEFAULT_CODES
        else:
            self._key_code_quit = shortkey_to_codes(shortkey_quit)

    def _get_lparam(self, modifier_code, key_code):
        """
        Returns lparam which represents 32 bit value which stores passed modifier virtual codes and key virtual code.

        :param modifier_code: modifier virtual code
        :param key_code: key virtual code
        :return: 32 bit lparam value
        :rtype: int
        """
        lparam = (key_code << 16) | modifier_code
        return lparam

    def _store_regitered_key(self, modifier_code, key_code):
        """
        Stores passed modifier and key virtual codes in the list. Later it can be used e.g. for checking
        wether the shortkey with the specified modifier and key codes are already registered or not.

        :param modifier_code:
        :param key_code:
        :return: None
        """
        lparam = self._get_lparam(modifier_code, key_code)

        self._key_ids.append((self._key_id_last, lparam))
        self._key_id_last += 1

    def _unregister_key(self, key_id):
        """
        Stop listening the shortkey with the specified id.

        :param key_id: id of the shortkey to unregister
        :return: True if success, False if can't unregister.
        :rtype: bool
        """
        ret = False
        logging.debug("Unregistering key with id %u" % key_id[0])
        if not windll.user32.UnregisterHotKey(None, key_id[0]):
            logging.warning("Unable to unregister the key")
        else:
            logging.debug("Unregistering OK")
            ret = True
        return ret

    def _register_key_by_code(self, modifier_code, key_code):
        """
        Start listening the shortkey with the specified modifier and key virtual codes.

        :param modifier_code: modifier virtual codes of the shortkey to register.
        :param key_code: key virtual code of the shortkey to register.
        :return: True if success, False if can't register the shortkey.
        :rtype: bool
        """
        logging.debug("_register_key_by_code %s %s" % (modifier_code, key_code))
        ret = False
        if (modifier_code != MOD_INVALID) and (key_code is not None):
            is_key_registered = False

            # TODO check if it is already registered or not
            for key_tuple in self._key_ids:
                lparam = self._get_lparam(modifier_code, key_code)
                is_key_registered = set((lparam,)).issubset(key_tuple)
                if is_key_registered:
                    logging.debug("the key is already registered")
                    break

            if not is_key_registered:
                logging.info("Registering shortkey (\'%u\', \'%u\')" % (modifier_code, key_code))
                if not windll.user32.RegisterHotKey(None, self._key_id_last, modifier_code, key_code):
                    logging.warning("Unable to register the shortkey")
                else:
                    self._store_regitered_key(modifier_code, key_code)
                    ret = True
                    logging.debug("Registering OK")
            else:
                # in case shortkey is already registered do nothing but just return True
                ret = True
        return ret

    def _register_key(self, shortkey):
        """
        Start listening the shortkey

        :param shortkey: the shortkey to register.
        :type shortkey: tuple (see :data:`.SHORTKEY_EXAMPLE`)
        :return: True if success, False if can't register the shortkey.
        :rtype: bool
        """
        logging.debug("_register_key %s", shortkey)

        mod_code = MOD_INVALID
        for mod_name in shortkey[0]:
            mod_code_tmp = NAME_TO_MOD_TABLE.get(mod_name, None)

            if mod_code_tmp is not None:
                mod_code |= mod_code_tmp
            else:
                logging.warning("Can't resolve modifier name %s" % mod_name)
                mod_code = MOD_INVALID
                break;

        key_code = NAME_TO_VK_TABLE.get(shortkey[1], None)

        return self._register_key_by_code(mod_code, key_code)

    def register_observer(self, observer):
        """
        Register observer which wants to receive notifications about pressed registered shortkeys.

        :param observer: observer sublass (see :class:`.KeylistenerObserver`)
        :return: None
        """
        if issubclass(type(observer), KeylistenerObserver):
            n_registered_key = 0
            for key in observer.get_keys():
                if self._register_key(key):
                    n_registered_key += 1
            if n_registered_key > 0:
                self._observers.append(observer)
        else:
            logging.error("KeylistenerObserver is expected")
            sys.exit(1)

    def start_listening(self):
        """
        Start key press monitoring - in case registered key is pressed, registered observers are notified
        """
        logging.debug("Key listening is STARTED")
        self._register_key_by_code(self._key_code_quit[0], self._key_code_quit[1])
        try:
            msg = wintypes.MSG()
            while windll.user32.GetMessageA(byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    key_code = (msg.lParam >> 16) & 0xFFFF
                    mod_codes = msg.lParam & 0xFFFF
                    logging.debug("Key is pressed (%s, %s)" % (mod_codes, key_code))

                    # notify observers about pressed shortkey
                    mod_tuple = ()
                    for mod_name, mod_code in NAME_TO_MOD_TABLE.items():
                        if (mod_code & mod_codes) != 0:
                            mod_tuple += (mod_name,)

                    key = VK_TO_NAME_TABLE.get(key_code, None)

                    if mod_tuple and key is not None:
                        shortkey = [mod_tuple, key]
                        for observer in self._observers:
                            observer.key_pressed(shortkey)

                    if mod_codes == self._key_code_quit[0] and key_code == self._key_code_quit[1]:
                        logging.info("Key listening is STOPPED")
                        break

                    windll.user32.TranslateMessage(byref(msg))
                    windll.user32.DispatchMessageA(byref(msg))

        finally:
            key_ids_remove = []
            # unregister all stored keys
            for key_id in self._key_ids:
                if self._unregister_key(key_id):
                    key_ids_remove.append(key_id)

            # remove stored keys which were unregistered successfully
            for key_id in key_ids_remove:
                self._key_ids.remove(key_id)
