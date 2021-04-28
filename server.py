from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
import re
import random
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "speak friend and enter"

#THIS IS A EXAMPLE TEST FOR MERGING THROUGH TERMINAL

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


@app.route('/tavern/start')
def tavern_start():
    #DELETE any enemies from database
    query = "SELECT * FROM game.enemies;"
    enemies = connectToMySQL('game').query_db(query)
    for enemy in enemies:
        if enemy['user_id'] == session['user_id']:
            query = "DELETE from enemies WHERE id = %(id)s"
            data = {
                "id" : enemy['id']
            }
            results = connectToMySQL('game').query_db(query,data)


    #check the database for a paladin of that player
    query = "SELECT * FROM game.paladin;"
    paladins = connectToMySQL('game').query_db(query)
    paladin_made = False
    for paladin in paladins:
        if paladin['user_id'] == session['user_id']:
            paladin_made = True
    if  paladin_made == False:
        #make a paladin for the user;
        query = "INSERT INTO paladin (name, attack, defense, hp, sword, shield, armor, gold, created_at, updated_at, user_id) VALUES (%(name)s, %(attack)s, %(defense)s, %(hp)s, %(sword)s, %(shield)s, %(armor)s, %(gold)s, NOW(), NOW(), %(user_id)s);"
        print(query)
        data = {
            "name": "Paladin",
            "attack": 10,
            "defense": 5,
            "hp": 40,
            "sword": 0,
            "shield": 0,
            "armor": 0,
            "gold": 100,
            "user_id": session['user_id']
        }
        result = connectToMySQL('game').query_db(query,data)
        print(result)

    #put paladin id in session
    query_paladin = "SELECT * FROM paladin WHERE user_id = %(id)s;"
    data_paladin = {
        "id": session['user_id']
    }
    result_paladin = connectToMySQL('game').query_db(query_paladin, data_paladin)
    session['paladin_id'] = result_paladin[0]["id"]
    print(session['paladin_id'])

    #POTIONS FOR SHOP
    #red_potion
    query_red = "INSERT INTO items_shop (name, description, effect, gold, created_at, updated_at) VALUES (%(name)s, %(description)s, %(effect)s, %(gold)s, NOW(), NOW());"
    data_red = {
        "name": "red_potion.png",
        "description": "juicy red blood from the depths of the dragon's lair, rumored to have healing properties",
        "effect": "Gain 20 HP",
        "gold": 20 
    }
    result_1 = connectToMySQL('game').query_db(query_red, data_red)
    print(result_1)

    #yellow_potion
    query_yellow = "INSERT INTO items_shop (name, description, effect, gold, created_at, updated_at) VALUES (%(name)s, %(description)s, %(effect)s, %(gold)s, NOW(), NOW());"
    data_yellow = {
        "name": "yellow_potion.png",
        "description": "delicious syrupy nectar from the abyss of the nectar tree, rumored to increase your attack",
        "effect": "Gain 20 Attack",
        "gold": 35
    }
    result_2 = connectToMySQL('game').query_db(query_yellow, data_yellow)
    print(result_2)

    #green_potion
    query_green = "INSERT INTO items_shop (name, description, effect, gold, created_at, updated_at) VALUES (%(name)s, %(description)s, %(effect)s, %(gold)s, NOW(), NOW());"
    data_green = {
        "name": "green_potion.png",
        "description": "ooey gooey sticky green lather from the dragon's skin itself, rumored to increase the defense of whoever wears it",
        "effect": "Gain 20 Defense",
        "gold": 35
    }
    result_3 = connectToMySQL('game').query_db(query_green, data_green)
    print(result_3)
    return render_template('tavern.html')

@app.route('/tavern')
def tavern():
    #TJK code for inventory query
    query = "SELECT * FROM inventory WHERE paladin_id = %(paladin_id)s"
    data = {
        "paladin_id" : session['paladin_id']
    }
    result = connectToMySQL('game').query_db(query, data)

    return render_template("tavern.html", inventory = result)

