#!/usr/bin/env python

import os, sys
# find the best StringIO implementation available on this platform
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import pycurl # http://pycurl.sourceforge.net/doc/index.html
import json

'''
A read-only class that obj.name = value or obj['key'] = value is not allowed.
set properties internally via obj.__dict__['key'] = value
'''
class ReadOnlyObject:
    def __setattr__(self, name, value):
        raise AttributeError('Read-only attribute')
    
    def __getitem__(self, key):
        return self.__dict__[key]

class GrafanaApiClient(object):            
    def __init__(self, api_token, base_url = None):
        self.api_token = api_token
        self.base_url = base_url if base_url else ''
        self._clear_request()
        
    def _clear_request(self):
        # reset member vars
        self.last_request = ReadOnlyObject()
        self.last_response = ReadOnlyObject()
        
    def request(self, method, url, content = None, content_type = None):
        headers = []
        headers.append('Authorization: Bearer %s' % self.api_token)
        
        return self._request(method, url, content, 'application/json', headers)
        
    def _request(self, method, url, content = None, content_type = None, headers = None):
        self._clear_request()
    
        # make sure headers is a list
        if not isinstance(headers, list):
            headers = []
        
        # append content_type to headers
        if isinstance(content_type, basestring):
            headers.append('Content-Type: %s' % content_type)
        
        # if url starts with '/', url will be prefixed with base_url
        if url[:1] == '/':
            url = self.base_url + url
        
        c = pycurl.Curl()
        
        # apply headers
        if len(headers):
            c.setopt(c.HTTPHEADER, headers)
        # apply content body
        if content:
            c.setopt(c.POSTFIELDS, content)
        c.setopt(c.CUSTOMREQUEST, method.upper())
        c.setopt(c.URL, url)
        buffer = StringIO()
        c.setopt(c.WRITEFUNCTION, buffer.write)
        
        # make request
        c.perform()

        # HTTP response code, e.g. 200.
        self.last_response.__dict__['code'] = c.getinfo(c.RESPONSE_CODE)
        
        # Elapsed time for the transfer.
        self.last_request.__dict__['time'] = c.getinfo(c.TOTAL_TIME)

        c.close()

        body = buffer.getvalue()
        # Body is a string in some encoding.
        # In Python 2, we can print it without knowing what the encoding is.
        return body

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
    
    r_body = g.request('GET', '/dashboards/db/my_dash')
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    
    source = {
        "name":"my_graphite",
        "type":"graphite",
        "url":"http://172.16.33.30",
        "access":"proxy",
        "basicAuth":False
    }
    q_body = json.dumps(source)

    r_body = g.request('POST', '/datasources', q_body)
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    
    r_body = g.request('GET', '/datasources')
    print('Response Code: %d' % g.last_response.code)
    print('Request Time: %f' % g.last_request.time)
    print r_body
    


'''
{
  "name":"test_datasource",
  "type":"graphite",
  "url":"http://mydatasource.com",
  "access":"proxy",
  "basicAuth":false
}
'''

