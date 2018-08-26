from enum import Enum
from dataprov.google import *
from dataprov.clipboard import *
import logging

"""
This module is an entry point for getting the required data provider.

After new data provider is added this file should be updated.
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

    NOTE: After adding new data provider add new type in this Enum!!!
    """

    Clipboard = 0,
    """ :class:`.clipboard.Clipboard` data provider should be used """
    Googletranslate = 1,
    """ :class:`.google.Google` data provider should be used """
    Googleimage = 2,
    """ @TODO :class:`.googleimg.GoogleImage` data provider should be used """


def get_dataprov_factory(dataprov_type):
    """
    Function which returns concrete factory instance of the specified data provider.

    NOTE: After adding new data provider please extend this function!!!

    param dataprov_type: the type of the data provider
    """
    dataprov_factory = None
    if dataprov_type is not None:
        if dataprov_type == DataProvType.Clipboard:
            dataprov_factory = ClibpboardFactory()
            logging.debug("Dataprovider \"%s \" is returned" % dataprov_type)
        elif dataprov_type == DataProvType.Googletranslate:
            dataprov_factory = GoogleFactory()
            logging.debug("Dataprovider \"%s \" is returned" % dataprov_type)
        else:
            dataprov_factory = None
            logging.warning("Invalid dataprovider: %s" % dataprov_type)

    return dataprov_factory