@app.route('/purchase_item', methods=['POST'])
def purchase_item():
    if 'activities' not in session:
        session['activities'] = []

    query = "SELECT gold FROM paladin WHERE user_id = %(id)s;"
    data = {
        "id": session['user_id'],
    }
    print("***********************************")
    paladin_gold = connectToMySQL('game').query_db(query, data)[0]["gold"]
    print(paladin_gold)

    if request.form['option'] == 'red_potion':
        query_gold = "SELECT gold FROM items_shop WHERE name = %(name)s;"
        data_gold = {
            "name": 'red_potion.png'
        }
        potion_gold = connectToMySQL('game').query_db(query_gold, data_gold)[0]["gold"]
        if paladin_gold >= potion_gold:
            query = "INSERT INTO inventory (name, description, effect, created_at, updated_at, paladin_id) VALUES (%(name)s, %(description)s, %(effect)s, NOW(), NOW(), %(paladin_id)s);"
            data = {
                "name": "red potion.png",
                "description": "juicy red blood from the depths of the dragon's lair, rumored to have healing properties",
                "effect": "Gain 20 HP",
                "paladin_id": session['paladin_id']
            }
            result = connectToMySQL('game').query_db(query, data)
            print(result)
            query_update = "UPDATE paladin SET gold = %(new_gold)s WHERE id = %(id)s;"
            data_update = {
                "new_gold": paladin_gold - potion_gold,
                "id": session['paladin_id']
            }
            result_update = connectToMySQL('game').query_db(query_update, data_update)
            print(result_update)
            bought = ("Red potion purchased.")
            session['activities'].append(bought)
            print(session['activities'])
            return redirect ('/tavern')
        else: 
            flash("Not enough gold")

    print("******************************************************************")

    query = "SELECT gold FROM paladin WHERE user_id = %(id)s;"
    data = {
        "id": session['user_id'],
    }
    print("***********************************")
    paladin_gold = connectToMySQL('game').query_db(query, data)[0]["gold"]
    print(paladin_gold)

    if request.form['option'] == 'yellow_potion':
        query_gold = "SELECT gold FROM items_shop WHERE name = %(name)s;"
        data_gold = {
            "name": 'yellow_potion.png',
            "description": "delicious syrupy nectar from the abyss of the nectar tree, rumored to increase your attack",
            "effect": "Gain 20 Attack",
            "paladin_id": session['paladin_id']
        }
        potion_gold = connectToMySQL('game').query_db(query_gold, data_gold)[0]["gold"]
        if paladin_gold >= potion_gold:
            query = "INSERT INTO inventory (name, description, effect, created_at, updated_at, paladin_id) VALUES (%(name)s, %(description)s, %(effect)s, NOW(), NOW(), %(paladin_id)s);"
            data = {

                "paladin_id": session['paladin_id']
            }
            result = connectToMySQL('game').query_db(query, data)
            print(result)
            query_update = "UPDATE paladin SET gold = %(new_gold)s WHERE id = %(id)s;"
            data_update = {
                "new_gold": paladin_gold - potion_gold,
                "id": session['paladin_id']
            }
            result_update = connectToMySQL('game').query_db(query_update, data_update)
            print(result_update)
            bought_1 = "Yellow potion purchased."
            session['activities'].append(bought_1)
            print(session['activities'])
            return redirect ('/tavern')
        else:
            flash("Not enough gold")

    print("******************************************************************")

    query = "SELECT gold FROM paladin WHERE user_id = %(id)s;"
    data = {
        "id": session['user_id'],
    }
    print("***********************************")
    paladin_gold = connectToMySQL('game').query_db(query, data)[0]["gold"]
    print(paladin_gold)

    if request.form['option'] == 'green_potion':
        query_gold = "SELECT gold FROM items_shop WHERE name = %(name)s;"
        data_gold = {
            "name": 'green_potion.png',
            "description": "ooey gooey sticky green lather from the dragon's skin itself, rumored to increase the defense of whoever wears it",
            "effect": "Gain 20 Defense",
            "paladin_id": session['paladin_id']
        }
        potion_gold = connectToMySQL('game').query_db(query_gold, data_gold)[0]["gold"]
        if paladin_gold >= potion_gold:
            query = "INSERT INTO inventory (name, description, effect, created_at, updated_at, paladin_id) VALUES (%(name)s, %(description)s, %(effect)s, NOW(), NOW(), %(paladin_id)s);"
            data = {

                "paladin_id": session['paladin_id']
            }
            result = connectToMySQL('game').query_db(query, data)
            print(result)
            query_update = "UPDATE paladin SET gold = %(new_gold)s WHERE id = %(id)s;"
            data_update = {
                "new_gold": paladin_gold - potion_gold,
                "id": session['paladin_id']
            }
            result_update = connectToMySQL('game').query_db(query_update, data_update)
            print(result_update)
            bought_2 = "Green potion purchased."
            session['activities'].append(bought_2)
            print(session['activities'])
            return redirect ('/tavern')
        else: 
            flash("Not enough gold")
    return redirect('/tavern')

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
    if 'user_id' not in session:
        return redirect("/")
    return render_template("map.html")


