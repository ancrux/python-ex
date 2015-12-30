# -*- coding: utf-8 -*-
"""
Documentation:
http://falcon.readthedocs.org/

#pip install gunicorn

gunicorn app:api # app.py with api instance: app with default gunicorn settings (127.0.0.1:8000 with 1 worker)
# or
gunicorn -w 2 -b '0.0.0.0:8000' app:api # bind to all address with 2 workers
# useful options:
#  --reload: when code changes
#  -D daemon mode

# test with curl
curl localhost:8000/
"""

# Let's get this party started
import falcon

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class MyApp:
    def on_get(self, req, rsp):
        """Handles GET requests"""
        rsp.status = falcon.HTTP_200  # This is the default status
        rsp.body = (
            '\n'
            'Hello, World!\n'
            '\n'
            '==========================\n'
            'Falcon\n'
            )

class DefaultHandler:
    def __init__(self):
        pass
    
    def __call__(self, req, rsp):
        rsp.status = falcon.HTTP_404
        rsp.body = (
            '\n'
            'Ouch! "%s" not found\n'
            '\n'
            '==========================\n'
            'Falcon\n'
            ) % req.path
        pass
            
# falcon.API instances are callable WSGI apps
api = falcon.API()

# Resources are represented by long-lived class instances
myapp = MyApp()

# things will handle all requests to the '/things' URL path
api.add_route('/', myapp)

# anything not in the routing will fall thru in sink callback/handler
api.add_sink(DefaultHandler(), '/')

