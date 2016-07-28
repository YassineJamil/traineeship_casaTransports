# -*- coding: utf-8 -*-
"""
"""

from matplotlib._png import read_png
import os
import psycopg2
from switch import Switch
from pylab import *
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
def monthstr_To_monthnbr(monthstr):
    with Switch(monthstr) as case:
        if case("janvier"):
            return "01"
        if case("fevrier"):
            return "02"
        if case("mars"):
            return "03"
        if case("avril"):
            return "04"
        if case("mai"):
            return "05"
        if case("juin"):
            return "06"
        if case("juillet"):
            return "07"
        if case("aout"):
            return "08"
        if case("septembre"):
            return "09"
        if case("octobre"):
            return "10"
        if case("novembre"):
            return "11"
        if case.default:
            return "12"

def monthnbr_To_monthstr(monthnbr):
    with Switch(monthnbr) as case:
        if case("01"):
            return "janvier"
        if case("02"):
            return "fevrier"
        if case("03"):
            return "mars"
        if case("04"):
            return "avril"
        if case("05"):
            return "mai"
        if case("06"):
            return "juin"
        if case("07"):
            return "juillet"
        if case("08"):
            return "aout"
        if case("09"):
            return "septembre"
        if case("10"):
            return "octobre"
        if case("11"):
            return "novembre"
        if case.default:
            return "decembre"

def eraseFile(repertoire):
    files=os.listdir(repertoire)
    for filename in files:
        os.remove(repertoire + "/" + filename)

@app.route('/')
def home():
    return render_template('home.html')

# la deconnexion et renvoi à la page d'acceuil
@app.route('/db_disconnect/')
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

@app.route('/db_action/', methods=['GET', 'POST'])
def db_action():
    if session.get('connexion'):
        if request.method == 'POST':
            with Switch(request.form['action']) as case:
                if case("tableinspectormonth"):
                    return redirect(url_for("tableinspectormonth"))
                if case("tableinspectoryear"):
                    return redirect(url_for("tableinspectoryear"))
                if case("test"):
                    return redirect(url_for("test"))
                if case.default:
                    return redirect(url_for('error'))
        else:
            return render_template('home.html')
    else:
        return redirect(url_for('error'))


@app.route('/tableinspectormonth/', methods=['GET', 'POST'])
def tableinspectormonth():
    if session.get('connexion'):
        if request.method == 'POST':
            conn = connect()
            cur1 = conn.cursor()
            cur2 = conn.cursor()
            date_nbr = request.form['mois']
            tab_date = date_nbr.split("-")
            month_nbr = tab_date[1]
            year = tab_date[0]
            month_str = monthnbr_To_monthstr(month_nbr)
            date_str = month_str + "_" + year
            cur1.execute(
                """SELECT table_name
                FROM INFORMATION_SCHEMA.TABLES
                WHERE table_name LIKE '"""+ date_str +"""';
                """
            )
            check = cur1.fetchall()
            if (check):
                cur1.execute(
                    """
                        drop table if exists somme_mois;
                        create table somme_mois (
                        datevalidation date,
                        sommenb1eremonteeentree int,
                        sommenb1eremonteesortie int,
                        sommenbcorrespentree int,
                        sommenbcorrespsortie int,
                        sommenbvalidationsentree int,
                        sommenbvalidationssortie int );

                        drop table if exists sommeentree;
                        create table sommeentree (
                        datevalidation date,
                        sommenb1eremonteeentree int,
                        sommenbcorrespentree int,
                        sommenbvalidationsentree int);
                        insert into sommeentree
                        SELECT datevalidation ,SUM(nb1eremontees),SUM(nbcorresp),SUM(nbvalidations)
                        FROM """ + date_str + """
                        where directionvalidation = 'entree'
                        GROUP BY datevalidation;

                        drop table if exists sommesortie;
                        create table sommesortie (
                        datevalidation date,
                        sommenb1eremonteesortie int,
                        sommenbcorrespsortie int,
                        sommenbvalidationssortie int);
                        insert into sommesortie
                        SELECT datevalidation ,SUM(nb1eremontees),SUM(nbcorresp),SUM(nbvalidations)
                        FROM """ + date_str + """
                        where directionvalidation = 'sortie'
                        GROUP BY datevalidation;

                        insert into somme_mois
                        SELECT sommeentree.datevalidation, sommenb1eremonteeentree,  sommenb1eremonteesortie, sommenbcorrespentree, sommenbcorrespsortie, sommenbvalidationsentree, sommenbvalidationssortie
                            FROM sommeentree, sommesortie
                            WHERE sommeentree.datevalidation = sommesortie.datevalidation;

                        -- ordonnement de somme create table sommebuffer (like somme);
                        drop table if exists sommebuffer;
                        create table sommebuffer (like somme_mois);
                        insert into sommebuffer
                        select * from somme_mois order by datevalidation;

                        delete from somme_mois;

                        insert into somme_mois
                        select * from sommebuffer;
                        drop table if exists sommebuffer;
                        drop table if exists sommesortie;
                        drop table if exists sommeentree;

                        """
                )
                cur2.execute(
                    """
                    SELECT * FROM somme_mois;
                    """
                )
                result = cur2.fetchall()
                tab_res = []
                for t in result:
                    tab_res.append([str(t[0]),t[1],t[2],t[3],t[4],t[5],t[6]])

                conn.commit()
                return render_template("tableinspectormonth_result.html", active="tableinspectormonth", res=tab_res)
            else:
                #la date n'est pas bonne
                return render_template("tableinspectormonth_error.html", active="tableinspectormonth")

        return render_template("tableinspectormonth.html", active="tableinspectormonth")
    else:
        return redirect(url_for('error'))

