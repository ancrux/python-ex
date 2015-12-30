# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import abort, redirect, url_for

import json

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
    
@app.route('/folder/') # works for both /folder/ and /folder (without tailing slash)
def folder():
    return 'folder()'
    
@app.route('/file') # works only for /file, but NOT for /file/ (404 Not Found)
def file():
    return 'file()'
    
# place files in static folder and flask will handle it automatically for you. e.g. /static/file

# place files in templates folder
@app.route('/hello')
def hello():
    return render_template('hello.html', name='angus')
    
@app.route('/request', methods=['GET', 'POST', 'PUT', 'DELETE'])
def req(): # avoid overriding global request object, do not use 'request' for function name
    resp = make_response("request_object=%s" % request.__dict__)
    resp.headers['Content-Type'] = 'text/plain'
    return resp

# customized error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

