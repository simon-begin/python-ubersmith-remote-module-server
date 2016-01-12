# Copyright 2015 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from hamcrest import is_, assert_that
import mock
from pyubwebhook.router import Router


class RouterTest(unittest.TestCase):
    def setUp(self):
        self.instance = mock.Mock()
        self.instance.my_method_name.return_value = 'yes'

        self.basic_router = Router(self.instance)
        self.router = Router(self.instance, env_as_kwarg=True)

    def test_basic_mode(self):
        payload = {'method': 'my_method_name',
                   'params': {'param1': 'value1', 'param2': 'value2'}}

        result = self.basic_router.route(payload)

        self.instance.my_method_name.assert_called_with(param1='value1', param2='value2')
        assert_that(result, is_('yes'))

    def test_env_is_optionally_passed_as_keyword_argument_in_every_call(self):
        payload = {'method': 'my_method_name',
                   'params': {'param1': 'value1', 'param2': 'value2'},
                   'env': {'local_variable1': 'value1', 'local_variable2': 'value2'}}

        result = self.router.route(payload)

        self.instance.my_method_name.assert_called_with(env={'local_variable1': 'value1', 'local_variable2': 'value2'},
                                                      param1='value1', param2='value2')
        assert_that(result, is_('yes'))