@app.route('/tableinspectoryear/', methods=['GET', 'POST'])
def tableinspectoryear():
    if session.get('connexion'):
        if request.method == 'POST':
            conn = connect()
            cur1 = conn.cursor()
            cur2 = conn.cursor()
            eraseFile('static/images')
            choix = request.form['choice']
            if (int(choix) == 0 or int(choix) == 1 ):
                annee_nbr = request.form['annee']
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%""" + str(annee_nbr) + """';
                    """
                )
                check = cur1.fetchall()
                if (check):
                    cur1.execute(
                        """
                            drop table if exists somme_annee;
                            create table somme_annee (
                            datevalidation CHAR(20),
                            sommenb1eremonteeentree int,
                            sommenb1eremonteesortie int,
                            sommenbcorrespentree int,
                            sommenbcorrespsortie int,
                            sommenbvalidationsentree int,
                            sommenbvalidationssortie int );
                        """
                    )

                    for date_str in check:
                        tab_date = str(date_str[0]).split("_")
                        month_str = tab_date[0]
                        year = tab_date[1]
                        month_nbr = monthstr_To_monthnbr(month_str)
                        date_nbr = year + '-' + month_nbr
                        cur1.execute(
                            # date validation chagement to date si ca marche c bien ...
                            # si non ... on verra pr le plot
                            """
                                DROP TABLE IF EXISTS les_mois;
                                CREATE TABLE les_mois(
                                datevalidation CHAR(20)
                                );
                                INSERT INTO les_mois
                                values('"""+ date_nbr +"""');
                                drop table if exists somme_mois;
                                create table somme_mois (
                                datevalidation date,
                                sommenb1eremonteeentree int,
                                sommenb1eremonteesortie int,
                                sommenbcorrespentree int,
                                sommenbcorrespsortie int,
                                sommenbvalidationsentree int,
                                sommenbvalidationssortie int );

                                drop table if exists sommeentree;
                                create table sommeentree (
                                datevalidation date,
                                sommenb1eremonteeentree int,
                                sommenbcorrespentree int,
                                sommenbvalidationsentree int);
                                insert into sommeentree
                                SELECT datevalidation ,SUM(nb1eremontees),SUM(nbcorresp),SUM(nbvalidations)
                                FROM """ + date_str[0] + """
                                where directionvalidation = 'entree'
                                GROUP BY datevalidation;

                                drop table if exists sommesortie;
                                create table sommesortie (
                                datevalidation date,
                                sommenb1eremonteesortie int,
                                sommenbcorrespsortie int,
                                sommenbvalidationssortie int);
                                insert into sommesortie
                                SELECT datevalidation ,SUM(nb1eremontees),SUM(nbcorresp),SUM(nbvalidations)
                                FROM """ + date_str[0] + """
                                where directionvalidation = 'sortie'
                                GROUP BY datevalidation;

                                insert into somme_mois
                                SELECT sommeentree.datevalidation, sommenb1eremonteeentree,  sommenb1eremonteesortie, sommenbcorrespentree, sommenbcorrespsortie, sommenbvalidationsentree, sommenbvalidationssortie
                                    FROM sommeentree, sommesortie
                                    WHERE sommeentree.datevalidation = sommesortie.datevalidation;

                                -- ordonnement de somme create table sommebuffer (like somme);
                                drop table if exists sommebuffer;
                                create table sommebuffer (like somme_mois);
                                insert into sommebuffer
                                select * from somme_mois order by datevalidation;

                                delete from somme_mois;

                                insert into somme_mois
                                select * from sommebuffer;
                                drop table if exists sommebuffer;
                                drop table if exists sommesortie;
                                drop table if exists sommeentree;
                                """
                        )

                        cur2.execute(
                            """
                            INSERT INTO somme_annee
                            SELECT les_mois.datevalidation,SUM(somme_mois.sommenb1eremonteeentree),SUM(somme_mois.sommenb1eremonteesortie),
                            SUM(somme_mois.sommenbcorrespentree), SUM(somme_mois.sommenbcorrespsortie),
                            SUM(somme_mois.sommenbvalidationsentree), SUM(somme_mois.sommenbvalidationssortie)
                            FROM les_mois, somme_mois
                            GROUP BY les_mois.datevalidation;
                            CREATE TABLE test (LIKE somme_annee);
                            INSERT INTO test
                            SELECT * FROM somme_annee ORDER BY datevalidation;
                            DROP TABLE somme_annee;
                            ALTER TABLE test RENAME TO somme_annee;
                            DROP TABLE IF EXISTS les_mois;
                            """
                        )





                    choix = request.form['choice']
                    if (int(choix) == 0):
                        cur2.execute(
                            """
                            SELECT * FROM somme_annee;
                            """
                        )
                        result = cur2.fetchall()
                        tab_res = []
                        for t in result:
                            tab_res.append([str(t[0]), t[1], t[2], t[3], t[4], t[5], t[6]])
                        return render_template("tableinspectoryear_result.html", active="tableinspectoryear", res=tab_res)
                    else :


                       #utiliser le os.path.exists(chemin) pr faire attendre le html ...
                        cur1.execute(
                            """
                            SELECT datevalidation FROM somme_annee;
                            """
                        )
                        tab_d_float = []
                        xdate = cur1.fetchall()
                        for x in xdate:
                            tab_d = x[0].split("-")
                            m_str = tab_d[1]
                            m_float = float(m_str)
                            tab_d_float.append(m_float)

                        cur2.execute(
                            """
                            SELECT sommenb1eremonteeentree FROM somme_annee;
                            """
                        )
                        figure()
                        yvalidation = cur2.fetchall()
                        plot(tab_d_float, yvalidation, label="premiere montee")
                        title("Graph de la premiere montee")
                        legend()
                        ylim(0, 4000000)
                        xlabel("Mois")
                        ylabel("Valeur 1ere montee")
                        numero = random()
                        path = 'static/images/graphic'+str(numero)+'.png'
                        savefig(path)
                        tpath = path.split('/', 1)
                        path1 = tpath[1]
                        return render_template("tableinspectoryear_result_graph.html", active="tableinspectoryear",res = path1)

                else:
                    #la date n'est pas bonne
                    return render_template("tableinspectoryear_error.html", active="tableinspectoryear")

            else :
                print 'graph global'

            conn.commit()
        return render_template("tableinspectoryear.html", active="tableinspectoryear")
    else:
        return redirect(url_for('error'))

# tous les renvois d'erreur
@app.route('/error/')
def error():
    return render_template("db_error.html")
# encoding key
a = os.urandom(24)
app.secret_key = a.encode('base-64')
# or app.secret_key = '7vNivdefmjkPOz3kUG7aaErD0Z2lPd1G'

#launch the application
if __name__ == '__main__':
    app.run(debug=True)