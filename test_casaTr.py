# -*- coding: utf-8 -*-
"""
"""

import os
import psycopg2
from switch import Switch
import re
import time
import sys
import pprint

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect():
    return psycopg2.connect("dbname='"+ session['db_name'] +
                            "' user='"+ session['user'] +
                            "' host='" + session['host'] +
                            "' password='" + session['password'] + "'")

@app.route('/')
def home():
    return render_template('home.html')



# encoding key
a = os.urandom(24)
app.secret_key = a.encode('base-64')
# or app.secret_key = '7vNivdefmjkPOz3kUG7aaErD0Z2lPd1G'

#launch the application
if __name__ == '__main__':
    app.run()