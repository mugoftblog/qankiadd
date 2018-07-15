from config import *
from dataprov.factory import *
import xml.etree.ElementTree as ET

ELEM_ROOT = 'Root'
ELEM_CONFIG = 'Configuration'
ELEM_FIELD = 'Field'
ELEM_KEY1 = 'Key1'
ELEM_KEY2 = 'Key2'
ELEM_OBSERVABLE_FIELD = "ObservableField"
ELEM_DATA_PROVIDER = "DataProvider"
ATTR_ADDMODE = 'addmode'
ATTR_NAME = 'name'

class ConfigImproter:
    def __init__(self, path):
        self._path = path
        self.cfg_list = []

    def __pretty_write(self, elem, level=0):
        """Adds new lines for each element in the XML file to simplfy human reading"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__pretty_write(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def read(self):
        if self._path != "":
            try:
                tree = ET.parse(self._path)
                root = tree.getroot()

                for Configuration in root.findall(ELEM_CONFIG):
                    name = Configuration.get(ATTR_NAME)
                    if name is None:
                        name = "None"

                    cfg = Config(name)

                    for Field in Configuration.findall(ELEM_FIELD):
                        field_name = Field.get(ATTR_NAME)
                        if field_name is None:
                            field_name = "None"

                        field_cfg = FieldCfg(field_name)

                        # try to find AddMode element
                        try:
                            addmode = AddMode[Field.get(ATTR_ADDMODE).title()]
                            field_cfg._addmode = addmode
                        except KeyError:
                            print("LOG: ConfigImproter::read wrong addmode \"%s\" in config file" %
                                  Field.get(ATTR_ADDMODE))

                        # try to find key1 and key2
                        key1_str = ""
                        key_elem = Field.find(ELEM_KEY1)
                        if key_elem is not None:
                            key1_str = key_elem.text

                        key2_str = ""
                        key_elem = Field.find(ELEM_KEY2)
                        if key_elem is not None:
                            key2_str = key_elem.text

                        field_cfg._shortkey = (key1_str, key2_str)

                        # try to find obervable name
                        obervable_elem = Field.find(ELEM_OBSERVABLE_FIELD)
                        if obervable_elem is not None:
                            field_cfg.observable_field = obervable_elem.text

                        # try to find data provider element
                        dataprov_elem = Field.find(ELEM_DATA_PROVIDER)
                        if dataprov_elem is not None:
                            try:
                                field_cfg.dataprov_type = DataProvType[dataprov_elem.text]
                            except KeyError:
                                print("LOG: ConfigImproter::read wrong dataprov_type \"%s\" in config file" %
                                      dataprov_elem.text)


                        cfg.field_cfgs.append(field_cfg)

                    self.cfg_list.append(cfg)
            except ET.ParseError:
                print("LOG: ConfigImproter::read can't parse file")
            except FileNotFoundError as e:
                print("LOG: ConfigImproter::read can't find file")
                print(e)

    def write(self):
        root = ET.Element(ELEM_ROOT)

        for cfg in self.cfg_list:
            Configuration = ET.SubElement(root, ELEM_CONFIG)
            Configuration.set(ATTR_NAME, cfg.name)
            for field in cfg.field_cfgs:
                Field = ET.SubElement(Configuration, ELEM_FIELD)
                Field.set(ATTR_ADDMODE, field._addmode.name)
                Field.set(ATTR_NAME, field.name)

                if (field.observable_field is not None) and (field.observable_field != ""):
                    ObservableField = ET.SubElement(Field, ELEM_OBSERVABLE_FIELD)
                    ObservableField.text = field.observable_field

                if field._shortkey is not None:
                    if (field._shortkey[0] != '') and (field._shortkey[0] != ''): #TODO? if at least one availble write?
                        Key1 = ET.SubElement(Field, ELEM_KEY1)
                        Key1.text = field._shortkey[0]
                        Key2 = ET.SubElement(Field, ELEM_KEY2)
                        Key2.text = field._shortkey[1]

                if field.dataprov_type is not None:
                    DataProvider = ET.SubElement(Field, ELEM_DATA_PROVIDER)
                    DataProvider.text = field.dataprov_type.name

        self.__pretty_write(root)
        ET.ElementTree(root).write(self._path, encoding="UTF-8", xml_declaration=True, short_empty_elements = False)


