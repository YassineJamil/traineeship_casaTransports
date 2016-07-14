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

# la deconnexion et renvoi à la page d'acceuil
@app.route('/db_disconnect')
def db_disconnect():
    session.clear()
    return redirect(url_for('home'))

#la connexion
@app.route('/db_connect/', methods=['GET', 'POST'])
def db_connect():
    if not session.get('connexion'):
        if request.method == 'POST':
            db_name = request.form['db_name']
            usr = request.form['usr']
            psw = request.form['psw']
            #Localhost is default
            if request.form['host'] == "":
                host = "localhost"
            else:
                host = request.form['host']

            try:
                conn = psycopg2.connect("dbname='"+db_name+"' user='"+usr+"' host='"+host+"' password='"+psw+"'")
                conn.close()

            except:
                return redirect(url_for('error'))

            #set session data
            session['db_name'] = db_name
            session['user'] = usr
            session['password'] = psw
            session['host'] = host
            session['connexion'] = True
            return redirect(url_for('home'))

    else:
        return redirect(url_for('db_action'))

    return render_template("db_connect.html")

@app.route('/db_action', methods=['GET', 'POST'])
def db_action():
    if session.get('connexion'):
        if request.method == 'POST':
            with Switch(request.form['action']) as case:
                if case("tableinspector"):
                    return redirect(url_for("tableinspector"))
                if case.default:
                    return redirect(url_for('error'))
        else:
            return render_template('home.html')
    else:
        return redirect(url_for('error'))


@app.route('/tableinspector', methods=['GET', 'POST'])
def tableinspector():
    if session.get('connexion'):
        if request.method == 'POST':
            annee = request.form['annee']
            print annee
            return render_template("tableinspector_result.html", active="tableinspector")
        return render_template("tableinspector.html", active="tableinspector")
    else:
        return redirect(url_for('error'))


# tous les renvois d'erreur
@app.route('/error')
def error():
    return render_template("db_error.html")
# encoding key
a = os.urandom(24)
app.secret_key = a.encode('base-64')
# or app.secret_key = '7vNivdefmjkPOz3kUG7aaErD0Z2lPd1G'

#launch the application
if __name__ == '__main__':
    app.run()