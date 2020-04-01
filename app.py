import csv
import mysql.connector
import os
import pandas as pd
import urllib.request

from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename


# Extensions de fichiers autorisés pour la question 7
extensions_fichiers = set(['csv', 'tsv'])


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/page_1")
def page_1():
    return "Question 1 >>> Hello World! <<< \
            (Page précédente pour revenir au menu)"

@app.route("/page_2")
def page_2():
    return render_template("page_2.html")

@app.route("/page_3")
def page_3():
    return render_template("page_3.html")

@app.route("/page_3bis")
def page_3bis():
    return render_template("page_3bis.html")

@app.route("/page_4", methods=['GET', 'POST'])
def page_4():
    return render_template("page_4.html")


@app.route("/page_4bis", methods=['GET', 'POST'])

def page_4bis():
    nom1    = request.form['nom'].title()
    prenom1 = request.form['prenom'].title()
    pseudo1 = request.form['pseudo']
    sexe1   = (request.form['sexe']).upper()
    
    if sexe1 == "M":
        titre = "Monsieur"
    else:
        titre = "Madame/Mademoiselle"

    db = mysql.connector.connect(host="localhost", 
                                 user="root", 
                                 passwd="root")
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS question_5")

    cursor.execute("USE question_5")

    cursor.execute("CREATE TABLE IF NOT EXISTS `users` \
                   (`prenom` VARCHAR(25) NOT NULL, \
                    `nom` VARCHAR(25) NOT NULL, \
                    `sexe` CHAR NOT NULL, \
                    `pseudo` VARCHAR(25) NOT NULL, \
                    UNIQUE KEY (`pseudo`)) \
                    ENGINE=InnoDB DEFAULT CHARSET=utf8;")
    
    try:
        cursor.execute("INSERT INTO users \
                      (prenom, nom, sexe, pseudo) \
                      VALUES (%s, %s, %s, %s)", \
                      (prenom1, nom1, sexe1, pseudo1))
        db.commit()
        db.close()
        
        return render_template("page_4bis.html", \
                            titre=titre, \
                            prenom=prenom1, \
                            nom=nom1, \
                            pseudo=pseudo1)            
    except:
        db.commit()
        db.close()

        return render_template("page_4bisbis.html", pseudo=pseudo1)
       
    
@app.route("/page_4bisbis")
def page_4bisbis():
    return render_template("page_4bisbis.html")    


@app.route("/page_5")
def page_5():

    # TODO
    # Préciser que la question est déjà résolu dans la question 4

    return render_template("page_5.html")

@app.route("/page_6")
def page_6():
    # Vérifier si la base existe ou non
    db = mysql.connector.connect(host="localhost", 
                                 user="pascal", 
                                 passwd="pascal")
    cursor = db.cursor()

    cursor.execute("SHOW DATABASES LIKE 'question_5'")

    result = cursor.fetchone()

    if result:
        # La table existe
        cursor.execute("USE question_5")
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        db.close()
        return render_template("page_6.html", data=data)

    else:
        # La table n'existe pas
        db.close()
        return render_template("page_6bis.html")


@app.route("/page_6bis")
def page_6bis():
    return render_template("page_6bis.html")


@app.route("/page_7", methods=['GET', 'POST'])
def page_7():
    return render_template("page_7.html")


@app.route("/page_7bis", methods=['GET', 'POST'])
def page_7bis():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('./temp', filename))
    
    filepath = os.path.join('./temp' + '/' + filename)
    
    common_delimeters = set(['\' \'', '\'\t\'', '\',\'', '\';\''])
    
    # TODO stocker le fichier en mémoire
    with open(filepath, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(2048))
        delimiter = repr(dialect.delimiter)
        
        if delimiter not in common_delimeters:
            return render_template("page_7bisbis.html")
        
        csvfile.seek(0)
        
        if csv.Sniffer().has_header(csvfile.read(2048)):
            data = pd.read_csv(filepath, sep=dialect.delimiter)
        else:
            data = pd.read_csv(filepath, sep=dialect.delimiter, header=None)
            
        df = data.describe()
        return render_template('page_7bis.html',  \
                                       tables=[df.to_html(classes='data')], \
                                           titles=df.columns.values)
            
    
@app.route("/page_7bisbis")
def page_7bisbis():
    return render_template("page_7bisbis.html")


@app.route("/page_8")
def page_8():
    return render_template("page_8.html")

if __name__ == "__main__":
    app.run(debug=True)
