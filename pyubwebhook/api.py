import json
from flask import request

class WebhookApi(object):
    def __init__(self, app, router):
        self.app = app
        self.router = router

        app.add_url_rule('/<module_name>/', view_func=self.list_implemented_methods, methods=['GET'])
        app.add_url_rule('/<module_name>/', view_func=self.handle_remote_invocation, methods=['POST'])


    def list_implemented_methods(self, module_name):
        return json.dumps({
            'implemented_methods': self.router.list_implemented_methods(module_name)
        })

    def handle_remote_invocation(self, module_name):
        data = json.loads(request.data)
        output = self.router.invoke_method(module_name=module_name, **data)
        return json.dumps(output)