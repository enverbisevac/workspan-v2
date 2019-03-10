"""processor testing with exceptions"""
import pytest
from workspan.processors import FileFactoryProcessor

def test_filename_none():
    """wrong input"""
    # wrong file name
    with pytest.raises(Exception):
        FileFactoryProcessor(None, '')


def test_filename_empty_string():
    """wrong input"""
    # wrong file name
    with pytest.raises(Exception):
        FileFactoryProcessor('', '')
