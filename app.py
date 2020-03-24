import mysql.connector
from flask import Flask, render_template, request

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
                                 user="pascal", 
                                 passwd="pascal")
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS question_5")

    cursor.execute("USE question_5")

    cursor.execute("CREATE TABLE IF NOT EXISTS users \
                   (prenom TEXT NOT NULL, \
                    nom TEXT NOT NULL, \
                    sexe CHAR NOT NULL, \
                    pseudo TEXT NOT NULL UNIQUE) \
                    ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    cursor.execute("INSERT IGNORE INTO users \
                    (prenom, nom, sexe, pseudo) \
                    VALUES (%s, %s, %s, %s)", (prenom1, nom1, sexe1, pseudo1))
    db.commit()
    db.close()

    # TODO
    # Possibilité de 2 Return(s) selon première vérification

    return render_template("page_4bis.html", \
                            titre=titre, \
                            prenom=prenom1, \
                            nom=nom1, \
                            pseudo=pseudo1)

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


@app.route("/page_7")
def page_7():
    return render_template("page_7.html")

@app.route("/page_8")
def page_8():
    return render_template("page_8.html")

if __name__ == "__main__":
    app.run(debug=True)
