# Copyright 2016 Internap.
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

from flexmock import flexmock, flexmock_teardown

from ubersmith_remote_module_server import ubersmith_core
from ubersmith_remote_module_server.exceptions import NamedArgumentsOnly
from ubersmith_remote_module_server.ubersmith_core import NoRequestContext, UbersmithCore, \
    ConfiguredRequestContext


class UbersmithCoreTest(unittest.TestCase):
    def test_raises_when_out_of_context(self):
        remote_executor_mock = flexmock()
        flexmock(ubersmith_core).should_receive('RemoteExecutor').and_return(remote_executor_mock)
        with self.assertRaises(NoRequestContext):
            UbersmithCore.test()

    def test_raises_when_args(self):
        remote_executor_mock = flexmock()
        flexmock(ubersmith_core).should_receive('RemoteExecutor').and_return(remote_executor_mock)
        with self.assertRaises(NamedArgumentsOnly):
            UbersmithCore.test('hello')

    def test_calls_executor_with_context_when_called(self):
        remote_executor_mock = flexmock()
        flexmock(ubersmith_core).should_receive('RemoteExecutor').\
            with_args(context='context').and_return(remote_executor_mock).once()
        remote_executor_mock.should_receive('invoke_global').with_args('test', args={}).once()

        with ConfiguredRequestContext(context='context'):
            UbersmithCore.test()

    def tearDown(self):
        flexmock_teardown()
        super(UbersmithCoreTest, self).tearDown()