#!----------------------------- ----Combat------------------------------------!#
@app.route('/combat/start')
def combat_start():
    #putting to session action feed.
    if 'action' not in session:
        session['action'] = []
    #Load image of enemy

    #INSERT Enemy into Database
    query = "INSERT INTO enemies(name, attack,defense,hp,created_at,updated_at,user_id) VALUE ('zombie', 10,5,40,NOW(),NOW(),%(id)s);"
    data = {
        "id" : session['user_id']
    }
    enemy = connectToMySQL('game').query_db(query,data)
    print(enemy)
    return redirect('/combat')

@app.route('/combat')
def combat():
    return render_template("combat.html")

@app.route('/combat/attack0', methods = ["POST"])
def combat_attack0():
    #does player hit?
        #The Player Always Hits.
    #Query to grab enemy object
    query = "SELECT * from enemies WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    enemies = connectToMySQL('game').query_db(query,data)

    #Query to grab paladin object
    query = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #Math for paladin basic attack
        #All Calculations of hitting and damage.
    new_enemyHP = int(enemies[0]['hp']) - int(paladin[0]['attack']) + int(enemies[0]['defense'])
    
    #NewStatus Effects for player

    #NewStatus Effects for enemy

    #if enemy dies.
    if new_enemyHP <= 0:
        return redirect(f"/combat/on_enemy_death")
    #query for updating the enemy hp
    query = "UPDATE enemies SET hp = '%(new_enemyHP)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_enemyHP" : int(new_enemyHP),
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #putting to activities
    session['action'] = []
    if 'action' not in session:
            session['action'] = []
    session['activities'].append("You dealt the Zombie 5 damage")

    return redirect("/combat/enemy_attack")

@app.route('/combat/attack1', methods = ['POST'])
def combat_attack1():
    #does player hit?
        #The Player Always Hits.
    #Query to grab enemy object
    query = "SELECT * from enemies WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    enemies = connectToMySQL('game').query_db(query,data)

    #Query to grab paladin object
    query = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #All Calculations of hitting and damage.
    new_enemyHP = int(enemies[0]['hp']) - int(paladin[0]['attack'] - 4) + int(enemies[0]['defense'])

    #NewStatus Effects for player
    if paladin[0]['hp'] + 5 >= 40:
        new_paladin_hp = 40
    else:
        new_paladin_hp = paladin[0]['hp'] + 5
    query = "UPDATE paladin SET hp = '%(new_paladin_hp)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_paladin_defense" : int(new_paladin_hp),
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #NewStatus Effects for enemy

    #if enemy dies.
    if new_enemyHP <= 0:
        return redirect(f"/combat/on_enemy_death")

    #query for updating the enemy hp
    query = "UPDATE enemies SET hp = '%(new_enemyHP)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_enemyHP" : int(new_enemyHP),
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #putting to activities
    session['action'] = []
    if 'action' not in session:
            session['action'] = []
    session['activities'].append("You dealt the Zombie 1 damage.")
    session['activities'].append("You healed 1 damage.")

    return redirect("/combat/enemy_attack")

