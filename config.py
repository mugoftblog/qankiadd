from enum import Enum
from dataprov.factory import *

"""
The module contains configuration models.
Each main configuration model consists of its name and the list of field configuration models.
"""


class AddMode(Enum):
    """
    Contains "addmode" types. Each "addmode" type describes how the data
    should be added to the field.
    """

    Ignore = 0,
    """ ignore - if the field already contains some data do not update field's data """
    Write = 1,
    """ write - the data of the field will be rewritten by new data """
    Append = 2,
    """ append - new data will be appended to the already existing field's data """


def print_cfg(cfg):
    for field in cfg.field_cfgs:
        print("FieldCfg(\"%s\", HOTKEY, \"%s\")" % (field.name, field.observable_field))


class FieldCfg:
    def __init__(self, name, shortkey=None, observable_field=None, addmode=AddMode.Write,
                 dataprov_type=None, required=False):
        """
        Field configuration model. Contains the information which should be used to set up correct
        behaviour of the field model and to create correct linking between field models,
        listened shortkeys, various data providers and etc.

        :param name: name of the field
        :param shortkey: shortkey of the field which should be used to set up the data of the field \
        using the specified data provider
        :type shortkey: :data:`keylistener.SHORTKEY_EXAMPLE` @TODO format of the shortkey in the configuration model \
        should not tightly couple on the format of the shortkey in the keylistener module. New converter function \
        should be introduced.
        :param observable_field: observable field which should notify this field about new data every time \
        data of the observable field is changed
        :type observable_field: :class:`.FieldCfg`
        :param addmode: :class:`.AddMode`
        :param required: indicates whether the field can be exported even if it is empty (False) or not (True)
        :type required: bool
        :param dataprov_type: :class:`.dataprov.factory.DataProvType`
        """
        self.name = name
        self._shortkey = shortkey
        self.observable_field = observable_field
        self._addmode = addmode
        self._required = required
        self.dataprov_type = dataprov_type


class Config:
    def __init__(self, name, field_cfgs=(), autosave=True):
        """
        Main configuration model.

        :param name: name of the configuration
        :param field_cfgs: list of the field configuration models
        :param autosave: True: if all fields are full then save in the file automatically.
        """
        self.name = name
        self.autosave = autosave
        # check if field names are unique. If not - add _1 or _2 at the end. Also update observers
        self.field_cfgs = field_cfgs

