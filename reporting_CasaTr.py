# coding: utf8
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


#création de l'application
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

def split_int(number, separator=' ', count=3):
    return separator.join(
        [str(number)[::-1][i:i+count] for i in range(0, len(str(number)), count)]
    )[::-1]

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
                if case('tableinspectormonth'):
                    return redirect(url_for('tableinspectormonth'))
                if case('tableinspectoryear'):
                    return redirect(url_for('tableinspectoryear'))
                if case('ssdmonth'):
                    return redirect(url_for('ssdmonth'))
                if case('ssdmonthstation'):
                    return redirect(url_for('ssdmonthstation'))
                if case.default:
                    return redirect(url_for('error'))
        else:
            return render_template('home.html')
    else:
        return redirect(url_for('error'))

# fonction station et branche SDD_station
@app.route('/ssdmonthstation/', methods=['GET', 'POST'])
def ssdmonthstation():
    if session.get('connexion'):
        if request.method == 'POST':
            conn = connect()
            cur1 = conn.cursor()
            cur2 = conn.cursor()
            cur3 = conn.cursor()
            choix = request.form['choice']
            if( choix == '0' or choix == '1'):
                date = request.form['jour']
                station = request.form['station']
                tab_date = date.split('-')
                y = tab_date[0]
                m = tab_date[1]
                j = tab_date[2]
                m_str = monthnbr_To_monthstr(m)
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%""" + m_str+'_'+y + """';
                    """
                )
                check = cur1.fetchall()
                if (check) :
                    if (choix == '0'):
                        cur1.execute(
                            """
                                SELECT jourvalidation, tranchehoraire, nb1eremontees
                                FROM """+ m_str+'_'+y+"""
                                WHERE libellearret = '"""+station+"""' AND jourvalidation = '"""+date+"""'
                                ORDER BY tranchehoraire;
                            """
                        )
                        result = cur1.fetchall()
                        tab_res = []
                        for t in result:
                            tab_res.append([str(t[0]), split_int(t[1]), split_int(t[2])])
                        return render_template('ssdmonthstation_result_jour.html', active='ssdmonthstation',
                                               res=tab_res , res2 = station)
                    else:
                        cur1.execute(
                            """
                                SELECT tranchehoraire
                                FROM """+ m_str+'_'+y+"""
                                WHERE libellearret = '"""+station+"""' AND jourvalidation = '"""+date+"""'
                                ORDER BY tranchehoraire;
                            """
                        )
                        x = cur1.fetchall()
                        cur1.execute(
                            """
                                SELECT nb1eremontees
                                FROM """+ m_str+'_'+y+"""
                                WHERE libellearret = '"""+station+"""' AND jourvalidation = '"""+date+"""'
                                ORDER BY tranchehoraire;
                            """
                        )
                        z = cur1.fetchall()
                        xticks(np.linspace(0, 23, 24, endpoint=True))
                        xlabel("Tranche Horaire")
                        ylabel("Validation")
                        title('Graphique journalier')
                        plot(x, z, "b-o", label=str(date))
                        legend()
                        grid()
                        show()
                        close()
                else:
                    # la date n'est pas bonne
                    return render_template('ssdmonthstation_error.html', active='ssdmonthstation')
            if (choix == '2' or choix == '3'):
                date = request.form['jour']
                branche = request.form['branche']
                with Switch(branche) as case:
                    if case('Branche tronc commun'):
                        list_station = ['Sidi Moumen', 'Ennasim', 'Mohamed Zef Zaf', 'Ctre Maintenance',
                                        u'Hôpital S Moumen', 'Attacharouk', 'Okba Ibn Nafii', 'Forces Aux', 'Ibn Tachfine',
                                        'Hay Raja', 'Ali Yaata', 'Achouada', 'Hay Mohammadi', 'Grande Ceinture', 'Ancien Abattoirs',
                                        'Bd Bahmad','Place Al Yassir', u'La Résistance', 'Mohamed Diouri', 'Pl Nations Unies',
                                        'Abdelmoumen', u'Marché Central', u'Fac. de Médecine', 'Casa Voyageurs', u'Les hôpitaux',
                                        'Bd Hassan II', 'Place Mohamed V']
                    if case('Branche ain diab'):
                        list_station = ['Sidi Abderrahman', u'Cité de l’air', 'Ghandi', 'Derb Ghellaf', 'Littoral',
                                        'Hay Hassani', u'Beauséjour', 'Riviera', 'Ain Diab Plage']
                    if case(u'Branche facultés'):
                        list_station = ['Mekka', 'Zenith', 'Panoramique', 'Gare Oasis', 'Bachkou', 'Technopark',
                                'Gare Casa Sud', u'Faculté Terminus']
                    if case.default:
                        return render_template('ssdmonthstation_error.html', active='ssdmonthstation')

                tab_date = date.split('-')
                y = tab_date[0]
                m = tab_date[1]
                j = tab_date[2]
                m_str = monthnbr_To_monthstr(m)
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%""" + m_str + '_' + y + """';
                    """
                )
                check = cur1.fetchall()
                if (check):
                    if (choix == '2'):
                        #creer une table ou je met le resultat voulu puis je l'affiche
                        cur2.execute(
                            """
                                DROP TABLE IF EXISTS buffer;
                                DROP TABLE IF EXISTS buffer2;
                                CREATE TABLE buffer
                                (
                                  jourvalidation date,
                                  tranchehoraire integer,
                                  nb1eremontees integer
                                );
                            """
                        )
                        for station in list_station:
                            cur1.execute(
                                """
                                    INSERT INTO buffer
                                    SELECT jourvalidation, tranchehoraire, nb1eremontees
                                    FROM """ + m_str + '_' + y + """
                                    WHERE libellearret = '""" + station + """' AND jourvalidation = '""" + date + """'
                                    ORDER BY tranchehoraire;
                                """
                            )
                        cur2.execute(
                            """
                                CREATE TABLE buffer2
                                (
                                  tranchehoraire integer,
                                  nb1eremontees integer
                                );
                            """
                        )
                        cur2.execute(
                            """
                                INSERT INTO buffer2
                                select distinct tranchehoraire, sum(nb1eremontees)
                                from buffer
                                group by tranchehoraire
                                order by tranchehoraire;
                            """
                        )
                        cur3.execute(
                            """
                                SELECT * FROM buffer2;
                            """
                        )
                        result = cur3.fetchall()
                        cur3.execute(
                            """
                                SELECT jourvalidation FROM buffer LIMIT 1;
                            """
                        )
                        date_res = cur3.fetchall()

                        cur3.execute(
                            """
                                DROP TABLE IF EXISTS buffer;
                                DROP TABLE IF EXISTS buffer2;
                            """
                        )
                        tab_res = []
                        for t in result:
                            tab_res.append([split_int(t[0]),  split_int(t[1])])
                        return render_template('ssdmonthbranche_result_jour.html', active='ssdmonthstation',
                                               res=tab_res, res2 = branche, res3 = str(date_res[0][0]))
                    else:
                        cur2.execute(
                            """
                                DROP TABLE IF EXISTS buffer;
                                DROP TABLE IF EXISTS buffer2;
                                CREATE TABLE buffer
                                (
                                  tranchehoraire integer,
                                  nb1eremontees integer
                                );
                            """
                        )
                        for station in list_station:
                            cur1.execute(
                                """
                                    INSERT INTO buffer
                                    SELECT tranchehoraire, nb1eremontees
                                    FROM """ + m_str + '_' + y + """
                                    WHERE libellearret = '""" + station + """' AND jourvalidation = '""" + date + """'
                                    ORDER BY tranchehoraire;
                                """
                            )
                        cur2.execute(
                            """
                                CREATE TABLE buffer2
                                (
                                  tranchehoraire integer,
                                  nb1eremontees integer
                                );
                            """
                        )
                        cur2.execute(
                            """
                                INSERT INTO buffer2
                                select distinct tranchehoraire, sum(nb1eremontees)
                                from buffer
                                group by tranchehoraire
                                order by tranchehoraire;
                            """
                        )

                        cur3.execute(
                            """
                                SELECT tranchehoraire from buffer2;
                            """
                        )
                        x = cur3.fetchall()
                        cur3.execute(
                            """
                            SELECT nb1eremontees from buffer2;
                            """
                        )
                        z = cur3.fetchall()
                        cur3.execute(
                            """
                              DROP TABLE IF EXISTS buffer;
                              DROP TABLE IF EXISTS buffer2;
                            """
                        )
                        xticks(np.linspace(0, 23, 24, endpoint=True))
                        xlabel("Tranche Horaire")
                        ylabel("Validation")
                        title('Graphique journalier')
                        plot(x, z, "b-o", label=str(date))
                        legend()
                        grid()
                        show()
                        close()
                else:
                    # la date n'est pas bonne
                    return render_template('ssdmonthstation_error.html', active='ssdmonthstation')
        return render_template('ssdmonthstation.html', active='ssdmonthstation')
    else:
        return redirect(url_for('error'))

