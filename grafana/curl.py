#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl # http://pycurl.sourceforge.net/doc/index.html
# find the best StringIO implementation available on this platform
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

'''
A read-only class that obj.name = value or obj['key'] = value is not allowed.
set properties internally via obj.__dict__['key'] = value
'''
class ReadOnlyObject:
    def __setattr__(self, name, value):
        raise AttributeError('Read-only attribute')
    
    def __getitem__(self, key):
        return self.__dict__[key]

class HttpClient(object):            
    def __init__(self, base_url = None):
        self.base_url = base_url if base_url else ''
        self._clear_request()
        
    def _clear_request(self):
        # reset member vars
        self.last_request = ReadOnlyObject()
        self.last_response = ReadOnlyObject()
        
    def request(self, method, url, content = None, content_type = None, headers = None):
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
    c = HttpClient()
    r_body = c.request('GET', 'http://ancrux.com')

    c = HttpClient('http://ancrux.com')
    r_body = c.request('GET', '/')
'''
if __name__ == '__main__':
    c = HttpClient()
    r_body = c.request('GET', 'http://www.google.com')
    
    print('Response Code: %d' % c.last_response.code)
    print('Request Time: %f' % c.last_request.time)
    print r_body


