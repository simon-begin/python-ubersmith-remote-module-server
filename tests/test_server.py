import unittest
import mock
from pyubwebhook import server


class TestModule(object):
    def hello(self):
        return "world"

@mock.patch('pyubwebhook.server.Flask')
@mock.patch('pyubwebhook.server.router.Router')
@mock.patch('pyubwebhook.server.api.WebhookApi')
class ServerTest(unittest.TestCase):
    def test_starting_a_server(self, api_mock, router_mock, flask_mock):
        router_instance = router_mock.return_value
        flask_instance = flask_mock.return_value

        modules = {'test_module': TestModule()}
        s = server.Server(modules)
        s.run()

        router_mock.assert_called_with(modules)
        api_mock.assert_called_with(flask_instance, router_instance)
        flask_instance.run.assert_called_with()

    def test_run_passes_parameters_to_flask(self, api_mock, router_mock, flask_mock):
        flask_instance = flask_mock.return_value

        s = server.Server({})
        s.run('param1', 'param2', kwarg1='test')
        flask_instance.run.assert_called_with('param1', 'param2', kwarg1='test')
