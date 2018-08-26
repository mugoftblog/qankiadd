import logging
from dataprov.factory import *
from keylistener import *
from exporting.base import *


SHORTKEY_SAVEALL_DEFAULT = (('ctrl', 'shift'), 's')
""" Deault shortkey to save the text of all fields into the file.  """

SHORTKEY_CLEARALL_DEFAULT = (('ctrl', 'shift'), 'l')
""" Deault shortkey to clear the text of all fields.  """


class FieldModel(KeylistenerObserver):
    TEXT_LEN_MAX = 3000
    """ Maximum allowed lenght of the text in the fields. """

    def __init__(self, field_cfg):
        """
        This class represents the model of the passed field configuration.
        The controlling of this model is performed via :class:`.ModelManager`.

        :param field_cfg: field configuration
        :type field_cfg: :class:`config.FieldCfg`
        """
        self.cfg = field_cfg
        KeylistenerObserver.__init__(self, [self.cfg._shortkey])
        self.observers = []
        self._text = ""
        self._dataprov = None
        # self._id = None

    def set_dataprov(self, dataprov):
        """
        Sets the data provider which is related to the model/configuration.

        :param dataprov: data provider related to the model/configuration.
        :type dataprov: :class:`dataprov.base.DataProv`
        """
        self._dataprov = dataprov

    def key_pressed(self, shortkey):
        if self.compare_shortkeys(self.cfg._shortkey, shortkey):
            logging.debug("Key is pressedsss (%s, %s)" % (shortkey[0], shortkey[1]))
            # just get text from the data provider
            self.set_text("")

    def set_text(self, text):
        """
        Based on the configuration either directly updates the text of the model with the passed text,
        or first receives dataprovider data (which is returned from the data provider based on the passed text)
        and only then updates the text of this model with the dataprovider data.
        At the end all observers are notified with the text of the model.

        :param text: text to set
        """
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

    def clear(self):
        """
        Clears the text of the model.
        """
        self._text = ""

    def add_observer(self, observer):
        """
        Registers the passed instance as an observer of this model.

        :param observer: the passed observer to register
        :type observer: :class:`.FieldModel`
        """

        if issubclass(type(observer), FieldModel):
            if observer.cfg.name == self.cfg.name:
                logging.warning("can't add observer for the field \"%s\" with the same name" % self.cfg.name)
                observer.cfg.observable_field = ""
            elif observer.cfg.name == self.cfg.observable_field:
                logging.warning(
                    "can't add observer for the field \"%s\" with the name equal to observable name" % self.cfg.name)
                self.cfg.observable_field = ""
            else:
                logging.debug("observer \"%s\" for the field \"%s\" is added" % (self.cfg.name, observer.cfg.name))
                self.observers.append(observer)
        else:
            logging.error("FieldModel is expected as observer")
            sys.exit(1)

    def get_text(self):
        """
        Return the text of the model.

        :return: the text of the model
        """
        return self._text

    def get_text_max(self):
        """
        Return the maximum allowed text length of the model

        :return: the maximum allowed text length of the model
        """
        return self.TEXT_LEN_MAX


class ModelManager(KeylistenerObserver):
    def __init__(self, cfg, exporter, shortkey_saveall, shortkey_clearall):
        """
        Perform the management of the field models:
        based on the read configurations from the file, this class takes care about correct creation of the
        field models (e.g. correct assigning observers to the field models, or acquiring correct data providers
        and assigning them to the correct field models). Also it takes care about checking the names of the
        field configurations for the uniqueness. If name is not unique, it appends to this name unique identifier
        which makes the name unique. Also this class makes sure that field configiration doesn't contain its own
        name in the list of observers. !!!Therefore please note, that the passed configuration
        can be changed after passing to this class!!!


        :param cfg: the configuration read from the config file
        :type cfg: :class:`config.Config`
        :param exporter: exporter which is resposnsible for storing field's text into the file
        :type exporter: :class:`.exporting.base.Exporter`
        :param shortkey_saveall: the shortkey which should be pressed to export the text of all field models
                                 into the file. In case 'None' is given the default shortkey is used
                                 (:data:`.SHORTKEY_SAVEALL_DEFAULT`)
        :param shortkey_clearall: the shortkey which should be pressed to clear the text of all field models.
                                  In case 'None' is given the default shortkey is used
                                  (:data:`.SHORTKEY_CLEARALL_DEFAULT`)

        """
        self._shortkey_saveall = shortkey_saveall
        if self._shortkey_saveall is None:
            self._shortkey_saveall = SHORTKEY_SAVEALL_DEFAULT

        self._shortkey_clearall = shortkey_clearall
        if self._shortkey_clearall is None:
            self._shortkey_clearall = SHORTKEY_CLEARALL_DEFAULT

        KeylistenerObserver.__init__(self, [self._shortkey_saveall,  self._shortkey_clearall])
        self._exporter = exporter

        self._cfg = cfg
        self._fields = {}

        # list with fields which should be added as observers
        observer_fields = []

        # create dictionary with fields
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
        """
        Checks wether the name of the passed field configuration is already used by another field configuration or not.
        In case the name is not unique it makes it unique by appending to the end of the name unique identifier.

        :param field_cfg: the field configuration which name should be checked for the uniqueness
        :type field_cfg: :class:`config.FieldCfg`
        :return: new name of the field confgiration
        """
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
        """
        Searches for the field based on the passed field name.

        :param field_name: the name of the field to find
        :return: the found field (if found), otherwise None.
        """
        ret = None
        if field_name in self._fields:
            return self._fields[field_name]
        else:
            logging.warning("field with name % doesn't exist" % field_name)

        return None

    def key_pressed(self, shortkey):
        if self.compare_shortkeys(self._shortkey_saveall, shortkey):
            self.save_all()
        elif self.compare_shortkeys(self._shortkey_clearall, shortkey):
            self.clear_all()

    def save_all(self):
        """
        Export the text of all field models if all required conditions are met (e.g. if all required field models
        contain the text).
        """
        logging.debug("save_all")
        fields = self.get_fields()

        fields_empty = []
        # check if all required fields are not empty
        for field in fields:
            if field.cfg._required:
                if not field.get_text():
                    fields_empty.append((field.cfg.name))

        if len(fields_empty) == 0:
            # export field models
            self._exporter.write(fields)
            # clear text from fields
            self.clear_all()
        else:
            logging.info("can't export: required fields %s are still empty" % fields_empty)

    def clear_all(self):
        """
        Clear the tet of all field models.
        """
        logging.debug("clear_all")
        fields = self.get_fields()
        for field in fields:
            field.clear()

    def get_name(self):
        """
        Return the name of the configuration assigned to this model manager.
        :return: the name of the configuration assigned to this model manager.
        """
        return self.name

    def get_fields(self):
        """
        Return all field models assigned to this model manager.

        :return: all field models assigned to this model manager.
        """
        return list(self._fields.values())