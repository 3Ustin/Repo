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
    return render_template('registration.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

#! ------------------------------------Register User---------------------------------------!#
# Registration
@app.route('/register', methods=['POST'])
def process():
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
    return redirect("/")



#!--------------------------------Login----------------------------------------------!#
@app.route('/display_login')
def display_login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
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
            session['user_id'] = results[0]['id']
            return redirect('/')
        flash("Invalid username/password")
        return redirect('/')
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)