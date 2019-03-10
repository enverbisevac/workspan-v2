"""graph integration tests"""
import pytest
from workspan.graph import Graph
from workspan.entity import Entity
from workspan.link import Link
from workspan.tests.integration import TEST_INPUT_FILE_NAME

# pylint: disable=redefined-outer-name
@pytest.fixture()
def repository_setup():
    """fixture"""
    return Graph()


@pytest.fixture()
def entities_setup():
    """fixtures"""
    entity_a = Entity(3, "EntityA")
    entity_b = Entity(5, "EntityB")
    entity_c = Entity(7, "EntityC")
    return entity_a, entity_b, entity_c


def test_add_entity_by_object(repository_setup):
    """test add entity object"""
    expected = Entity(3, "EntityA")
    repository_setup.add_entity(expected)
    got = repository_setup.entities[0]
    assert expected == got


def test_add_link_by_dict(repository_setup, entities_setup):
    """test adding link by dict"""
    entity_a, entity_b, _ = entities_setup
    repository_setup.add_entity(entity_a)
    repository_setup.add_entity(entity_b)
    link = {
        "from": entity_a.entity_id,
        "to": entity_b.entity_id
    }
    repository_setup.add_link(link)
    assert entity_a.links[0] == entity_b


def test_add_link_by_object(repository_setup, entities_setup):
    """test adding link by object"""
    entity_a, entity_b, _ = entities_setup
    repository_setup.add_entity(entity_a)
    repository_setup.add_entity(entity_b)
    link = Link(entity_a.entity_id, entity_b.entity_id)
    repository_setup.add_link(link)
    assert entity_a.links[0] == entity_b


def test_links(repository_setup, entities_setup):
    """test links"""
    entity_a, entity_b, entity_c = entities_setup
    repository_setup.add_entity(entity_a)
    repository_setup.add_entity(entity_b)
    repository_setup.add_entity(entity_c)

    repository_setup.add_link(Link(entity_a.entity_id, entity_b.entity_id))
    repository_setup.add_link(Link(entity_b.entity_id, entity_c.entity_id))
    repository_setup.add_link(Link(entity_c.entity_id, entity_a.entity_id))

    assert len(repository_setup.links) == 3


def test_load_file(repository_setup):
    """testing using fixtures file"""
    repository_setup.load_from_file(TEST_INPUT_FILE_NAME)
    assert len(repository_setup.entities) == 4
