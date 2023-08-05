import json
import pytest
import os


DATA_DIR = f'{os.getcwd()}/tests'


@pytest.fixture
def mock_data(task, test):
    """
    Get the mock data for the test
    """
    file_path = f'{DATA_DIR}/{task}/{test}/mocks.json'
    mocks = []
    if os.path.exists(file_path):
        mocks = json.load(open(f'{DATA_DIR}/{task}/{test}/mocks.json', 'r'))
    return mocks


@pytest.fixture
def config():
    config = json.load(open(f'{DATA_DIR}/config.json'))
    return config


@pytest.fixture
def mock_requests(pytestconfig):
    return pytestconfig.getoption("mock")


def pytest_addoption(parser):
    parser.addoption("--mock",
                     help='Use mock requests defined in "mocks.json" for all default tests.',
                     action="store_true",
                     default=False)


