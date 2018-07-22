from exporting.base import *


"""
The calsses and methods of the anki exporter

Anki exporter allows to save fields with questions, answers and other fields into anki compatable format.
"""


class AnkiExporterStub(FileExporter):
    def __init__(self):
        FileExporter.__init__(self)
        self.filename = "anki"
        self.extension = "txt"
        self._write_calls_n = 0  # how many times "write" function was called

    def write(self, field_models):
        # no errors, write to the file
        line = ""
        for field in field_models:
            line += field.get_text() + ";"

        line = line[:-1]  # remove last semicolon
        line += "\r\n"
        self._write_calls_n += 1
        print("AnkiExporterStub::write\n%s" % line)

