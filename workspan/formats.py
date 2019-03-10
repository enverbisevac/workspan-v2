"""Formats module is for handling a lot of different
formats of input files, in this module is JSONFormat
but you can inherit BaseProcessor so extend formats
like YAML

Classes
-------
JSONFormat
"""

import ijson
from workspan.base import BaseProcessor


class JSONFormat(BaseProcessor):
    """Basic json format processor, iterative so
    its memory efective

    Methods
    -------
    register_prefix(prefix: str) : void
        register prefix for processing, prefix can be item, entity
    set_prefixes(prefixes: list) : void
        set list of prefixes

    """

    START_MAP = 'start_map'
    END_MAP = 'end_map'
    MAP_KEY = 'map_key'

    def __init__(self, file_handle):
        self._prefixes = []
        self._file_handle = file_handle

    def register_prefix(self, prefix):
        """register prefix in list of prefixes

        Parameters
        ----------
        prefix : str
            prefix can be item, link etc.

        """

        self._prefixes.append(prefix)

    def set_prefixes(self, prefixes):
        """set list of prefixes

        Parameters
        ----------
        prefixes : list
            set prefixes for further processing items

        """

        self._prefixes = prefixes

    def process(self):
        """processing file handle, file handle can be memory, file, url
        this can be obtained from FileFactoryBuilder

        Raises
        ------
        Exception
            when prefixes are empty
        IOError
            when file_handle is empty

        """
        if self._file_handle is None:
            raise IOError()
        if not self._prefixes:
            self._file_handle.close()
            raise Exception(
                "Prefixes cant be empty! for first level you can use ''")
        parser = ijson.parse(self._file_handle)
        entity = {}
        last_key = None
        for prefix, event, value in parser:
            if prefix in self._prefixes and event == self.START_MAP:
                entity = {}
            elif event == self.MAP_KEY:
                last_key = value
            elif prefix.endswith('%s' % last_key):
                entity[last_key] = value
            elif prefix in self._prefixes and event == self.END_MAP:
                yield prefix, entity
        self._file_handle.close()
