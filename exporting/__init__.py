"""
This package contains various exporters which are used for exporting field's data
into the specified output file/database/... . E.g. if you would like to store the text of the fields
into the text file which can be then imported into the anki, you can use "anki" exporter.

If you would like to add new exporter please create new module with the name of the exporter and add class
inherited from the one of the base classes (e.g. :class:`.base.TextFileExporter`).
"""