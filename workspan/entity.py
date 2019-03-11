# -*- coding: utf-8 -*-
"""Entity module summary

Classes
-------
    Entity
"""
import copy
from workspan.base import BaseAsDict

__all__ = ['Entity', ]


class Entity(BaseAsDict):
    """
    Entity class is used as vertex in this project, so it has two important
    roles to keep connections and links to other entities.

    Attributes
    ----------
    entity_id : int
        unique identifier for entity instance
    name : str
        name your entity instance
    description : str
        detail information about your entity instance
    connections : tuple
        list of connected entities to instance
    links : tuple
        list of linked entities from this instance

    Methods
    -------
    link_to(entity)
        linking to other entity
    connected_from(entity)
        backward link to entity
    clone(entity)
        clone entity and all linked entites and connect all links from original entity
        ** you can use copy.deepcopy ** its same functionality
    """
    # memory optimization
    __slots__ = ('entity_id', 'name', 'description', '_links', '_connections')

    def __init__(self, entity_id=None, name=None, description=None):
        """Constructor

        Parameters
        ----------
        entity_id : int
            identify this entity with unique number (the default is None,
            which can be set by any int value)
        name : str
            name of this entity (the default is None)
        description : str
            more details about entity (the default is None)
        """

        self.entity_id = entity_id
        self.name = name
        self.description = description

        # private fields
        self._links = []
        self._connections = []

    def link_to(self, entity, force=False):
        """This method links object to entity while at the same time
        adding connection to linked entity. This is important to know
        who is connected to this entity.

        Parameters
        ----------
        entity : Entity
            destination object for direct linking
        """

        # check if is the linking to this object and if exists in links
        if not force and (entity == self or entity in self._links):
            return False
        # allow only instances of class Entity or inherited class
        if isinstance(entity, Entity):
            self._links.append(entity)
            # every linked entety has info about connected entity
            entity.connected_from(self, force)
            return True
        return False

    def connected_from(self, entity, force=False):
        """Connected from entity

        Parameters
        ----------
        entity : Entity
        """
        # avoid same entity and existing one
        if not force and (entity == self or entity in self._connections):
            return False
        # allow only instances of class Entity or inherited class
        if isinstance(entity, Entity):
            self._connections.append(entity)
            return True
        return False

    @property
    def connections(self):
        """property connections (readonly), for new connections you must use
        connected_from() method

        Returns
        -------
        tuple
            collection of entities connected to this object (entity)
        """
        # readonly
        return tuple(self._connections)

    @property
    def links(self):
        """property links (readonly), for new links you must use
        link_to method

        Returns
        -------
        tuple
            of linked entites
        """
        # readonly
        return tuple(self._links)

    def siblings(self):
        """list all nested entities

        Returns
        -------
        list
            list of entities
        """

        siblings = []

        def traverse(entity, memo):
            """travers all nodes and fill list"""
            not_there = False
            existing = memo.get(entity, not_there)
            if existing:
                return
            siblings.append(entity)
            memo[entity] = entity
            for link in entity.links:
                traverse(link, memo)
        traverse(self, {})
        return siblings

    def clone(self):
        """clone method is just shortcut for deepcopy

        Returns
        -------
        Entity
            Cloned object of this instance
        """
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        """override for deepcopy use"""
        def copy_entity(entity, memo_cp):
            """recursive copy entity"""
            not_there = False
            existing = memo_cp.get(entity, not_there)
            if existing:
                return existing
            dup = Entity(copy.deepcopy(entity.entity_id, memo_cp),
                         copy.deepcopy(entity.name, memo_cp))
            memo_cp[entity] = dup
            for link in entity.links:
                dup.link_to(copy_entity(link, memo_cp))
            return dup

        cloned = copy_entity(self, memo)
        # copy all connections to cloned object
        if self.connections:
            for conn in self.connections:
                conn.link_to(cloned, True)
        return cloned

    def __str__(self):
        return '%s - %d' % (self.name, self.entity_id)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.entity_id == other.entity_id and self.name == other.name
        return False

    def __ne__(self, other):
        if isinstance(self, other.__class__):
            return self.entity_id != other.entity_id or self.name != other.name
        return False
