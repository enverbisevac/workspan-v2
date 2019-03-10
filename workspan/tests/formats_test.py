"""testing formats module"""
# pylint: disable=redefined-outer-name
import pytest
from pytest_mock import mocker  # pylint: disable=unused-import
from workspan.formats import JSONFormat


def test_json_format_no_prefixes():
    """raise exception when no prefixes"""
    processor = JSONFormat(None)
    with pytest.raises(Exception):
        items = processor.process()
        next(items)


def test_json_format_empty_file():
    """raise exception when file handle is empty"""
    processor = JSONFormat(None)
    processor.register_prefix("")
    with pytest.raises(IOError):
        items = processor.process()
        next(items)


def fake_yields(handle):  # pylint: disable=unused-argument
    """fake data for parsing"""
    yield "", JSONFormat.START_MAP, None
    yield "", JSONFormat.MAP_KEY, "id"
    yield "id", "", 1
    yield "", JSONFormat.END_MAP, None


def test_json_format_process(mocker):
    """mocking and testing process"""
    processor = JSONFormat('fake handle')
    processor.register_prefix("")
    mocker.patch('ijson.parse', fake_yields)
    mocker.patch.object(processor, "_file_handle")
    items = processor.process()
    prefix, item = next(items)
    assert prefix == ""
    assert item == {'id': 1}
