.. image:: https://travis-ci.org/mat128/pyubwebhook.svg?branch=master
    :target: https://travis-ci.org/mat128/pyubwebhook

pyubwebhook
===========

Standardizing on the proposed ubersmith webhook format (method, params, env and callback),
this aims to be a wrapper for any python instance. This should allow any object to be a ubersmith webhook.


Mission
=======

Offer an easy way to write device, order and service modules, in python, with as few lines of code as possible.


Vision
======

A remote "hello world" device module should fit under 20 lines.


Values
======

* Everything should be tested and easy to understand.


Example
=======

>>> from pyubwebhook import server
>>> class MyDeviceModule(object):
...   def hello(self, env):
...     return "world"
...
>>> s = server.Server({'my_device_module': MyDeviceModule()})
>>> s.run()
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


TODOs
=====

* Callbacks (a.k.a. remote invocation of internal Ubersmith methods using the callback endpoint)
