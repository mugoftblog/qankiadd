import os
import os.path
import sys
import logging
import datetime

"""
Base classes for exporting the data of the fields.
"""

from models import *

OUTPUT_DIR = "output"
""" Output directory of the export file """

OUTPUT_FORMAT = "output/%s_%s.%s"


class Exporter:
    def __init__(self):
        """
        Base class for all exporters.
        """
        self._path = ""

    def get_path(self):
        """
        Returns the output path.

        :return: the path to where the data is exported.
        """
        return self._path

    def write(self, field_models):
        """
        Writes the data from the passed field models into the output.

        :param field_models: field models with the data to write
        :type field_models: list of :class:`.models.FieldModel`
        """
        raise NotImplementedError('subclasses must override write()!')


class TextFileExporter(Exporter):
    FILE_SIZE_MAX_DEFAULT = 10000
    """ Maximum size of the export file after which new file should be created. """

    def __init__(self):
        """
        Base class for exporters which are used for exporting field's data into the text files.
        """
        Exporter.__init__(self)
        self.filename = ""
        self.extension = ""

        self._size_max = TextFileExporter.FILE_SIZE_MAX_DEFAULT

    def check_update_path(self, force_update = False):
        """ Check file in the specified path and if necessary create new file
        (e.g. if the file is already too big)

        :param force_update: if True create new file for export, if False create new file for the export only if\
         all other conditions are met.
        """
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        is_path_ok = True
        if not os.path.isfile(self._path):
            is_path_ok = False
            logging.debug("file \"%s\" doesn't exist" % self._path)
        else:
            statinfo = os.stat(self._path)

            if (self._size_max is not None) and (self._size_max != 0):
                # Check size of the file and compare with the max allowed
                if statinfo.st_size >= self._size_max:
                    is_path_ok = False
                    logging.debug("file \"%s\" is already too big" % self._path)

        if not is_path_ok:
            self._path = OUTPUT_FORMAT % (self.filename, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f"), self.extension)
            # new file and directory create
            logging.debug("new file path \"%s\"" % self._path)

    def write(self, field_models):
        raise NotImplementedError('subclasses must override TextFileExporter.write()!')
