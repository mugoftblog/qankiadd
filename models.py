
from dataprov.dataprov_factory import *

class FieldModel:

    TEXT_LEN_MAX = 3000

    def __init__(self, field_cfg):
        """
        :param field_cfg: field configuration
        """
        self.cfg = field_cfg
        self.observers = []
        self._text = ""
        self._dataprov = None

    def set_dataprov(self, dataprov):
        self._dataprov = dataprov

    def set_text(self, text):
        text_set = text
        if len(text) > self.TEXT_LEN_MAX:
            print("LOG: Model % s: text with length %u exceeds max length %u" % (self.cfg.name, len(text), self.TEXT_LEN_MAX))
            text_set = text_set[:self.TEXT_LEN_MAX]

       # if self._dataprov is not None:
            #self._dataprov.update_data(text_set)
            #text_set = self._dataprov.get_data()

        self._text = text_set

        for observ in self.observers:
            observ.set_text(self._text)

    def add_observer(self, observer):
        if observer.cfg.name == self.cfg.name:
            print("LOG: field \"%s\" can't add observer with the same name" % self.cfg.name)
            observer.cfg.observable_name = ""
        elif observer.cfg.name == self.cfg.observable_name:
            print("LOG: field \"%s\" can't add observer with the name equal to observable name" % self.cfg.name)
            self.cfg.observable_name = ""
        else:
            print("LOG: field \"%s\": observer \"%s\" is added" % (self.cfg.name, observer.cfg.name))
            self.observers.append(observer)

    def get_text(self):
        return self._text

    def get_text_max(self):
        return self.TEXT_LEN_MAX


class ModelManager:
    "IDs are indexes within the list"
    def __init__(self, cfg):
        """
        :param cfg: configuration
        """
        self._cfg = cfg
        self._fields = {}

        #list with fields which should be added as observers
        observer_fields = []

        #create dictionary with fields
        for field_cfg in self._cfg.field_cfgs:
            self._ensure_name_unique(field_cfg)
            field = FieldModel(field_cfg)

            if field_cfg.dataprov_type is not DataProvTypes.INVALID:
                data_prov = get_dataprov_factory(field_cfg.dataprov_type)
                field.set_dataprov(data_prov)

            self._fields[field_cfg.name] = field


            if (field_cfg.observable_name is not None) and (field_cfg.observable_name.strip() is not ""):
                observer_fields.append(field)

        for observ in observer_fields:
            if observ.cfg.observable_name in self._fields:
                field = self._fields[observ.cfg.observable_name]
                field.add_observer(observ)
            else:
                print("LOG: wrong observable name \"%s\" (doesn't exist)" % observ.cfg.observable_name)
                observ.observable_name = None

            #add observer to the observable field

    def _set_id(self, m):
        raise NotImplementedError
        #while 1:
            #id = str(int(time.time()*scale))
            #if id not in self.models:
            #    break
        #m['id'] = id

    def _ensure_name_unique(self, field_cfg):
        name_old = field_cfg.name
        if name_old in self._fields:
            print("NOT UNIQUE: %s observable %s" % (name_old, field_cfg.observable_name))
            # name_new = checksum(str(time.time())
            name_new = name_old + "_UNIQUE"
            # new name is assinged
            field_cfg.name = name_new

    def get_field(self, field_name):
        ret = None
        if field_name in self._fields:
            return self._fields[field_name]
        else:
            print("LOG: field with name % doesn't exist" % field_name)

        return None

    def update(self, m):
        "Update an existing field. "
        self._ensure_name_unique(m)
        self.models[str(m['id'])] = m
        # mark registry changed, but don't bump mod time
        self.save()

    def save_all(self):
        raise NotImplementedError
        "Save fields"

    def contains_id(self, id):
        return str(id) in self.models

    def get_ids(self):
        return list(self.models.keys())

    def get_name(self):
        return self.name

    def get(self, id):
        "Get field with ID, or None."
        id = str(id)
        if id in self.models:
            return self.models[id]

    def get_fields(self):
        "Get all fields."
        raise NotImplementedError