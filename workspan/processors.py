"""factory module

Classes
-------
FileFactoryProcessor
"""
# pylint: disable=too-few-public-methods
import os
from workspan.base import BaseProcessor
from workspan.formats import JSONFormat
from workspan.settings import MISSING_INPUT_FILE_NAME


class FileFactoryProcessor(BaseProcessor):
    """factory for build processor based on file format

    Methods
    -------
    process() : void
    """

    formats = {
        'json': JSONFormat
    }

    def __init__(self, filename, prefixes, file_format=None):
        if filename is None or filename == '':
            raise Exception(MISSING_INPUT_FILE_NAME)
        self.filename = filename
        self.file_format = self._get_file_format(file_format)
        self.prefixes = prefixes

    def _get_file_format(self, file_format=None):
        """get format private method

        Parameters
        ----------
        file_format : str, optional
            default is None, method can resolve format if is not specified

        Returns
        -------
        str
            like .json, .yml etc.
        """

        if file_format:
            return file_format.lower()
        _, file_extension = os.path.splitext(self.filename)
        if file_extension:
            if file_extension.startswith('.'):
                file_extension = file_extension[1:]
            return file_extension.lower()
        return None

    def _get_formats(self):
        """get registered formats

        Returns
        -------
        dict, None
            return dict of formats with processor classes or None if formats is None
        """

        if self.formats:
            return self.formats
        return None

    def process(self):
        """processing based on format

        Raises
        ------
        Exception
            No format specified

        Returns
        -------
        void
        """

        if self._get_formats():
            file_handle = open(self.filename, 'r')
            processor = self.formats[self.file_format](file_handle)
            processor.set_prefixes(self.prefixes)
            # return generator
            return processor.process()
        else:
            raise Exception('No formats registered')
