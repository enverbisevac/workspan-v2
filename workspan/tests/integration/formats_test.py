"""integration testing of formats"""
import cStringIO
import json
import pytest
from ijson.backends.python import UnexpectedSymbol
from workspan.formats import JSONFormat


def test_json_format_process():
    """test json format"""
    obj = {
        'entity_id': 1,
        'name': 'Entity'
    }
    output = cStringIO.StringIO(json.dumps(obj))
    processor = JSONFormat(output)
    processor.register_prefix("")
    items = processor.process()
    _, entity = next(items)
    assert entity == obj
    output.close()


def test_json_incorrect_structure():
    """raise exception while incorrect structure"""
    content = '{\"entity_id\': 1, \"name\": \"Entity\"}'
    output = cStringIO.StringIO(content)
    processor = JSONFormat(output)
    processor.register_prefix("")
    with pytest.raises(UnexpectedSymbol):
        next(processor.process())
    output.close()
