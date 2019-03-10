"""Entity testing module"""
# pylint: disable=redefined-outer-name
import copy
import pytest
from workspan.entity import Entity


@pytest.fixture()
def setup_entities():
    """setup entities with function scope for later use"""
    entity_a = Entity(3, "EntityA")
    entity_b = Entity(5, "EntityB")
    return entity_a, entity_b


def test_str(setup_entities):
    """entity string format"""
    entity, _ = setup_entities
    assert str(entity) == "EntityA - 3"


def test_link_to_wrong_type(setup_entities):
    """only Entity instance can be added"""
    entity, _ = setup_entities
    entity.link_to(1)
    assert not entity.links


def test_self_linking(setup_entities):
    """test linking to self"""
    entity_a, _ = setup_entities
    entity_a.link_to(entity_a)
    # this two methods are in relation so two assert is not a problem
    assert not entity_a.links
    assert not entity_a.connections


def test_prop_links_readonly(setup_entities):
    """testing links readonly"""
    entity, _ = setup_entities
    with pytest.raises(Exception):
        entity.links.append(1)  # pylint: disable=no-member


def test_prop_connections_readonly(setup_entities):
    """testing connections readonly"""
    entity, _ = setup_entities
    with pytest.raises(Exception):
        entity.connections.append(1)  # pylint: disable=no-member


def test_duplicate_entity_links(setup_entities):
    """in both cases it should be one because in first
    case linking to origin object is not allowed and second case
    linked entity is already linked
    """
    entity_a, entity_b = setup_entities
    entity_a.link_to(entity_b)
    entity_a.link_to(entity_b)
    assert entity_a.links


def test_entity_link_to(setup_entities):
    """this is normal one direction linking"""
    entity_a, entity_b = setup_entities

    assert entity_a.link_to(entity_b)
    assert len(entity_a.links) == 1
    assert entity_b == entity_a.links[0]


def test_entity_connection_from(setup_entities):
    """testing list of connections from entity"""
    entity_a, entity_b = setup_entities

    assert entity_a.link_to(entity_b)
    assert len(entity_b.connections) == 1
    assert entity_a == entity_b.connections[0]


def test_deepcopy_references(setup_entities):
    """checking copying mutable types"""
    entity_a, entity_b = setup_entities
    entity_a.link_to(entity_b)
    # cloning
    entity_c = copy.deepcopy(entity_a)

    assert id(entity_a) != id(entity_c)

    # checking immutable types
    assert id(entity_a.links) != id(entity_c.links)
    assert id(entity_a.links[0]) != id(entity_c.links[0])


def test_deep_copy(setup_entities):
    """cloning of root object with one link"""
    entity_a, entity_b = setup_entities
    entity_a.link_to(entity_b)
    # cloning
    entity_c = copy.deepcopy(entity_a)

    assert entity_a == entity_c
    # entity_a links + link to entity c
    assert len(entity_a.links) == len(entity_c.links)
    # check if number of connections are equal
    assert not entity_c.connections


def test_deep_copy_1(setup_entities):
    """cloning of nested object with one link"""
    entity_a, entity_b = setup_entities
    entity_c = Entity(7, 'EntityC')
    # linking
    entity_a.link_to(entity_b)
    entity_b.link_to(entity_c)

    # cloning
    entity_d = copy.deepcopy(entity_b)

    assert entity_b == entity_d
    # entity_a links + link to entity c
    assert len(entity_b.links) == len(entity_d.links)
    # check if number of connections are equal
    assert len(entity_d.connections) == 1


def test_deep_copy_rec_link(setup_entities):
    """cloning of root object with one link per entity and one reverse link"""
    entity_a, entity_b = setup_entities
    entity_c = Entity(7, 'EntityC')
    entity_d = Entity(9, 'EntityD')
    # linking
    entity_a.link_to(entity_b)
    entity_b.link_to(entity_c)
    entity_c.link_to(entity_d)
    entity_d.link_to(entity_b)
    # cloning
    entity_e = copy.deepcopy(entity_a)

    assert entity_e == entity_a
    # entity_a links + link to entity c
    assert len(entity_a.links) == len(entity_e.links)


def test_deep_copy_rec_link_nested(setup_entities):
    """cloning of nested object with one link per entity and one reverse link"""
    entity_a, entity_b = setup_entities
    entity_c = Entity(7, 'EntityC')
    entity_d = Entity(9, 'EntityD')
    # linking
    entity_a.link_to(entity_b)
    entity_b.link_to(entity_c)
    entity_c.link_to(entity_d)
    entity_d.link_to(entity_b)
    # cloning
    entity_e = copy.deepcopy(entity_b)

    assert entity_e == entity_b
    assert len(entity_b.links) == len(entity_e.links)
    # e should  have one connection from origin b
    # and one connection from a
    # and one connection from d
    assert len(entity_e.connections) == 3
