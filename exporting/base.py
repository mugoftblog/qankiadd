import os
import os.path
import sys
import logging
import datetime

from models import *

OUTPUT_DIR = "output"
OUTPUT_FORMAT = "output/%s_%s.%s"
FILE_SIZE_MAX_DEFAULT = 10000 # size in bytes


class Exporter:
    def __init__(self):
        self._path = ""

    def get_path(self):
        return self._path

    def write(self, field_models):
        raise NotImplementedError('subclasses must override write()!')


class FileExporter(Exporter):
    """ class for exporting data from the fields into the files """
    def __init__(self):
        Exporter.__init__(self)
        self.filename = ""
        self.extension = ""

        self._size_max = FILE_SIZE_MAX_DEFAULT

    def check_update_path(self, force_update = False):
        """ check file in the specified path and if necessary create new file
        (e.g. if the file is already too big)
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
