"""Processor testing"""
import os
import shutil
import pytest


from workspan.tests.integration import (
    TEST_INPUT_FILE_NAME,
    TEST_INPUT_FILE_NAME_BACKUP
)
from workspan.formats import JSONFormat
from workspan.processors import FileFactoryProcessor
from workspan.entity import Entity


def test_file_processor_not_exists():
    """FileFactoryProcessor should raise exception bcs file not exists"""
    if os.path.exists(TEST_INPUT_FILE_NAME):
        os.remove(TEST_INPUT_FILE_NAME)
    # file not exists
    with pytest.raises(IOError):
        processor = FileFactoryProcessor(TEST_INPUT_FILE_NAME, '')
        items = processor.process()
        items.next()

    shutil.copy(TEST_INPUT_FILE_NAME_BACKUP, TEST_INPUT_FILE_NAME)


def test_file_factory_get_ext():
    """get extension"""
    factory = FileFactoryProcessor(TEST_INPUT_FILE_NAME, [""])
    assert factory.file_format == 'json'


def test_file_factory_formats():
    """check processor formats"""
    factory = FileFactoryProcessor(TEST_INPUT_FILE_NAME, [""])
    got = factory.formats
    expected = {
        'json': JSONFormat
    }
    assert expected == got


def test_file_factory_empty_format():
    """raise exception on empty format"""
    factory = FileFactoryProcessor(TEST_INPUT_FILE_NAME, [""])
    factory.formats = None

    with pytest.raises(Exception):
        factory.process()


def test_file_factory_process():
    """test processing method"""
    factory = FileFactoryProcessor(TEST_INPUT_FILE_NAME, ["entities.item"])
    _, entity = next(factory.process())
    got = Entity(**entity)
    expected = Entity(3, "EntityA")

    assert got == expected
