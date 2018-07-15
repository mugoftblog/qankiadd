from dataprov.base import *


class Google(DataProv):
    def update_data(self, txt):
        DataProv.text = txt + "_UPDATED_GOOGLE"


class GoogleFactory(DataProvFactory):
    def __init__(self):
        DataProvFactory.dataprov = Google()
