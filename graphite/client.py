#!/usr/bin/env python

import os, sys
# find the best StringIO implementation available on this platform
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import pycurl # http://pycurl.sourceforge.net/doc/index.html
import json

class GrafanaApiClient(object):
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.api_token = api_token
        self.last_request_time = None
        self.last_response_code = None
        
    def request(self, method, url, content = None, content_type = None):
        headers = []
        headers.append('Authorization: Bearer %s' % self.api_token)
        
        return self.raw_request(method, url, content, content_type, headers)
        
    def raw_request(self, method, url, content = None, content_type = None, headers = None):
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
        c.perform()

        # HTTP response code, e.g. 200.
        self.last_response_code = c.getinfo(c.RESPONSE_CODE)
        print('Status: %d' % self.last_response_code)
        
        # Elapsed time for the transfer.
        self.last_request_time = c.getinfo(c.TOTAL_TIME)
        print('Status: %f' % self.last_request_time)

        c.close()

        body = buffer.getvalue()
        # Body is a string in some encoding.
        # In Python 2, we can print it without knowing what the encoding is.
        return body

if __name__ == '__main__':
    g = GrafanaApiClient('http://172.16.33.30:3000/api', 'eyJrIjoiaXM3a0k4M2RaY3ZETG05cE9LczdubmdwNVpSM28wMkMiLCJuIjoiYWRtaW4iLCJpZCI6MX0=')
    output = g.request('GET', '/dashboards/db/my_dash')
    print output

    '''
    output = g.request('GET', 'http://172.16.33.30:3000/api/dashboards/db/my_dash')
    print output
    '''


