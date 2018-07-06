from enum import Enum

class DataProvTypes(Enum):
    CLIPBOARD = 0,  # information should be added from clipboard @TODO selected text
    MANUAL = 1,  # information will be added manually, therefore just highlight the field in case hotkey is pressed
    GOOGLETRANS = 2,  # information will be automatically translated via google translate module
    GOOGLEIMG = 3,  # information will be automatically found and added via google image module
    INVALID = 4


def get_dataprov_factory(dataprov_type):
    dataprov_factory = None
    if dataprov_type is not DataProvTypes.INVALID:
        if dataprov_type == DataProvTypes.CLIPBOARD:
            dataprov_factory = Clipboard()
        elif dataprov_type == DataProvTypes.GOOGLETRANS:
            dataprov_factory = GoogleFactory()
        else:
            dataprov_factory = None

    return dataprov_factory

class DataProv(object):
    data = ""

    def get_data(self):
        return self.data


class Google(DataProv):
    def update_data(self, text):
        data = text + "_UPDATED_GOOGLE"


class Clipboard(DataProv):
    def update_data(self, text):
        data = text + "_UPDATED_Clipboard"


class DataProvFactory(object):
    data_prov = None

    def get_data_provider(self):
        return self.data_prov


class GoogleFactory(DataProvFactory):
    DataProvFactory.data_prov = Google();


class ClibpboardFactory(object):
    DataProvFactory.data_prov = Clipboard();

