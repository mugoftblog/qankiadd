from enum import Enum
from dataprov.google import *
from dataprov.clipboard import *

"""
This module is an entry point for getting the required data provider.

After new data provider is added (see module "interface" for details)
this file should be updated. 
First of all new data provider type has to be added.
Second of all the method returning an instance of the concrete factory
for the specified type has to be updated.
"""

__author__ = 'Mug0ft (mugoft.com)'
__copyright__ = 'Copyright (c) 2018 Mug0ft'
__license__ = 'GNU Affero General Public License v3.0'
__vcs_id__ = '$Id$'
__version__ = '0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/


class DataProvType(Enum):
    """
    All available data provider types.
    After adding new data provider add new type in this Enum
    """
    Clipboard = 0,  # information should be added from clipboard @TODO selected text
    GoogleTranslate = 1,  # information will be automatically translated via google translate module
    GoogleImage = 2,  # information will be automatically found and added via google image module


def get_dataprov_factory(dataprov_type):
    """
    Function which returns concrete object of the specified data provider.
    After adding new data provider please extend this function.

    param dataprov_type: the type of the data provider
    """
    dataprov_factory = None
    if dataprov_type is not None:
        if dataprov_type == DataProvType.Clipboard:
            dataprov_factory = ClibpboardFactory()
        elif dataprov_type == DataProvType.GoogleTranslate:
            dataprov_factory = GoogleFactory()
        else:
            dataprov_factory = None

    return dataprov_factory
