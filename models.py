import logging
from dataprov.factory import *
from keylistener import *
from exporting.base import *


KEY_SAVE = 's'
KEY_SAVE_TUPLE_STR = ('ctrl', KEY_SAVE)


class FieldModel(KeylistenerObserver):
    TEXT_LEN_MAX = 3000

    def __init__(self, field_cfg):
        """
        :param field_cfg: field configuration
        """
        self.cfg = field_cfg
        KeylistenerObserver.__init__(self, self.cfg._shortkey)
        self.observers = []
        self._text = ""
        self._dataprov = None
        # self._id = None

    def set_dataprov(self, dataprov):
        self._dataprov = dataprov

    def key_pressed(self, key_tuple_str):
        if key_tuple_str == self._key_tuple:
            logging.debug("Key is pressed (%s, %s)" % (key_tuple_str[0], key_tuple_str[1]))
            # just get text from the data provider
            self.set_text("")

    def set_text(self, text):
        logging.debug("Setting text")
        text_set = text
        if len(text) > self.TEXT_LEN_MAX:
            logging.warning("Model % s: text with length %u exceeds max length %u" % (self.cfg.name, len(text), self.TEXT_LEN_MAX))
            text_set = text_set[:self.TEXT_LEN_MAX]

        if self._dataprov is not None:
            self._dataprov.update_data(text_set)
            text_set = self._dataprov.get_text()

        self._text = text_set

        for observ in self.observers:
            observ.set_text(self._text)

    def add_observer(self, observer):
        if observer.cfg.name == self.cfg.name:
            logging.warning("can't add observer for the field \"%s\" with the same name" % self.cfg.name)
            observer.cfg.observable_field = ""
        elif observer.cfg.name == self.cfg.observable_field:
            logging.warning("can't add observer for the field \"%s\" with the name equal to observable name" % self.cfg.name)
            self.cfg.observable_field = ""
        else:
            logging.debug("observer \"%s\" for the field \"%s\" is added" % (self.cfg.name, observer.cfg.name))
            self.observers.append(observer)

    def get_text(self):
        return self._text

    def get_text_max(self):
        return self.TEXT_LEN_MAX


class ModelManager(KeylistenerObserver):
    "IDs are indexes within the list"
    def __init__(self, cfg, exporter):
        """
        :param cfg: configuration
        """
        KeylistenerObserver.__init__(self, KEY_SAVE_TUPLE_STR)
        self._exporter = exporter
        self._cfg = cfg
        self._fields = {}

        #list with fields which should be added as observers
        observer_fields = []

        #create dictionary with fields
        for field_cfg in self._cfg.field_cfgs:
            self._ensure_name_unique(field_cfg)
            field = FieldModel(field_cfg)

            if field_cfg.dataprov_type is not None:
                factory = get_dataprov_factory(field_cfg.dataprov_type)
                # check if factory exists for the specified type
                if factory is not None:
                    dataprov = factory.get_data_provider()
                    field.set_dataprov(dataprov)

            self._fields[field_cfg.name] = field

            if (field_cfg.observable_field is not None) and (field_cfg.observable_field.strip() is not ""):
                observer_fields.append(field)

        for observ in observer_fields:
            if observ.cfg.observable_field in self._fields:
                field = self._fields[observ.cfg.observable_field]
                field.add_observer(observ)
            else:
                print("LOG: wrong observable name \"%s\" (doesn't exist)" % observ.cfg.observable_field)
                observ.observable_field = None

    def _ensure_name_unique(self, field_cfg):
        name_new = field_cfg.name
        i = 0
        while (name_new in self._fields) or (name_new == ""):
            logging.warning("field name: %s observable %s" % (name_new, field_cfg.observable_field))
            # name_new = checksum(str(time.time())
            name_new = name_new + str(i) #TODO quick solution for making name unique
            i += 1

        # new name is assinged
        field_cfg.name = name_new

    def get_field(self, field_name):
        ret = None
        if field_name in self._fields:
            return self._fields[field_name]
        else:
            print("LOG: field with name % doesn't exist" % field_name)

        return None

    # def update(self, m):
    #     "Update an existing field. "
    #     self._ensure_name_unique(m)
    #     self.models[str(m['id'])] = m

    def key_pressed(self, key_tuple_str):
        if key_tuple_str == self._key_tuple:
            logging.debug("Key is pressed (%s, %s)" % (key_tuple_str[0], key_tuple_str[1]))
            self.save_all()

    def save_all(self):
        logging.debug("Saving all fields")
        self._exporter.write(self.get_fields())

    # def contains_id(self, id):
    #     return str(id) in self.models

    # def get_ids(self):
    #     return list(self.models.keys())

    def get_name(self):
        return self.name

    def get(self, id):
        "Get field with ID, or None."
        id = str(id)
        if id in self.models:
            return self.models[id]

    def get_fields(self):
        "Get all fields."
        return list(self._fields.values())