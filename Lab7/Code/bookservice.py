#!/usr/bin/env python

import library
from bottle import Bottle, run, debug
import json

app = Bottle()
bd = library.library("mylib")

 
	
@app.route('/')
def authors():
	return "Welcome to the book <b>library</b>"

if __name__=="__main__":
	debug()
	run(app, host='localhost', port=8080, reloader=True)
