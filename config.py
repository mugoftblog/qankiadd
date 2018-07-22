from enum import Enum
from dataprov.factory import *
"""
The calsses in this file contain configurtion descriptions.

Each configuration contains the list of fields.
"""



##################defines######################

class AddMode(Enum):
    """ this enum describes how the information is added to the field after shortkey press
    or after trigger execution
    """
    Ignore = 0,  # ignore - if field is not empty do nothing
    Write = 1,  # write - the field will be rewritten
    Append = 2,  # append = new text will be appended to the field


def print_cfg(cfg):
    for field in cfg.field_cfgs:
        print("FieldCfg(\"%s\", HOTKEY, \"%s\")" % (field.name, field.observable_field))


class FieldCfg:
    def __init__(self, name, shortkey=None, observable_field=None, addmode=AddMode.Write, dataprov_type=None):
        """
        :param name:
        :param shortkey:
        :param observer: observer which should be notified about new data every time data of this field is changed
        :param addmode:
        :param automode:
        """
        self.name = name
        self._shortkey = shortkey
        self.observable_field = observable_field
        self._addmode = addmode
        self.dataprov_type = dataprov_type


class Config:
    def __init__(self, name, field_cfgs=[], autosave=True):
        """
        :param name: name of the configuration
        :param fields: array with field models
        :param autosave: TODO ?? what is that - if all fields are full then save in file
        """
        self.name = name
        self.autosave = autosave
         # check if field names are unique. If not - add _1 or _2 at the end. Also update observers
        self.field_cfgs = field_cfgs

