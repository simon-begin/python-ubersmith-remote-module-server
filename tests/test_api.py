import json
import unittest
from flask import Flask
from hamcrest import assert_that, is_
import mock
from pyubwebhook.api import WebhookApi


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask('test_app')
        self.api_client = self.app.test_client()
        self.router = mock.Mock()

        self.api = WebhookApi(self.app, self.router)

    def test_list_implemented_methods(self):
        self.router.list_implemented_methods.return_value = ['abcd', 'efgh']

        output = self.api_client.get('/module1/')
        self.router.list_implemented_methods.assert_called_with('module1')

        assert_that(json.loads(output.data.decode(output.charset)), is_({
            "implemented_methods": [
                "abcd",
                "efgh"
            ]
        }))

    def test_execute_method_returns_string(self):
        self.router.invoke_method.return_value = 'simple string'
        output = self.api_client.post('/module2/',
                                      headers={'Content-Type': 'application/json'},
                                      data=json.dumps(
            {
                "method": "remote_method",
                "params": [],
                "env": {
                    "variable1": "value1"
                },
                "callback": {}
            }
        ))

        self.router.invoke_method.assert_called_with(module_name='module2', method='remote_method', params=[], env={'variable1': 'value1'}, callback={})
        assert_that(json.loads(output.data.decode(output.charset)), is_('simple string'))

    def test_execute_method_returns_list(self):
        self.router.invoke_method.return_value = ['a', 'b', 'c']
        output = self.api_client.post('/module2/',
                                      headers={'Content-Type': 'application/json'},
                                      data=json.dumps(
            {
                "method": "remote_method",
                "params": [],
                "env": {
                    "variable1": "value1"
                },
                "callback": {}
            }
        ))

        self.router.invoke_method.assert_called_with(module_name='module2', method='remote_method', params=[], env={'variable1': 'value1'}, callback={})
        assert_that(json.loads(output.data.decode(output.charset)), is_(['a', 'b', 'c']))

