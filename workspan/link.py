"""link module for keeping track of link data

Classes
-------
Link
"""

from workspan.base import BaseAsDict

__all__ = ['Link', ]


class Link(BaseAsDict):
    """Link class"""

    __slots__ = ('from_entity', 'to_entity')

    def __init__(self, from_entity=None, to_entity=None):
        self.from_entity = from_entity
        self.to_entity = to_entity

    def __str__(self):
        return "from: %d, to: %d" % (self.from_entity, self.to_entity)
