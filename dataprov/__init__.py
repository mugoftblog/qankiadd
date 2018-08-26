"""
This package contains various data providers which return some data based on the specified text.
E.g. if you use "google" data provder and ask for the data for the specified text, the "google" returns
the translation of the specified text to the specified in the settings language.
Another example: if you use "clipboard" data provider and ask for the data, the "clipboard" returns
the data from the clipboard buffer.

If you would like to add new data provider please
create new module with the name of the data provider and
add to this module the following classes:

- data provider class which has to be inherited from the data provider base class (see :class:`.base.DataProv`).

- data provider factory class which has to be inherited from the data provider factory base class \
(see :class:`.base.DataProvFactory`).

Don't forget to add the information about new data provider to the module "factory.py"
(e.g. update :class:`.factory.DataProvType`).
"""