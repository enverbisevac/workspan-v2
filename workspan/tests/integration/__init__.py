import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_INPUT_FILE_NAME = os.path.join(CURRENT_DIR, "./fixtures/test.json")
TEST_INPUT_FILE_NAME_BACKUP = os.path.join(CURRENT_DIR, "./fixtures/test.bak")
EXPECTED_RESULT_FILE_NAME = os.path.join(CURRENT_DIR, "./fixtures/expected.json")
