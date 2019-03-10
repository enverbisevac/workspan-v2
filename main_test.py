""" Testing CLI arguments """

import sys
from utils import run
from workspan.settings import (
    MISSING_INPUT_FILE_NAME,
    MISSING_ENTITY_ID_MESSAGE
)

def test_missing_args():
    """test input cli"""
    code, _, err = run([sys.executable, 'main.py'])
    assert MISSING_INPUT_FILE_NAME == err
    assert code == 1

    code, _, err = run([sys.executable, 'main.py', 'test.json'])
    assert MISSING_ENTITY_ID_MESSAGE == err
    assert code == 2
