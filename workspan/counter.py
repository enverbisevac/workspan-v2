"""Counter module at the moment only define one class Counter
based on integer value, if you need customization you can iherit from
Counter.
"""
from base import BaseCounter

__all__ = ['Counter', ]


class Counter(BaseCounter):

    """ Description	"""

    def __init__(self, start=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        super(Counter, self).__init__(start)

    def inc(self):
        """Atomically increment the counter by 1 and return the
        new value.
        """
        with self._lock:
            self._value += 1
            return self._value
