"""Graph module with one simple Graph class

Classes
-------
Graph
"""

import json
from workspan.processors import FileFactoryProcessor
from workspan.entity import Entity
from workspan.link import Link


__all__ = ['Graph', ]


class Graph(object):
    """

    Properties
    ----------
    entities: tuple
    links: tuple

    Methods
    -------
    load_from_file(filename : str) : void
    save_to_file(filename : str): void
    get_last_id(): any
    add_entity(entity: Entity): void
    add_link(link: Link): void
    find_entity_by_id(id: any): Entity

    """
    _ENTITIES_ITEM = "entities.item"
    _LINKS_ITEM = "links.item"

    def __init__(self):
        self._last_id = 0
        self._entities = []

        self.listeners = {
            self._ENTITIES_ITEM: self.add_entity,
            self._LINKS_ITEM: self.add_link
        }

    def load_from_file(self, filename):
        """loading data from file

        Parameters
        ----------
        filename : str
            loading file name content for processing

        """

        self._last_id = 0
        self._entities = []
        processor = FileFactoryProcessor(
            filename, [self._ENTITIES_ITEM, self._LINKS_ITEM])

        for prefix, item in processor.process():
            self.listeners[prefix](item)

    def save_to_file(self, filename):
        """saving objects to json file, maybe it will be better
        to use generator and writing to file bcs of performance and memory
        consumption.

        Parameters
        ----------
        filename : str

        """

        collection = {
            "entities": [entity.as_dict() for entity in self.entities],
            "links": [
                link.as_dict(
                    mappings={
                        "from_entity": "from",
                        "to_entity": "to"}) for link in self.links]
        }
        with open(filename, 'w') as save_file:
            json.dump(collection, save_file, indent=4)

    def get_last_id(self):
        """getting last inserted id

        Returns
        -------
        any
            can be int, uuid etc
        """

        return self._last_id

    def add_entity(self, entity):
        """Adding entity

        Parameters
        ----------
        entity : Entity
            adding entity to entities

        Raises
        ------
        Exception
            Entity cant be None

        """

        if entity is None:
            raise Exception("Entity cant be None")

        new_entity = entity
        if isinstance(entity, dict):
            new_entity = Entity(**entity)

        if new_entity.links:
            for item in entity.siblings():
                self._entities.append(item)
        else:
            self._entities.append(new_entity)
        # bcs data can be unordered we have to do this
        if new_entity.entity_id > self._last_id:
            self._last_id = new_entity.entity_id

    def add_link(self, link):
        """add link to links

        Parameters
        ----------
        link : Link
            add link to links

        Raises
        ------
        Exception
            link cant be empty

        """

        if link is None:
            raise Exception("Link cant be None")
        new_link = link
        if isinstance(link, dict):
            new_link = Link(link["from"], link["to"])
        from_entity = self.find_entity_by_id(new_link.from_entity)
        to_entity = self.find_entity_by_id(new_link.to_entity)
        from_entity.link_to(to_entity)

    def find_entity_by_id(self, entity_id):
        """find entity with entity id

        Parameters
        ----------
        id : int
            find enitity by id of entity

        Returns
        -------
        Entity
            with entity_id
        """
        for entity in self._entities:
            if entity.entity_id == entity_id:
                return entity
        return None

    @property
    def entities(self):
        """retern readonly entities

        Returns
        -------
        tuple
            list of entities
        """

        return tuple(self._entities)

    @property
    def links(self):
        """return read only links

        Returns
        -------
        tuple
            of link objects
        """

        links_arr = []
        for entity in self.entities:
            for link in entity.links:
                links_arr.append(Link(entity.entity_id, link.entity_id))
        return tuple(x for x in set(links_arr))
