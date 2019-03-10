"""Graph testing module"""
# pylint: disable=redefined-outer-name
import pytest
from workspan.entity import Entity
from workspan.graph import Graph


@pytest.fixture()
def repository_setup():
    """fixture"""
    return Graph()


def test_add_entity_by_dict(repository_setup):
    """add object dict to entities"""
    entity = {
        "entity_id": 3,
        "name": "EntityA"
    }
    repository_setup.add_entity(entity)
    assert entity == repository_setup.entities[0].as_dict(
        fields=['entity_id', 'name'])


def test_found_entity(repository_setup):
    """test finding entity"""
    expected = Entity(3, "EntityA")
    repository_setup.add_entity(expected)
    got = repository_setup.find_entity_by_id(3)
    assert got == expected


def test_not_found_entity(repository_setup):
    """test not found entity"""
    expected = Entity(3, "EntityA")
    repository_setup.add_entity(expected)
    got = repository_setup.find_entity_by_id(5)
    assert got is None
