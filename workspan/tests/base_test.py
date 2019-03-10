"""base module tests"""
# pylint: disable=too-few-public-methods
import pytest
from workspan.base import BaseAsDict

class Person(BaseAsDict):
    """Example Person class for test"""
    __slots__ = ('pin', 'name', '_years')

    def __init__(self, pin, name, years):
        self.pin = pin
        self.name = name
        self._years = years

PERSON = Person(3, 'EntityA', 22)
EXPECTED_PERSON = {
    'pin': 3,
    'name': 'EntityA'
}

TEST_DICT_DATA = [
    (PERSON.as_dict(), EXPECTED_PERSON),
    (PERSON.as_dict(fields=['pin', 'name']), EXPECTED_PERSON),
    (PERSON.as_dict(fields=['pin', 'name', '_years']), EXPECTED_PERSON),
    (PERSON.as_dict(fields=['pin', 'name'], mappings={'pin': 'id'}), {
        'id': 3,
        'name': 'EntityA',
    })
]


@pytest.mark.parametrize('got,expected', TEST_DICT_DATA, ids=[
    'dict all fields', 'dict some fields', 'private fields', 'mappings'])
def test_as_dict(got, expected):
    """test converting object to dict"""
    assert got == expected
