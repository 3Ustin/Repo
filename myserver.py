from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
import re
import random
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "speak friend and enter"

@app.route('/')
def main():
    return render_template('main_menu.html')



#! ------------------------------------Register User---------------------------------------!#
# Registration
@app.route('/register')
def register():
    return render_template("registration.html")

@app.route('/register/processing', methods=['POST'])
def register_process():
    is_valid = True

    if len(request.form['username']) <2:
        is_valid = False
        flash("Username must be longer than 2 characters")
    if len(request.form['password']) <8:
        is_valid = False
        flash("password must be at least 8 characters")
    if len(request.form['password']) >15:
        is_valid = False
        flash("Must create a password")
    if request.form['password'] != request.form['confirm_password']:
        is_valid = False
        flash("passwords must match")
    if is_valid == True:
        query = "INSERT INTO users (username, password, created_at, updated_at) VALUES (%(username)s, %(password)s, NOW(), NOW());"
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "username": request.form['username'],
            "password": pw_hash
        }
        results = connectToMySQL('game').query_db(query,data)
        print(results)
        session['user_id'] = results
        return redirect('/login')
    return redirect("/game")

#!--------------------------------Login----------------------------------------------!#
@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login/processing', methods=['POST'])
def login_process():
    is_valid = True

    if len(request.form['username']) <2:
        is_valid = False
        flash("Username must be longer than 2 characters")
    if len(request.form['password']) <8:
        is_valid = False
        flash("password must be at least 8 characters")
    if is_valid == True:
        query = "SELECT * FROM users WHERE username = %(username)s"
        data = {
            "username": request.form['username']
        }
        results = connectToMySQL('game').query_db(query,data)
        if not results:
            flash("Invalid username/password")
            return redirect('/')
        if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
            flash("Invalid username/password")
            session['user_id'] = results[0]['id']
            return redirect('/welcome_page')
        return redirect('/login')

#!--------------------------------CREDITS----------------------------------------------!#
@app.route('/credits')
def credits():
    return render_template('credits.html')

#!--------------------------------GAME----------------------------------------------!#
@app.route('/game')
def game():
    return render_template('Game.html')

#!---------------------------------Welcome Page------------------------------------!#
@app.route('/welcome_page')
def welcome_page():
    return render_template("welcome_page.html")


#!---------------------------------Tavern------------------------------------!#
@app.route('/tavern')
def tavern():
    return render_template("tavern.html")

@app.route('/tavern/rest')
def tavern_rest():
    query = "SELECT * FROM paladin WHERE user_id = %(user_id)s"
    data = {
        "user_id": session['user_id']
    }
    results = connectToMySQL('game').query_db(query,data)
    print(results)
    results[0]['hp'] = 50
    query = "UPDATE paladin SET name = 'Paladin',attack = '10',defense = '10',hp = %(hp)s,sword = '0',shield = '0',armor = '0',created_at = NOW(),updated_at = NOW(),user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id'],
        "hp" : 40
    }
    results = connectToMySQL('game').query_db(query,data)
    return redirect("/tavern")


@app.route('/game/equipment_upgrade', methods=['POST'])
def game_equipment_upgrade():
    return redirect('game')

if __name__=="__main__":
    app.run(debug=True)