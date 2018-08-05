from config import *
from dataprov.factory import *
import sys
import xml.etree.ElementTree as ET
import logging

ELEM_ROOT = 'Root'
ELEM_CONFIG = 'Configuration'
ELEM_FIELD = 'Field'
ELEM_MODIFIER = 'Modifier'
ELEM_KEY = 'Key'
ELEM_OBSERVABLE_FIELD = "ObservableField"
ELEM_DATA_PROVIDER = "DataProvider"
ATTR_ADDMODE = 'addmode'
ATTR_NAME = 'name'
ATTR_REQUIRED = 'required'
ELEM_SAVEALL = 'SaveAll'
ELEM_CLEARALL = 'ClearAll'
ELEM_QUIT = 'Quit'

class ConfigImproter:
    def __init__(self, path):
        self._path = path
        self._shortkey_saveall = None
        self._shortkey_clearall = None
        self._shortkey_quit = None
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

    def _read_shortkey_from_elem(self, elem):
        shortkey = None
        mod_tuple = ()
        mod_str = ""
        for mod_elem in elem.findall(ELEM_MODIFIER):
            mod_str = mod_elem.text.lower()
            if (mod_str != "") and (mod_str not in mod_tuple):
                mod_tuple = mod_tuple + (mod_str,)

        key_str = ""
        key_elem = elem.find(ELEM_KEY)
        if key_elem is not None:
            key_str = key_elem.text.lower()

        if mod_tuple and key_str:
            shortkey = [mod_tuple, key_str]

        return shortkey

    def _read_shortkey(self, elem_parent, elem_name):
        elem_sub = elem_parent.find(elem_name)
        if elem_sub is not None:
            return self._read_shortkey_from_elem(elem_sub)

    def _write_shortkey(self, elem_parent, elem_name, shortkey):
        if shortkey is not None:
            if (shortkey[0]) and (shortkey[1]):
                elem_sub = ET.SubElement(elem_parent, elem_name)
                for mod in shortkey[0]:
                    Modifier = ET.SubElement(elem_sub, ELEM_MODIFIER)
                    Modifier.text = mod

                Key = ET.SubElement(elem_sub, ELEM_KEY)
                Key.text = shortkey[1]

    def read(self):
        if self._path != "":
            try:
                tree = ET.parse(self._path)
                root = tree.getroot()

                # read shortkey for saving all fields into the file (if exists)
                self._shortkey_saveall = self._read_shortkey(root, ELEM_SAVEALL)

                # read shortkey for clearing all fields (if exists)
                self._shortkey_clearall = self._read_shortkey(root, ELEM_CLEARALL)

                # read shortkey for quiting the app (if exists)
                self._shortkey_quit = self._read_shortkey(root, ELEM_QUIT)

                # read all configurations
                for Configuration in root.findall(ELEM_CONFIG):
                    name = Configuration.get(ATTR_NAME)
                    if name is None:
                        name = "None"

                    cfg = Config(name)

                    # read all fields
                    for Field in Configuration.findall(ELEM_FIELD):
                        field_name = Field.get(ATTR_NAME)
                        if field_name is None:
                            field_name = "None"

                        field_cfg = FieldCfg(field_name)

                        # try to read addmode attribute (if exists)
                        try:
                            addmode = AddMode[Field.get(ATTR_ADDMODE).title()]
                            field_cfg._addmode = addmode
                        except KeyError:
                            logging.warning("wrong addmode \"%s\" in config file" % Field.get(ATTR_ADDMODE))

                        # read required attribute (True or False)
                        required = Field.get(ATTR_REQUIRED).lower()
                        if (required is not None) and (required == 'true'):
                            field_cfg._required = True
                        else:
                            field_cfg._required = False

                        # try to read field shortkey (if exists)
                        field_cfg._shortkey = self._read_shortkey_from_elem(Field)
                        print(field_cfg._shortkey)

                        # try to read obervable name (if exists)
                        obervable_elem = Field.find(ELEM_OBSERVABLE_FIELD)
                        if obervable_elem is not None:
                            field_cfg.observable_field = obervable_elem.text

                        # try to read data provider (if exists)
                        dataprov_elem = Field.find(ELEM_DATA_PROVIDER)
                        if dataprov_elem is not None:
                            try:
                                field_cfg.dataprov_type = DataProvType[dataprov_elem.text.title()]
                            except KeyError:
                                logging.warning("wrong dataprov_type \"%s\" in config file" % dataprov_elem.text)

                        cfg.field_cfgs.append(field_cfg)

                    self.cfg_list.append(cfg)
            except ET.ParseError as e:
                logging.error(e)
                sys.exit(1)
            except FileNotFoundError as e:
                logging.error(e)
                sys.exit(1)

    def write(self):
        # prepare XML root used to store all available configuration's data
        root = ET.Element(ELEM_ROOT)

        # write shortkey for saving all fields (if exists)
        self._write_shortkey(root, ELEM_SAVEALL, self._shortkey_saveall)

        # write shortkey for clearing all fields (if exists)
        self._write_shortkey(root, ELEM_CLEARALL, self._shortkey_clearall)

        # write shortkey for quiting the app (if exists)
        self._write_shortkey(root, ELEM_QUIT, self._shortkey_quit)

        # write all configurations
        for cfg in self.cfg_list:
            Configuration = ET.SubElement(root, ELEM_CONFIG)
            Configuration.set(ATTR_NAME, cfg.name)
            for field in cfg.field_cfgs:
                Field = ET.SubElement(Configuration, ELEM_FIELD)
                Field.set(ATTR_ADDMODE, field._addmode.name)
                Field.set(ATTR_NAME, field.name)
                if field._required == True:
                    Field.set(ATTR_REQUIRED, "True")

                if (field.observable_field is not None) and (field.observable_field != ""):
                    ObservableField = ET.SubElement(Field, ELEM_OBSERVABLE_FIELD)
                    ObservableField.text = field.observable_field

                if field._shortkey is not None:
                    for mod in field._shortkey[0]:
                        Modifier = ET.SubElement(Field, ELEM_MODIFIER)
                        Modifier.text = mod

                    Key = ET.SubElement(Field, ELEM_KEY)
                    Key.text = field._shortkey[1]

                if field.dataprov_type is not None:
                    DataProvider = ET.SubElement(Field, ELEM_DATA_PROVIDER)
                    DataProvider.text = field.dataprov_type.name

        # make XML file human readable (add necessary spaces and new lines)
        self.__pretty_write(root)

        # write XML root into the file
        ET.ElementTree(root).write(self._path, encoding="UTF-8", xml_declaration=True, short_empty_elements = False)


