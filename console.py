"""
The calsses and methods responsible for creating and showing field's information in the console.
"""

import logging
import os
from keylistener import *


class Console(KeylistenerObserver):
    SHORTKEY_SHOWSTATUS_DEFAULT = (('ctrl', 'shift'), 'o')
    """ Default shortkey for showing current field's status in the console. """

    def __init__(self, modelmngr, shortkey_showstatus):
        """
        The class displays status information of the fields in the console.

        :param modelmngr: model manager (see :class:`.ModelManager`)
        :param shortkey_showstatus: shortkey which should be pressed to see status information
        """
        self._shortkey_showstatus = Console.SHORTKEY_SHOWSTATUS_DEFAULT
        if shortkey_showstatus is not None:
            self._shortkey_showstatus = shortkey_showstatus

        KeylistenerObserver.__init__(self, [self._shortkey_showstatus])
        self._modelmngr = modelmngr

    def print_status(self):
        """
        Shows information about all available fields (shortkeys, observable fields and text).

        :return: None
        """

        """ @TODO this function should show current status in the new window on the top of all other windows, and
        should also allow to modify the text of the fields. Probably the best way to achieve this is to use Tkinter"""

        print("***Status of the fields***")
        fields = self._modelmngr.get_fields()
        i = 0
        for field in fields:
            print("    %d. %s[Shortkey=%s][ObservableField=%s]:\n\"%s\"" % (i, field.cfg.name,
                                                                            field.cfg._shortkey,
                                                                            field.cfg.observable_field,
                                                                            field.get_text()))
            i += 1

    def key_pressed(self, shortkey):
        """
        For more details see :class:`.KeylistenerObserver`.
        """
        if self.compare_shortkeys(self._shortkey_showstatus, shortkey):
            self.print_status()