@app.route('/combat/attack2', methods = ["POST"])
def combat_attack2():
    #does player hit?
        #The Player Always Hits.
    #Query to grab enemy object
    query = "SELECT * from enemies WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    enemies = connectToMySQL('game').query_db(query,data)

    #Query to grab paladin object
    query = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #All Calculations of hitting and damage.

    #NewStatus Effects for player
    new_paladin_defense = paladin[0]['defense'] + 1
    query = "UPDATE paladin SET defense = '%(new_paladin_defense)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_paladin_defense" : int(new_paladin_defense),
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #NewStatus Effects for enemy

    #if enemy dies.
    if enemies[0]['hp'] <= 0:
        return redirect(f"/combat/on_enemy_death")

    #query for updating the enemy hp

    #putting to activities
    session['action'] = []
    if 'action' not in session:
            session['action'] = []
    session['activities'].append("You gained 1 defense.")

    return redirect("/combat/enemy_attack")

@app.route('/combat/enemy_attack')
def combat_enemy_attack():
    #does player hit?
        #The Player Always Hits.
    #Query to grab enemy object
    query = "SELECT * from enemies WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    enemies = connectToMySQL('game').query_db(query,data)

    #Query to grab paladin object
    query = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #All Calculations of hitting and damage.
    if paladin[0]['hp'] - enemies[0]['attack'] + paladin[0]['defense'] <= 0:
        return redirect('/combat/player_death')
    else:
        new_paladin_hp = paladin[0]['hp'] - enemies[0]['attack'] + paladin[0]['defense'] 
    query = "UPDATE paladin SET hp = '%(new_paladin_hp)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_paladin_hp" : int(new_paladin_hp),
        "user_id" : session['user_id']
    }
    connectToMySQL('game').query_db(query,data)
    #NewStatus Effects for player

    #NewStatus Effects for enemy

    #if player dies.
    if paladin[0]['hp'] <= 0:
        return redirect(f"/combat/player_death")

    #query for updating the enemy hp

    #putting to activities
    if 'action' not in session:
        session['action'] = []
    session['activities'].append("Zombie hits you for 5.")

    return redirect('/combat')

@app.route('/combat/player_death')
def combat_on_player_death():
    return redirect('/death')

@app.route('/combat/on_enemy_death')
def combat_On_Enemy_Death():
    #query for killing an enemy at too low of hp
    query = "DELETE from enemies WHERE user_id = %(user_id)s;"
    data = {
        'user_id' : session['user_id']
    }
    session['action'] = []
    if 'action' not in session:
            session['action'] = []
    session['activities'].append("You killed the zombie!")
    session['activities'].append("Press advance to move forward!")
    #putting an enemy in after you kill them
    connectToMySQL('game').query_db(query,data)
    query = "INSERT INTO enemies(name, attack,defense,hp,created_at,updated_at,user_id) VALUE ('zombie', 10,5,5,NOW(),NOW(),%(id)s);"
    data = {
        "id" : session['user_id']
    }
    enemy = connectToMySQL('game').query_db(query,data)
    return redirect('/combat')

#!--------------------------------Logout--------------------------------!#
@app.route('/logout')
def logout():
    query = "DELETE from enemies WHERE user_id = %(user_id)s;"
    data = {
        'user_id' : session['user_id']
    }
    #THIS IS THE COMMENT FOR TEST
    connectToMySQL('game').query_db(query,data)
    session.clear()
    return redirect('/')

#!--------------------------------DEATH--------------------------------!#
@app.route('/death')
def death():
    query = "DELETE from enemies WHERE user_id = %(user_id)s;"
    data = {
        'user_id' : session['user_id']
    }
    #THIS IS THE COMMENT FOR TEST
    connectToMySQL('game').query_db(query,data)
    session.clear()
    return render_template('death.html')


if __name__=="__main__":
    app.run(debug=True)