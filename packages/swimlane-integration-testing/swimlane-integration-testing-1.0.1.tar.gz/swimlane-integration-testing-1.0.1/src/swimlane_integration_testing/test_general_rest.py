




"""
These tests work on any integrations using BasicRest classes
"""

import json
import pytest
from jsonschema import validate
from .output_verify import OUTPUT_MAP
import functools
from unittest.mock import patch
from requests import Session
import pickle
from deepdiff import DeepDiff
import os
import sys
import re
import importlib


# For shell execution
sys.path.append(os.getcwd())

# Globals
DATA_DIR = f'{os.getcwd()}/tests'
# Config Variables


def get_task_names():
    tasks = [x.replace('.py', '') for x in os.listdir(f'{os.getcwd()}/imports') if x.endswith('.py')]
    # asset is its own test
    if 'asset' in tasks:
        tasks.remove('asset')
    return tasks


def gather_test_dirs(task):
    tests = []
    if os.path.exists(os.path.join(DATA_DIR, task)):
        tests = [d for d in os.listdir(os.path.join(DATA_DIR, task)) if re.findall(r'test_.+', d)]
    return tests

def gather_tests():
    tests = []
    for task in get_task_names():
        for test in gather_test_dirs(task):
            tests.append((task, test))
    return tests


def build_mock(mock_definitions, auth_endpoints):

    def mock_handler(self, *args, **kwargs):
        comparable = {
            "args": list(args),
            "kwargs": kwargs
        }
        comparable['kwargs'].pop('headers', None)
        if auth_endpoints and any([endpoint in args[1] for endpoint in auth_endpoints]):
            comparable['kwargs'] = {}
        for request in mock_definitions:
            if DeepDiff(comparable, request['request']) == {}:
                return pickle.loads(bytes.fromhex(request["response"]))
        else:
            raise (Exception(f"No mock found for request args: {args}, kwargs: {kwargs}"))

    return mock_handler


def mock_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].mock_requests:
            with patch.object(Session, 'request', build_mock(args[0].mocks, args[0].config['auth_endpoints'])):
                return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


def sw_main(task, _inputs, _asset):
    mod = importlib.import_module(f'imports.{task}')
    if not _asset:
        _asset = json.loads(open(f'{DATA_DIR}/asset.json').read())

    class Context:
        asset = _asset
        inputs = _inputs
    ctx = mod.SwMain(Context)
    return ctx


@pytest.mark.parametrize("task, test", gather_tests())
class TestStandardRest:

    @pytest.fixture(autouse=True)
    def _set_ctx(self, task, test, mock_data, mock_requests, config):
        self.task = task
        self.test = test
        self.mocks = mock_data
        self.mock_requests = mock_requests
        self.config = config
        self.ctx = self.cls(task, test)

    @mock_session
    def cls(self, task, test):
        """Instantiate SwMain for general tests"""
        inputs = json.load(open(f'{DATA_DIR}/{task}/{test}/inputs.json')) if task != 'asset' else {}
        return sw_main(task, inputs, None)

    def test_kwargs(self, *args, **kwargs):
        """
        This will test the payload schema json, params, data, files, etc. As utils passes it.
        """
        schema = json.loads(open(f'{DATA_DIR}/{self.task}/schemas/payload.json').read())
        validate(
            instance=self.ctx.get_kwargs(),
            schema=schema
        )

    def test_session_headers(self, test, *args, **kwargs):
        """
        Verify session headers against schema
        """
        schema = json.loads(open(f'{DATA_DIR}/{self.task}/schemas/headers.json').read())
        validate(
            instance=self.ctx.session.headers,
            schema=schema
        )

    @mock_session
    def test_parse_response(self, *args, **kwargs):
        """
        Execute task and verify data to output manifest types.
        """
        resp = self.ctx.execute()
        assert self.validate_output_manifest(resp)
        assert DeepDiff(resp, json.load(open(f'{DATA_DIR}/{self.task}/{self.test}/output.json'))) == {}

    def validate_output_manifest(self, resp, *args, **kwargs):
        """
        Helper function:
        Loads the task manifest and compares task results to output type schema.
        """
        missing = []  # store missing outputs
        schema = json.loads(open(f'imports/{self.task}.json').read())['availableOutputVariables']
        if isinstance(resp, dict):
            resp = [resp]
        for record in resp:
            for k, v in record.items():
                _type = schema.get(k, {}).get('type')
                # Todo handle all of the types in output_verify.py and rewrite this POC.
                if _type in [1, 6, 5, 9]:
                    if not OUTPUT_MAP[_type](v):
                        raise TypeError(f'Output Key: {k}, Type: {_type}\nValue: {v}')
                else:
                    missing.append(k)

        return True
