"""An atomic, thread-safe incrementing counter."""
# pylint: disable=too-few-public-methods
import threading
from abc import ABCMeta, abstractmethod

__all__ = ['BaseCounter', ]


class BaseCounter(object):
    """Base class for counters, counter can be int counter,
    uuid counter, etc.

    Properties
    ----------
    value: any
        return last identified

    Methods
    -------
    inc(): any
        return incremented counter value

    """

    __metaclass__ = ABCMeta

    def __init__(self, start=None):
        """Initialize a default values"""
        self._value = start
        self._lock = threading.Lock()

    @property
    def value(self):
        """return last stored value"""
        return self._value

    @abstractmethod
    def inc(self):
        """Atomically increment the counter and return the
        new value.
        """
        return


class BaseProcessor(object):
    """Base processor is abstract class with one method only for processing
    different kind of text processors

    Methods
    -------
    process(): generator
        executes processing different text processors
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self):
        """base process method should return generator"""
        return


class BaseAsDict(object):
    """This class is base for every class which uses slots bcs
    slots not allowing __dict__ attribute and there is some
    enhanced feature like specify fields and mappings

    Methods
    -------
    as_dict(fields, mappings): dict
        converting object to dict using fields spec and mappings of fields
    """

    __slots__ = ()

    def as_dict(self, fields=None, mappings=None):
        """converting object to dictionary data type, excluding private fields
        if you want to use custom attributes you can use fields argument

        Parameters
        ----------
        fields : list or tuple
            specify list of fields for forming new dict
        mappings: dict
            specify dict with map of fields

            Example
                {'pin': 1234} map to {'id': 1234}

        Returns
        -------
        dict
            dictionary bcs we use __slots__ for performance
        """
        _fields = self.__slots__
        if fields:
            _fields = fields
        _mappings = {key: key for key in _fields}
        if mappings:
            _mappings.update(mappings)
        return {_mappings[key]: getattr(self, key) for key in _fields if not key.startswith('_')}
