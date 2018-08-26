from exporting.base import *

"""
The calsses and methods of the anki exporter.

Anki exporter allows to save field's data into anki compatable format.
"""


class AnkiExporter(TextFileExporter):
    def __init__(self):
        """
        The calss which writes field's data into the file which later can be imported into the Anki.
        """
        TextFileExporter.__init__(self)
        self.filename = "anki"
        self.extension = "txt"
        self.check_update_path()

    def write(self, field_models):
        self.check_update_path()

        path_old = self.get_path()
        do_try = True
        while do_try:
            try:
                with open(self.get_path(), 'ab') as f:
                    # no errors, write to the file
                    line = ""
                    for field in field_models:
                        line += field.get_text() + ";"

                    line = line[:-1]  # remove last semicolon
                    line += "\r\n"
                    f.write(line.encode('utf-8'))
                    do_try = False
            except IOError as e:

                if do_try:
                    if self.get_path() == path_old:
                        # as we can't write data into the old path - create new one
                        self.check_update_path(True)
                        logging.error("%s, path=\"%s\", update the path" % (e, path_old))
                    else:
                        # we tried to write data into the new path but some error occured
                        do_try = False

                if not do_try:
                    # if we can't write data into the new path
                    # or we can't close the file
                    # some critical error occured - can't continue anymore
                    line = ""
                    for field in field_models:
                        line += field.get_text() + ";"
                    line += "\r\n"

                    logging.info(line.encode('utf-8'))
                    logging.error("%s, path=\"%s\", exit the program" % (e, self.get_path()))
                    do_try = False
                    #self.check_update_path(True)
                    sys.exit(0)
