"""Module clone is home for Cloner classes like EntityCloner
you can define new Cloners based on your needs you just need
to inherit from BaseCloner class

Classes
-------
EntityCloner
"""

__all__ = ['EntityCloner', ]

class EntityCloner(object):
    """EntityCloner class

    Properties
    ----------
    entity: Entity

    Methods
    -------
    clone(): Entity
        method for returning cloned object

    """

    def __init__(self, entity, counter):
        if entity is None:
            raise Exception("Entity cant be None")
        self._entity = entity
        self._counter = counter

    @property
    def entity(self):
        """propertie entity"""
        return self._entity

    def clone(self):
        """cloning method"""
        cloned_entity = self._entity.clone()
        self._entity.link_to(cloned_entity)
        self._generate_ids(cloned_entity)
        return cloned_entity

    def _generate_ids(self, cloned_entity):
        """method for generating new identity values for cloned objects"""
        arr = []
        def new_id(entity):
            """nested function for generate id"""
            entity.entity_id = self._counter.inc()
            for link in entity.links:
                if link in arr:
                    break
                arr.append(link)
                new_id(link)
        new_id(cloned_entity)
