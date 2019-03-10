"""Integration testing for entity cloner"""
from workspan.entity import Entity
from workspan.clone import EntityCloner
from workspan.counter import Counter


def test_simple_clone():
    """single entity clone without links"""
    entity_a = Entity(3, "EntityA")
    start = entity_a.entity_id
    counter = Counter(start)
    cloner = EntityCloner(entity_a, counter)
    entity_c = cloner.clone()

    assert entity_a.name == entity_c.name


def test_clone():
    """entity cloning with links"""
    entity_a = Entity(3, "EntityA")
    entity_b = Entity(5, "EntityB")
    entity_a.link_to(entity_b)

    start = entity_b.entity_id
    counter = Counter(start)
    cloner = EntityCloner(entity_a, counter)
    entity_c = cloner.clone()

    assert entity_a.name == entity_c.name
    assert entity_a.links[0].name == entity_c.links[0].name


def test_circ_clone():
    """circular link and cloning"""
    entity_a = Entity(3, "EntityA")
    entity_b = Entity(5, "EntityB")
    entity_c = Entity(7, "EntityB")
    entity_a.link_to(entity_b)
    entity_b.link_to(entity_c)
    entity_c.link_to(entity_a)

    start = entity_c.entity_id
    counter = Counter(start)
    cloner = EntityCloner(entity_a, counter)
    entity_d = cloner.clone()

    assert entity_a.name == entity_d.name
    assert entity_a.links[0].name == entity_d.links[0].name

def test_generate_ids():
    """generating id of entites"""
    entity_a = Entity(3, "EntityA")
    counter = Counter(entity_a.entity_id)
    cloner = EntityCloner(entity_a, counter)
    entity_b = cloner.clone()
    assert entity_b.entity_id == entity_a.entity_id + 1
