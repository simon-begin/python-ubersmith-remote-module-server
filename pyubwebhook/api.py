import json
from flask import request, current_app


class WebhookApi(object):
    def __init__(self, app, router):
        self.app = app
        self.router = router

        app.add_url_rule('/<module_name>/', view_func=self.list_implemented_methods, methods=['GET'])
        app.add_url_rule('/<module_name>/', view_func=self.handle_remote_invocation, methods=['POST'])


    def list_implemented_methods(self, module_name):
        return json_response({
            'implemented_methods': self.router.list_implemented_methods(module_name)
        }, 200)

    def handle_remote_invocation(self, module_name):
        data = request.get_json()
        output = self.router.invoke_method(module_name=module_name, **data)
        return json_response(output, 200)

def json_response(data, code):
    json_data = json.dumps(data, indent=None)
    response = current_app.response_class(json_data, mimetype='application/json; charset=UTF-8')
    response.status_code = code

    return response