#fonction par mois SDD_mois
@app.route('/ssdmonth/', methods=['GET', 'POST'])
def ssdmonth():
    if session.get('connexion'):
        if request.method == 'POST':
            conn = connect()
            cur1 = conn.cursor()
            cur2 = conn.cursor()
            cur3 = conn.cursor()
            choix = request.form['choice']
            if( choix == '4' or choix == '5'):
                date = request.form['jour']
                tab_date = date.split('-')
                y = tab_date[0]
                m = tab_date[1]
                j = tab_date[2]
                m_str = monthnbr_To_monthstr(m)
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%""" + m_str+'_'+y + """';
                    """
                )
                check = cur1.fetchall()
                if (check) :
                    if (choix == '4'):
                        cur1.execute(
                            """
                                SELECT * FROM """+ m_str+'_'+y+"""
                                WHERE jourvalidation = '"""+date+"""' order by tranchehoraire;
                            """
                        )
                        result = cur1.fetchall()
                        tab_res = []
                        for t in result:
                            tab_res.append([str(t[0]), split_int(t[1]), split_int(t[2])])
                        return render_template('ssdmonth_result_jour.html', active='ssdmonth', res=tab_res)
                    else:
                        cur1.execute(
                            """
                                SELECT tranchehoraire FROM """ + m_str + '_' + y + """
                                WHERE jourvalidation = '""" + date + """' order by tranchehoraire;
                            """
                        )
                        x = cur1.fetchall()
                        cur1.execute(
                            """
                                SELECT nb1eremontees FROM """ + m_str + '_' + y + """
                                WHERE jourvalidation = '""" + date + """' order by tranchehoraire;
                            """
                        )
                        z = cur1.fetchall()
                        xticks(np.linspace(0, 23, 24, endpoint=True))
                        xlabel("Tranche Horaire")
                        ylabel("Validation")
                        title('Graphique journalier')
                        plot(x, z, "b-o", label=str(date))
                        legend()
                        grid()
                        show()
                        close()
                else:
                    # la date n'est pas bonne
                    return render_template('ssdmonth_error.html', active='ssdmonth')
            elif( choix == '2' or choix == '3'):
                date = request.form['mois']
                tab_date = date.split('-')
                y = tab_date[0]
                m = tab_date[1]
                m_str = monthnbr_To_monthstr(m)
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%""" + m_str + '_' + y + """';
                        """
                )
                check = cur1.fetchall()
                if (check):
                    if (choix == '2'):
                        cur1.execute(
                            """
                              SELECT DISTINCT tranchehoraire, (SUM(nb1eremontees)/(SELECT COUNT(DISTINCT jourvalidation)
                              FROM """ + m_str + '_' + y + """))
                              FROM """ + m_str + '_' + y + """
                              GROUP BY tranchehoraire
                              ORDER BY tranchehoraire;
                            """
                        )

                        result = cur1.fetchall()
                        tab_res = []
                        for t in result:
                            tab_res.append([split_int(t[0]), split_int(t[1])])
                        return render_template('ssdmonth_result_moyenne.html', active='ssdmonth', res=tab_res,
                                               res2 = m_str + '_' + y)
                    else:
                        cur2.execute(
                            """
                                DROP TABLE IF EXISTS buffer2;
                                CREATE TABLE buffer2
                                (
                                  tranchehoraire integer,
                                  nb1eremontees integer
                                );
                            """
                        )
                        cur2.execute(
                            """
                                INSERT INTO buffer2
                                SELECT DISTINCT tranchehoraire, (SUM(nb1eremontees)/(SELECT COUNT(DISTINCT jourvalidation)
                                FROM """ + m_str + '_' + y + """))
                                FROM """ + m_str + '_' + y + """
                                GROUP BY tranchehoraire
                                ORDER BY tranchehoraire;
                            """
                        )
                        cur1.execute(
                            """
                                SELECT tranchehoraire FROM buffer2;
                            """
                        )
                        x = cur1.fetchall()
                        cur1.execute(
                            """
                                SELECT nb1eremontees FROM buffer2;
                            """
                        )
                        y = cur1.fetchall()
                        cur1.execute(
                            """
                                DROP TABLE IF EXISTS buffer2;
                            """
                        )
                        xticks(np.linspace(0, 23, 24, endpoint=True))
                        xlabel("Tranche Horaire")
                        ylabel("Validation")
                        title('Graphique moyenne mensuel')
                        plot(x, y, "b-o", label=str(date))
                        legend()
                        grid()
                        show()
                        close()
                else:
                    # la date n'est pas bonne
                    return render_template('ssdmonth_error.html', active='ssdmonth')
            else:
                date = request.form['mois']
                tab_date = date.split('-')
                y = tab_date[0]
                m = tab_date[1]
                m_str = monthnbr_To_monthstr(m)
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%""" + m_str + '_' + y + """';
                            """
                )
                check = cur1.fetchall()
                if (check):
                    if (choix == '0'):
                        cur1.execute(
                            """
                              SELECT DISTINCT tranchehoraire, SUM(nb1eremontees)
                              FROM """ + m_str + '_' + y + """
                              GROUP BY tranchehoraire
                              ORDER BY tranchehoraire;
                                """
                        )

                        result = cur1.fetchall()
                        tab_res = []
                        for t in result:
                            tab_res.append([split_int(t[0]), split_int(t[1])])
                        return render_template('ssdmonth_result_moyenne.html', active='ssdmonth', res=tab_res,
                                               res2=m_str + '_' + y)
                    else:
                        cur2.execute(
                            """
                                DROP TABLE IF EXISTS buffer2;
                                CREATE TABLE buffer2
                                (
                                  tranchehoraire integer,
                                  nb1eremontees integer
                                );
                            """
                        )
                        cur2.execute(
                            """
                                INSERT INTO buffer2
                                SELECT DISTINCT tranchehoraire, SUM(nb1eremontees)
                                FROM """ + m_str + '_' + y + """
                                GROUP BY tranchehoraire
                                ORDER BY tranchehoraire;
                                """
                        )
                        cur1.execute(
                            """
                                SELECT tranchehoraire FROM buffer2;
                            """
                        )
                        x = cur1.fetchall()
                        cur1.execute(
                            """
                                SELECT nb1eremontees FROM buffer2;
                            """
                        )
                        y = cur1.fetchall()
                        cur1.execute(
                            """
                                DROP TABLE IF EXISTS buffer2;
                            """
                        )
                        xticks(np.linspace(0, 23, 24, endpoint=True))
                        xlabel("Tranche Horaire")
                        ylabel("Validation")
                        title('Graphique mensuel')
                        plot(x, y, "b-o", label=str(date))
                        legend()
                        grid()
                        show()
                        close()
                else:
                    # la date n'est pas bonne
                    return render_template('ssdmonth_error.html', active='ssdmonth')

        return render_template('ssdmonth.html', active='ssdmonth')
    else:
        return redirect(url_for('error'))

#SDC mois
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
                    tab_res.append([str(t[0]), split_int(t[1]), split_int(t[2]), split_int(t[3]), split_int(t[4]),
                                    split_int(t[5]), split_int(t[6])])

                conn.commit()
                return render_template("tableinspectormonth_result.html", active="tableinspectormonth", res=tab_res)
            else:
                #la date n'est pas bonne
                return render_template("tableinspectormonth_error.html", active="tableinspectormonth")

        return render_template("tableinspectormonth.html", active="tableinspectormonth")
    else:
        return redirect(url_for('error'))

#SDC annee
@app.route('/tableinspectoryear/', methods=['GET', 'POST'])
def tableinspectoryear():
    if session.get('connexion'):
        if request.method == 'POST':
            conn = connect()
            cur1 = conn.cursor()
            cur2 = conn.cursor()
            cur3 = conn.cursor()
            eraseFile('static/images')
            choix = request.form['choice']
            if (int(choix) == 0 or int(choix) == 1 ):
                annee_nbr = request.form['annee']
                cur1.execute(
                    """SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE table_name LIKE '%\_""" + str(annee_nbr) + """';
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
                            DROP TABLE IF EXISTS somme_mois;
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
                            tab_res.append([str(t[0]), split_int(t[1]), split_int(t[2]), split_int(t[3]), split_int(t[4]),
                                            split_int(t[5]), split_int(t[6])])
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
                            m_int = int(m_str)
                            tab_d_float.append(m_int)

                        cur2.execute(
                            """
                            SELECT sommenb1eremonteeentree FROM somme_annee;
                            """
                        )
                        figure()
                        yvalidation = cur2.fetchall()
                        xticks(np.linspace(1, 12, 12, endpoint=True))
                        plot(tab_d_float, yvalidation, "c--o", label=str(annee_nbr))
                        legend()
                        title("Evolution de validation mensuelle")
                        xlabel("Mois")
                        ylabel("Validation")
                        numero = random()
                        path = 'static/images/graphic'+str(numero)+'.png'
                        grid()
                        savefig(path)
                        tpath = path.split('/', 1)
                        path1 = tpath[1]
                        close()
                        return render_template("tableinspectoryear_result_graph.html", active="tableinspectoryear",res = path1)
                else:
                    #la date n'est pas bonne
                    return render_template("tableinspectoryear_error.html", active="tableinspectoryear")

            else :
                tab_res = []
                lesDates = []
                cur1.execute(
                    """
                        SELECT table_name
                        FROM INFORMATION_SCHEMA.TABLES
                        WHERE table_name LIKE '%\_20%';
                    """
                )
                liste = cur1.fetchall()
                for l in liste:
                    tab_list = l[0].split('_')
                    year_str = tab_list[1]
                    year_nbr = int(year_str)
                    if year_nbr not in lesDates:
                        lesDates.append(year_nbr)
                i = 0
                for annee_nbr in lesDates:
                    cur1.execute(
                        """SELECT table_name
                        FROM INFORMATION_SCHEMA.TABLES
                        WHERE table_name LIKE '%\_""" + str(annee_nbr) + """';
                        """
                    )
                    check = cur1.fetchall()
                    if (check):
                        cur1.execute(
                            """
                                drop table if exists somme_annee"""+str(annee_nbr)+""";
                                create table somme_annee"""+str(annee_nbr)+""" (
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
                            month_nbr = monthstr_To_monthnbr(month_str)
                            date_nbr = month_nbr
                            cur1.execute(
                                """
                                    DROP TABLE IF EXISTS les_mois"""+str(annee_nbr)+""";
                                    CREATE TABLE les_mois"""+str(annee_nbr)+"""(
                                    datevalidation CHAR(20)
                                    );
                                    INSERT INTO les_mois"""+str(annee_nbr)+"""
                                    values('""" + date_nbr + """');
                                    drop table if exists somme_mois"""+str(annee_nbr)+""";
                                    create table somme_mois"""+str(annee_nbr)+""" (
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
                                    FROM """ + str(date_str[0]) + """
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
                                    FROM """ + str(date_str[0]) + """
                                    where directionvalidation = 'sortie'
                                    GROUP BY datevalidation;

                                    insert into somme_mois"""+str(annee_nbr)+"""
                                    SELECT sommeentree.datevalidation, sommenb1eremonteeentree,  sommenb1eremonteesortie, sommenbcorrespentree, sommenbcorrespsortie, sommenbvalidationsentree, sommenbvalidationssortie
                                        FROM sommeentree, sommesortie
                                        WHERE sommeentree.datevalidation = sommesortie.datevalidation;

                                    -- ordonnement de somme create table sommebuffer (like somme);
                                    drop table if exists sommebuffer;
                                    create table sommebuffer (like somme_mois"""+str(annee_nbr)+""");
                                    insert into sommebuffer
                                    select * from somme_mois"""+str(annee_nbr)+""" order by datevalidation;

                                    delete from somme_mois"""+str(annee_nbr)+""";

                                    insert into somme_mois"""+str(annee_nbr)+"""
                                    select * from sommebuffer;
                                    drop table if exists sommebuffer;
                                    drop table if exists sommesortie;
                                    drop table if exists sommeentree;
                                """
                            )
                            cur2.execute(
                                """
                                INSERT INTO somme_annee"""+str(annee_nbr)+"""
                                SELECT les_mois"""+str(annee_nbr)+""".datevalidation,SUM(somme_mois"""+str(annee_nbr)+""".sommenb1eremonteeentree),SUM(somme_mois"""+str(annee_nbr)+""".sommenb1eremonteesortie),
                                SUM(somme_mois"""+str(annee_nbr)+""".sommenbcorrespentree), SUM(somme_mois"""+str(annee_nbr)+""".sommenbcorrespsortie),
                                SUM(somme_mois"""+str(annee_nbr)+""".sommenbvalidationsentree), SUM(somme_mois"""+str(annee_nbr)+""".sommenbvalidationssortie)
                                FROM les_mois"""+str(annee_nbr)+""", somme_mois"""+str(annee_nbr)+"""
                                GROUP BY les_mois"""+str(annee_nbr)+""".datevalidation;
                                CREATE TABLE test (LIKE somme_annee"""+str(annee_nbr)+""");
                                INSERT INTO test
                                SELECT * FROM somme_annee"""+str(annee_nbr)+""" ORDER BY datevalidation;
                                DROP TABLE somme_annee"""+str(annee_nbr)+""";
                                ALTER TABLE test RENAME TO somme_annee"""+str(annee_nbr)+""";
                                DROP TABLE IF EXISTS les_mois"""+str(annee_nbr)+""";
                                DROP TABLE if EXiSTS somme_mois"""+str(annee_nbr)+""";
                                """
                            )
                choix = request.form['choice']
                if (int(choix) == 3):
                    for tdate in lesDates:
                        cur3.execute(
                            """
                            SELECT * FROM somme_annee"""+str(tdate)+""";
                            """
                        )
                        result = cur3.fetchall()
                        print result
                        print '------------------'
                        tab_res.append([str(tdate)])
                        for t in result:
                            tab_res.append([str(t[0]), split_int(t[1]), split_int(t[2]), split_int(t[3]), split_int(t[4]),
                                            split_int(t[5]), split_int(t[6])])
                            print t
                    return render_template("tableinspectoryear_result.html", active="tableinspectoryear", res=tab_res)
                else:
                    # les types sont : - -- : -.
                    # couleur b g r c m y b w
                    list_option = ["y--o", "g--o", "m--o", "c--o", "b--o", "r--o", "y-o", "g-o", "m-o", "c-o", "b-o", "r-o"]
                    for tdate in lesDates:
                        option = choice(list_option)
                        list_option.remove(option)
                        cur1.execute(
                            """
                            SELECT datevalidation FROM somme_annee"""+str(tdate)+""";
                            """
                        )
                        tab_d_int = []
                        xdate = cur1.fetchall()
                        for x in xdate:
                            m_str = x[0]
                            m_float = int(m_str)
                            tab_d_int.append(m_float)

                        cur2.execute(
                            """
                            SELECT sommenb1eremonteeentree FROM somme_annee"""+str(tdate)+""";
                            """
                        )
                        yvalidation = cur2.fetchall()
                        plot(tab_d_int, yvalidation, option, label= str(tdate))
                        legend()
                        title("Synthese validation annuelle")
                        xticks(np.linspace(1, 12,12, endpoint=True))
                        xlabel("Mois")
                        ylabel("Validation")
                    grid()
                    show()
                    close()
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