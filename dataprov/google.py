from dataprov.base import *


class Google(DataProv):
    """
    @TODO Google translate data provider. Translates the passed text and returns results to the caller.
    """
    def update_data(self, txt):
        DataProv.text = txt + "_UPDATED_GOOGLE"


class GoogleFactory(DataProvFactory):
    def __init__(self):
        """
        Factory for the :class:`Google` data provider.
        """
        DataProvFactory.dataprov = Google()
