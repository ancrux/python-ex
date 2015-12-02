#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json
from curl import HttpClient

class GrafanaApiClient(HttpClient):            
    def __init__(self, api_token, base_url = None):
        super(GrafanaApiClient, self).__init__(base_url)
        self.api_token = api_token
        
    def request(self, method, url, content = None, content_type = None):
        headers = []
        headers.append('Authorization: Bearer %s' % self.api_token)
        
        return super(GrafanaApiClient, self).request(method, url, content, 'application/json', headers)

'''
Usage:
g = GrafanaApiClient('eyJrIjoiaXM3a0k4M2RaY3ZETG05cE9LczdubmdwNVpSM28wMkMiLCJuIjoiYWRtaW4iLCJpZCI6MX0=')
response = g.request('GET', 'http://172.16.33.30:3000/api/dashboards/db/my_dash') # full url

g = GrafanaApiClient('eyJrIjoiaXM3a0k4M2RaY3ZETG05cE9LczdubmdwNVpSM28wMkMiLCJuIjoiYWRtaW4iLCJpZCI6MX0=', 'http://172.16.33.30:3000/api')
response = g.request('GET', '/dashboards/db/my_dash') # path with base_url

Reference:
http://docs.grafana.org/reference/http_api/
'''
if __name__ == '__main__':
    g = GrafanaApiClient('eyJrIjoiaXM3a0k4M2RaY3ZETG05cE9LczdubmdwNVpSM28wMkMiLCJuIjoiYWRtaW4iLCJpZCI6MX0=', 'http://172.16.33.30:3000/api')
    
    # view dashboard
    r_body = g.request('GET', '/dashboards/db/my_dash')
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    
    # create datasource
    source = \
    {
        "name":"_graphite",
        "type":"graphite",
        "url":"http://172.16.33.30",
        "access":"proxy",
        "basicAuth":False,
    }
    q_body = json.dumps(source)

    r_body = g.request('POST', '/datasources', q_body)
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    
    # get datasource
    r_body = g.request('GET', '/datasources')
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    
    # create dashboard
    dashboard = \
    {
        "dashboard": {
            "id": None,
            "title": "my_dash",
            "tags": ["auto-generated"],
            "timezone": "browser",
            "editable": True,
            "hideControls": False,
            "rows": [
                {
                "collapse": False,
                "editable": True,
                "height": "250px",
                "panels": [],
                "title": "Row"
                }
            ],
            "schemaVersion": 1,
            "version": 0
        },
        "overwrite": True
    }
    q_body = json.dumps(dashboard)
    
    r_body = g.request('POST', '/dashboards/db', q_body)
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    


'''
clipboard
---------
eyJrIjoiMFBLZGNTT243OHA0V2g1QmFvT0hOSE42OEJtblJ1eHAiLCJuIjoiYWRtaW4iLCJpZCI6MX0=
'''

