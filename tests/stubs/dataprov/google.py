from dataprov.base import *


class GoogleStub(DataProv):
    def update_data(self, txt):
        DataProv.text = txt + "_Google_DataProv_Stub"


class GoogleFactoryStub(DataProvFactory):
    def __init__(self):
        DataProvFactory.dataprov = GoogleStub()

