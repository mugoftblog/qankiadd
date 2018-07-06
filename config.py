from enum import Enum
from dataprov.dataprov_factory import *
"""
The calsses in this file contain configurtion descriptions.

Each configuration contains the list of fields.
"""



##################defines######################

class Addmode(Enum):
    I = 0,  # ignore - if field is not empty do nothing
    W = 1,  # write - the field will be rewritten
    A = 2,  # append = new text will be appended to the field

#this enum describes how the information is added to the field after shortkey press
#or after trigger execution
#TODO should be in dataprov_factory file



#  classes start  #

class FieldCfg:
    def __init__(self, name, shortkey, observable_name, addmode, dataprov_type):
        """
        :param name:
        :param shortkey:
        :param observer: observer which should be notified about new data every time data of this field is changed
        :param addmode:
        :param automode:
        """
        self.name = name
        self._shortkey = shortkey
        self.observable_name = observable_name
        self._addmode = addmode
        self.dataprov_type = dataprov_type


class Config:
    def __init__(self, name, field_cfgs, autosave=True):
        """
        :param name: name of the configuration
        :param fields: array with field models
        :param autosave: TODO ?? what is that
        """
        self.name = name
        self.autosave = autosave
         # check if field names are unique. If not - add _1 or _2 at the end. Also update observers
        self.field_cfgs = field_cfgs


##################execution code ##################

#TODO: it should be read from file later

#fields hotkeys
HOTKEY_QUESTION = ("ctrl", "b")
HOTKEY_ANSWER = ("ctrl", "spacebar")

""" TODO observers are registered as index within array of fields - not so convinient,
 and indexes always change whenever the order of added fields is changed """
configurations = [
    Config("Foreign Language",
           [FieldCfg("Question", HOTKEY_QUESTION,  "Answer",     Addmode.I, DataProvTypes.MANUAL),        # 0
            FieldCfg("Question", HOTKEY_QUESTION,  None,         Addmode.I, DataProvTypes.MANUAL),
            FieldCfg("Answer",   HOTKEY_ANSWER,   "Question",    Addmode.I, DataProvTypes.GOOGLETRANS),
            FieldCfg("Answer",   HOTKEY_ANSWER,   "Question",    Addmode.I, DataProvTypes.GOOGLETRANS)],  # 1
           False)
]