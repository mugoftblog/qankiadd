"""
This file contains data provider base class and
data provider factory base class.
"""

__author__ = 'Mug0ft (mugoft.com)'
__copyright__ = 'Copyright (c) 2018 Mug0ft'
__license__ = 'GNU Affero General Public License v3.0'
__vcs_id__ = '$Id$'
__version__ = '0.1'  # Versioning: http://www.python.org/dev/peps/pep-0386/


class DataProv(object):

    def __init__(self):
        """
        Base class for all data providers. Each data
        provider has to be able to return data based on the
        passed text. E.g. "translator" data provider has to return
        translation of the passed text.
        """
        text = ""

    def get_text(self):
        """
        Returns the text which is used for providing the data.

        :return: the text on which base the data is provided.
        """
        return self.text

    def get_image(self):
        """
        @TODO Returns image based on the provided text.
        """
        pass

    def get_audio(self):
        """
        @TODO Returns audio based on the provided text.
        """
        pass

    def update_data(self, text):
        """
        Stores the text which will be used by this data provided for providing the data (e.g. another text).

        :param text: the text on which base the data will be provided.
        """
        raise NotImplementedError('subclasses must override update_data()!')


class DataProvFactory(object):
    def __init__(self):
        """
        Base class for all data provider factories. Each data
        provider factory has to return the instance of the
        concrete data provider.
        """
        self.dataprov = None

    def get_data_provider(self):
        """
        Returns the data provider assigned to this factory.
        """
        return self.dataprov
