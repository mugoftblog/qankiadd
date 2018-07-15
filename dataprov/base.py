"""
This file contains data provider parent class and
data provider factory parent class.

If you would like to add new data provider please
create new module with the name of the data provider and
add to this modue two classes:
- data provider class which has to be inherited 
from the data provider parent class.
- data provider factory class which has to be inherited
from the data provider factory parent class.

At the end don't forget to add information about
new data provider to the module "factory".
"""


__author__ = 'Mug0ft (mugoft.com)'
__copyright__ = 'Copyright (c) 2018 Mug0ft'
__license__ = 'GNU Affero General Public License v3.0'
__vcs_id__ = '$Id$'
__version__ = '0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/


class DataProv(object):
    """
    Parent class for all data providers. Each data
    provider has to be able to return data based on the
    passed text. E.g. translator data provider has to return
    translation of the passed text.
    """
    text = ""

    def get_text(self):
        """

        :return:
        """

        return self.text

    def get_image(self):
        pass

    def get_audio(self):
        pass

    def update_data(self):
        raise NotImplementedError('subclasses must override update_data()!')


class DataProvFactory(object):
    """
    Parent class for all data provider factories. Each data
    provider factory has to return the instance of the
    concrete data provider.
    """

    def __init__(self):
        self.dataprov = None

    def get_data_provider(self):
        return self.dataprov
