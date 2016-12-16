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

from six import with_metaclass

from ubersmith_remote_module_server._remote_executor import RemoteExecutor
from ubersmith_remote_module_server.exceptions import NoRequestContext, NamedArgumentsOnly

_configuration = None


class ConfiguredRequestContext(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs or {}

    def __enter__(self):
        global _configuration
        _configuration = self.kwargs

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _configuration
        _configuration = None


class UbersmithCoreMeta(type):
    def _invoke_method(cls, name, *args, **kwargs):
        global _configuration
        if args:
            raise NamedArgumentsOnly()
        if _configuration is None:
            raise NoRequestContext()
        executor = RemoteExecutor(**_configuration)
        executor.invoke_global(name, args=kwargs)

    def __getattr__(cls, func_name):
        def invoke_without_name(*args, **kwargs):
            return cls._invoke_method(func_name, *args, **kwargs)
        return invoke_without_name


class UbersmithCore(with_metaclass(UbersmithCoreMeta, object)):
    __doc__ = """ This class is configured to wire the calls to ubersmith"""
