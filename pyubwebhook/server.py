from flask import Flask

from pyubwebhook import api, router

class Server(object):
    def __init__(self, modules):
        self.router = router.Router(modules)
        self.app = Flask(__name__)
        self.api = api.WebhookApi(self.app, self.router)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)