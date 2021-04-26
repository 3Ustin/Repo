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
    return redirect("/register")

#!--------------------------------Login----------------------------------------------!#
@app.route('/login')
def login():
    return render_template("login.html")

#TRY CODE BREAKING HERE WHEN I HAVE TIME
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
            session['enemy_id'] = 0
            return redirect('/welcome_page')
        return redirect('/login')

#!--------------------------------CREDITS----------------------------------------------!#
@app.route('/credits')
def credits():
    return render_template('credits.html')

#!---------------------------------Welcome Page------------------------------------!#
@app.route('/welcome_page')
def welcome_page():
    return render_template("welcome_page.html")


#!---------------------------------Tavern------------------------------------!#
@app.route('/tavern')
def tavern():
    # TEST FOR COMBAT ENEMY INSERTION
    if session['enemy_id'] != 0:
        query = "DELETE from enemies WHERE id = %(id)s"
        data = {
            "id" : session['enemy_id'],
        }
        results = connectToMySQL('game').query_db(query,data)
        session['enemy_id'] = 0
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


#!----------------------------------Map--------------------------------------!#
@app.route('/map')
def map():
    return render_template("map2.html")


#!----------------------------- ----Combat------------------------------------!#
@app.route('/combat/start')
def combat_start():
    #Load image of enemy
    query = "INSERT INTO enemies(name, attack,defense,hp,created_at,updated_at) VALUE ('zombie', 10,10,5,40,NOW(),NOW());"
    data = {
        "enemy_id" : session['enemy_id']
    }
    enemy = connectToMySQL('game').query_db(query,data)
    session['enemy_id'] = 1
    return redirect('/combat')

@app.route('/combat')
def combat():
    return render_template("combat.html")

@app.route('/combat/attack0')
def combat_attack0():
    #does player hit?
        #The Player Always Hits.
    #Query to grab enemy object
    query = "SELECT * from enemies WHERE id = %(enemy_id)s;"
    data = {
        "enemy_id" : session['enemy_id'],
    }
    enemies = connectToMySQL('game').query_db(query,data)

    #Query to grab paladin object
    query = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id'],
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #Math for paladin basic attack
        #All Calculations of hitting and damage.
    new_enemyHP = int(enemies[0]['hp']) - int(paladin[0]['attack']) + int(enemies[0]['defense'])
    if new_enemyHP <= 0:
        return redirect(f"/combat/on_enemy_death/{session['enemy_id']}")
    #query for updating the enemy hp
    query = "UPDATE enemies SET hp = '%(new_enemyHP)s';"
    data = {
        'new_enemyHP' : int(new_enemyHP)
    }
    paladin = connectToMySQL('game').query_db(query,data)
    return redirect("/combat")

@app.route('/combat/on_enemy_death/<id>')
def combat_On_Enemy_Death(id):
    #query for killing an enemy  at too low of hp
    query = "DELETE from enemies WHERE id = %(id)s;"
    data = {
        'id' : id
    }
    connectToMySQL('game').query_db(query,data)
    return redirect('/combat')

@app.route('/combat/attack1')
def combat_attack1():
    return redirect("/combat")

@app.route('/combat/attack2')
def combat_attack2():
    return redirect("/combat")



if __name__=="__main__":
    app.run(debug=True)