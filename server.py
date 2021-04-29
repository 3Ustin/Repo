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
    if len(request.form['password']) >25:
        is_valid = False
        flash("Password may not exceed 25 characters")
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

    #Reset actions in session.
    # if session['actions']:
    #     session['actions'] = []
    # #Reset activities in session.
    # if session['activities']:
    #     session['activities'] = []

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

    #put paladin id in session
    query_paladin = "SELECT * FROM paladin WHERE user_id = %(id)s;"
    data_paladin = {
        "id": session['user_id']
    }
    result_paladin = connectToMySQL('game').query_db(query_paladin, data_paladin)
    session['paladin_id'] = result_paladin[0]["id"]

    #DELETING THE potions
    query_paladin = "DELETE from items_shop;"
    data_paladin = {
        "id": session['user_id']
    }
    result_paladin = connectToMySQL('game').query_db(query_paladin, data_paladin)

    #POTIONS FOR SHOP
    #red_potion
    query_red = "INSERT INTO items_shop (name, description, effect, gold, created_at, updated_at) VALUES (%(name)s, %(description)s, %(effect)s, %(gold)s, NOW(), NOW());"
    data_red = {
        "name": "red_potion.png",
        "description": "juicy red blood from the depths of the dragon's lair, rumored to have healing properties",
        "effect": 20,
        "gold": 20 
    }
    result_1 = connectToMySQL('game').query_db(query_red, data_red)

    #yellow_potion
    query_yellow = "INSERT INTO items_shop (name, description, effect, gold, created_at, updated_at) VALUES (%(name)s, %(description)s, %(effect)s, %(gold)s, NOW(), NOW());"
    data_yellow = {
        "name": "yellow_potion.png",
        "description": "delicious syrupy nectar from the abyss of the nectar tree, rumored to increase your attack",
        "effect": 1,
        "gold": 80
    }
    result_2 = connectToMySQL('game').query_db(query_yellow, data_yellow)

    #green_potion
    query_green = "INSERT INTO items_shop (name, description, effect, gold, created_at, updated_at) VALUES (%(name)s, %(description)s, %(effect)s, %(gold)s, NOW(), NOW());"
    data_green = {
        "name": "green_potion.png",
        "description": "ooey gooey sticky green lather from the dragon's skin itself, rumored to increase the defense of whoever wears it",
        "effect": 1,
        "gold": 50
    }
    result_3 = connectToMySQL('game').query_db(query_green, data_green)

    #init activities
    if 'activities' not in session:
        session['activities'] = []
        session['activities'].append("Welcome to the inn brave adventurer! Feel free to take a rest and restore your strength here. If you wish to stock up on items, visit the shop and browse our wares. Once you are finished, check the world map to continue on to your next destination.")

    return redirect ('/tavern')

@app.route('/tavern')
def tavern():
    query = "UPDATE paladin SET attack = '10', defense = '5' WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)
    #print activities

    #QUERY PALADIN'S INVENTORY
    query = "SELECT * FROM inventory WHERE paladin_id = %(paladin_id)s"
    data = {
        "paladin_id" : session['paladin_id']
    }
    result = connectToMySQL('game').query_db(query, data)

    #DISPLAY PALADINS GOLD
    query = "SELECT gold FROM paladin WHERE id = %(paladin_id)s;"
    data = {
        "paladin_id": session['paladin_id']
    }
    #set paladin gold
    paladin_gold = connectToMySQL('game').query_db(query, data)[0]["gold"]
    print("paladin_gold in tavern: ",paladin_gold)

    #QUERY player attack
    query_attack = "SELECT attack FROM paladin WHERE id = %(id)s;"
    data_attack = {
        "id": session['paladin_id']
    }
    attack_stats = connectToMySQL('game').query_db(query_attack, data_attack)[0]["attack"]

    #QUERY player defense
    query_defense = "SELECT defense FROM paladin WHERE id = %(id)s;"
    data_defense = {
        "id": session['paladin_id']
    }
    defense_stats = connectToMySQL('game').query_db(query_defense, data_defense)[0]["defense"]

    return render_template("tavern.html", inventory = result, paladin_gold = paladin_gold, player_attack = attack_stats, player_defense = defense_stats)

@app.route('/purchase_item', methods=['POST'])
def purchase_item():
#CHECK PALADINS GOLD
    #query the database
    query = "SELECT gold FROM paladin WHERE id = %(id)s;"
    data = {
        "id": session['paladin_id']
    }
    #set paladin gold
    paladin_gold = connectToMySQL('game').query_db(query, data)[0]["gold"]
    print("paladin_gold in purchase item: ",paladin_gold)
# CHECK HOW MANY ITEMS IN INVENTORY
    # set max items at 4
    query = "SELECT * FROM inventory WHERE paladin_id = %(id)s;"
    data = {
        "id": session['paladin_id']
    }
    result = connectToMySQL('game').query_db(query, data)
    if len(result) >= 4:
        session['activities'].append("Your backpack is too heavy to carry more items.")
        return redirect('/tavern')
#/RED POTION/
    #check form for potion id
    if request.form['option'] == 'red_potion':
        query_gold = "SELECT gold FROM items_shop WHERE name = %(name)s;"
        data_gold = {
            "name": 'red_potion.png'
        }
        #set potion gold
        potion_gold = connectToMySQL('game').query_db(query_gold, data_gold)[0]["gold"]
        
        #if they have enough gold -> purchase
        if paladin_gold >= potion_gold:
            query = "INSERT INTO inventory (name, description, effect, created_at, updated_at, paladin_id) VALUES (%(name)s, %(description)s, %(effect)s, NOW(), NOW(), %(paladin_id)s);"
            data = {
                "name": "red_potion.png",
                "description": "juicy red blood from the depths of the dragon's lair, rumored to have healing properties",
                "effect": "Gain 20 HP",
                "paladin_id": session['paladin_id']
            }
            result = connectToMySQL('game').query_db(query, data)

            #update the paladin's gold
            query_update = "UPDATE paladin SET gold = %(new_gold)s WHERE id = %(id)s;"
            data_update = {
                "new_gold": paladin_gold - potion_gold,
                "id": session['paladin_id']
            }
            result_update = connectToMySQL('game').query_db(query_update, data_update)

            #append activities//PURCHASED
            session['activities'].append("You have purhcased the red potion. It is now available in your inventory")

        else: 
            #append activities//NO PURCHASE
            session['activities'].append("You don't have enough gold to purchase that item!")

#/YELLOW POTION/
    #check the potion id for yellow
    elif request.form['option'] == 'yellow_potion':
        query_gold = "SELECT gold FROM items_shop WHERE name = %(name)s;"
        data_gold = {
            "name": 'yellow_potion.png'
        }
        #set potion gold
        potion_gold = connectToMySQL('game').query_db(query_gold, data_gold)[0]["gold"]

        #check to see if paladin has enough gold
        if paladin_gold >= potion_gold:
            query = "INSERT INTO inventory (name, description, effect, created_at, updated_at, paladin_id) VALUES (%(name)s, %(description)s, %(effect)s, NOW(), NOW(), %(paladin_id)s);"
            data = {
                "name": "yellow_potion.png",
                "description": "delicious syrupy nectar from the abyss of the nectar tree, rumored to increase your attack",
                "effect": "Gain 1 Attack",
                "paladin_id": session['paladin_id']
            }
            result = connectToMySQL('game').query_db(query, data)

            #update the paladin's gold
            query_update = "UPDATE paladin SET gold = %(new_gold)s WHERE id = %(id)s;"
            data_update = {
                "new_gold": paladin_gold - potion_gold,
                "id": session['paladin_id']
            }
            result_update = connectToMySQL('game').query_db(query_update, data_update)
            
            #append activities//PURCHASED
            session['activities'].append("You have purhcased the yellow potion. It is now available in your inventory")

        else: 
            #append activities//NO PURCHASE
            session['activities'].append("You don't have enough gold to purchase that item!")

#/GREEN POTION/
    #check for green potion on form
    elif request.form['option'] == 'green_potion':
        query_gold = "SELECT gold FROM items_shop WHERE name = %(name)s;"
        data_gold = {
            "name": 'green_potion.png'
        }
        #set potion gold
        potion_gold = connectToMySQL('game').query_db(query_gold, data_gold)[0]["gold"]

        #compare paladin and potion gold
        if paladin_gold >= potion_gold:
            query = "INSERT INTO inventory (name, description, effect, created_at, updated_at, paladin_id) VALUES (%(name)s, %(description)s, %(effect)s, NOW(), NOW(), %(paladin_id)s);"
            data = {
                "name": "green_potion.png",
                "description": "ooey gooey sticky green lather from the dragon's skin itself, rumored to increase the defense of whoever wears it",
                "effect": "Gain 1 Defense",
                "paladin_id": session['paladin_id']
            }
            result = connectToMySQL('game').query_db(query, data)

            #update the paladin's gold
            query_update = "UPDATE paladin SET gold = %(new_gold)s WHERE id = %(id)s;"
            data_update = {
                "new_gold": paladin_gold - potion_gold,
                "id": session['paladin_id']
            }
            result_update = connectToMySQL('game').query_db(query_update, data_update)

            session['activities'].append("You have purhcased the green potion. It is now available in your inventory")
        else: 
            #append activities//NO PURCHASE
            session['activities'].append("You don't have enough gold to purchase that item!")

    #FINISH - REDIRECT        
    return redirect ('/tavern')

@app.route('/tavern/rest')
def tavern_rest():
    query = "SELECT * FROM paladin WHERE user_id = %(user_id)s"
    data = {
        "user_id": session['user_id']
    }
    results = connectToMySQL('game').query_db(query,data)

    query = "UPDATE paladin SET hp = %(hp)s WHERE id = %(paladin_id)s;"
    data = {
        "paladin_id" : session['paladin_id'],
        "hp" : 40
    }
    results = connectToMySQL('game').query_db(query,data)

    session['activities'].append("You take a long rest and awake in the morning fully rejuvinated")

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
    if 'actions' not in session:
        session['actions'] = []
    #Load image of enemy
    if 'is_enemy_alive' not in session:
        session['is_enemy_alive'] = True

    #INSERT Enemy into Database
    query = "INSERT INTO enemies(name, attack,defense,hp,created_at,updated_at,user_id) VALUE ('zombie', 15,5,10,NOW(),NOW(),%(id)s);"
    data = {
        "id" : session['user_id']
    }
    enemy = connectToMySQL('game').query_db(query,data)
    session['is_enemy_alive'] = True
    return redirect('/combat')

@app.route('/combat')
def combat():
    #QUERY for INVENTORY
    query = "SELECT * FROM inventory WHERE paladin_id = %(paladin_id)s"
    data = {
        "paladin_id" : session['paladin_id']
    }
    result = connectToMySQL('game').query_db(query, data)

    #GRAB PALADIN
    query_pal = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data_pal = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query_pal,data_pal)

    #Query to grab enemy object
    query = "SELECT * from enemies WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    enemies = connectToMySQL('game').query_db(query,data)

    #QUERY player attack
    query_attack = "SELECT attack FROM paladin WHERE id = %(id)s;"
    data_attack = {
        "id": session['paladin_id']
    }
    attack_stats = connectToMySQL('game').query_db(query_attack, data_attack)[0]["attack"]

    #QUERY player defense
    query_defense = "SELECT defense FROM paladin WHERE id = %(id)s;"
    data_defense = {
        "id": session['paladin_id']
    }
    defense_stats = connectToMySQL('game').query_db(query_defense, data_defense)[0]["defense"]

    return render_template("combat.html", inventory = result, paladin = paladin, enemies = enemies, player_attack = attack_stats, player_defense = defense_stats)

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

    #if enemy is dead.
    if session['is_enemy_alive'] == False:
        return redirect(f"/combat/on_enemy_death")

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
    if 'actions' not in session:
        session['actions'] = []
    session['actions'].append("You killed the zombie!")
    session['actions'].append("You dealt the Zombie 5 damage")

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

    #if enemy is dead.
    if session['is_enemy_alive'] == False:
        return redirect(f"/combat/on_enemy_death")

    #All Calculations of hitting and damage.
    new_enemyHP = int(enemies[0]['hp']) - int(paladin[0]['attack'] - 4) + int(enemies[0]['defense'])

    #NewStatus Effects for player
    if paladin[0]['hp'] + 20 >= 40:
        new_paladin_hp = 40
    else:
        new_paladin_hp = paladin[0]['hp'] + 20
    query = "UPDATE paladin SET hp = '%(new_paladin_hp)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_paladin_defense" : int(new_paladin_hp),
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #NewStatus Effects for enemy


    #query for updating the enemy hp
    query = "UPDATE enemies SET hp = '%(new_enemyHP)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_enemyHP" : int(new_enemyHP),
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    #putting to actions
    if 'actions' not in session:
            session['action'] = []
    session['actions'].append("You dealt the Zombie 1 damage.")
    session['actions'].append("You healed 1 damage.")

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

    #if enemy is dead.
    if session['is_enemy_alive'] == False:
        return redirect(f"/combat/on_enemy_death")

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

    #query for updating the enemy hp

    #putting to activities

    if 'action' not in session:
        session['action'] = []
    session['actions'].append("You gained 1 defense.")

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
    print(paladin[0]['hp'] - enemies[0]['attack'] + paladin[0]['defense'])
    if paladin[0]['hp'] - enemies[0]['attack'] + paladin[0]['defense'] <= 0:
        return redirect('/combat/player_death')
    else:
        if paladin[0]['defense'] >= enemies[0]['attack']:
            new_paladin_hp = paladin[0]['hp'] - 1
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

    #putting to actions
    if 'actions' not in session:
        session['actions'] = []
    print(session['actions'])
    session['actions'].append("Zombie hits you for 5.")

    return redirect('/combat')

@app.route('/combat/player_death')
def combat_on_player_death():
    return redirect('/death')

@app.route('/combat/on_enemy_death')
def combat_On_Enemy_Death():
    #give more money
    query = "SELECT * from Paladin WHERE user_id = %(user_id)s;"
    data = {
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)

    query = "UPDATE paladin SET gold = '%(new_paladin_gold)s' WHERE user_id = %(user_id)s;"
    data = {
        "new_paladin_gold" : paladin[0]['gold'] + 5,
        "user_id" : session['user_id']
    }
    paladin = connectToMySQL('game').query_db(query,data)
    #query for killing an enemy at too low of hp
    query = "DELETE from enemies WHERE user_id = %(user_id)s;"
    data = {
        'user_id' : session['user_id']
    }
    connectToMySQL('game').query_db(query,data)
    if 'action' not in session:
        session['action'] = []
    session['actions'].append("You killed the zombie!")
    session['actions'].append("Press advance to move forward!")
    session['is_enemy_alive'] = False
    return redirect('/combat')

@app.route('/combat/next_enemy')
def combat_next_enemy():
    #grabbing all of the enemies to see if any exist
    query = "SELECT * FROM game.enemies;"
    enemies = connectToMySQL('game').query_db(query)
    if session['is_enemy_alive'] == False:
        query = "INSERT INTO enemies(name, attack,defense,hp,created_at,updated_at,user_id) VALUE ('zombie', 15,5,10,NOW(),NOW(),%(id)s);"
        data = {
            "id" : session['user_id']
        }
        enemy = connectToMySQL('game').query_db(query,data)
        session['is_enemy_alive'] = True
        if 'actions' not in session:
            session['actions'] = []
        session['actions'].append("Another Zombie!")
    return redirect('/combat')

#--------------------------------use item----------------------------------#

@app.route('/use_item', methods = ['POST'])
def use_item():
#GRAB PALADIN
    query_pal = "SELECT * from Paladin WHERE id = %(paladin_id)s;"
    data_pal = {
        "paladin_id" : session['paladin_id']
    }
    paladin = connectToMySQL('game').query_db(query_pal,data_pal)

#QUERY PALADIN'S INVENTORY
    query_inv = "SELECT * FROM inventory WHERE paladin_id = %(paladin_id)s"
    data_inv = {
        "paladin_id" : session['paladin_id']
    }
    inventory = connectToMySQL('game').query_db(query_inv, data_inv)

#CHECK to see if they are any of the following items
    #check for red potion
    if request.form.get('item_option') == "red_potion.png":
        #Heal paladin for 20 HP
        #if their HP is greater than 20, just set it to max hp
        if paladin[0]['hp'] + 10 >= 40:
            new_paladin_hp = 40
        #else give them 20 health
        else:
            new_paladin_hp = paladin[0]['hp'] + 10

        query = "UPDATE paladin SET hp = '%(new_paladin_hp)s' WHERE id = %(paladin_id)s;"
        data = {
                "new_paladin_hp" : int(new_paladin_hp),
                "paladin_id" : session['paladin_id']
            }
        update_hp = connectToMySQL('game').query_db(query,data)

        #delete from paladin's inventory
        query = "DELETE FROM inventory WHERE id = %(item_id)s"
        data = {
            "item_id": request.form.get('item_id')
        }
        deleted_item = connectToMySQL('game').query_db(query,data)
    
    #check for yellow potion
    elif request.form.get('item_option') == "yellow_potion.png":
        #APPLY THE EFFECT FOR YELLOW POTION
        #create new paladin attack
        new_paladin_attack = paladin[0]['attack'] + 5
        #set the new paladin attack
        query = "UPDATE paladin SET attack = '%(new_paladin_attack)s' WHERE id = %(paladin_id)s;"
        data = {
                "new_paladin_attack" : int(new_paladin_attack),
                "paladin_id" : session['paladin_id']
            }
        update_attack = connectToMySQL('game').query_db(query,data)
        
        #delete from paladin's inventory
        query = "DELETE FROM inventory WHERE id = %(item_id)s"
        data = {
            "item_id": request.form.get('item_id')
        }
        deleted_item = connectToMySQL('game').query_db(query,data)
    
    #check for green potion
    elif request.form.get('item_option') == "green_potion.png":
        #APPLY THE EFFECT FOR GREEN POTION
        #create new paladin attack
        new_paladin_defense = paladin[0]['defense'] + 3
        #set the new paladin attack
        query = "UPDATE paladin SET defense = '%(new_paladin_defense)s' WHERE id = %(paladin_id)s;"
        data = {
                "new_paladin_defense" : int(new_paladin_defense),
                "paladin_id" : session['paladin_id']
            }
        update_defense = connectToMySQL('game').query_db(query,data)

        #delete from paladin's inventory
        query = "DELETE FROM inventory WHERE id = %(item_id)s"
        data = {
            "item_id": request.form.get('item_id')
        }
        deleted_item = connectToMySQL('game').query_db(query,data)

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
    query = "DELETE from paladin WHERE user_id = %(user_id)s;"
    data = {
        'user_id' : session['user_id']
    }
    #THIS IS THE COMMENT FOR TEST
    connectToMySQL('game').query_db(query,data)
    session.clear()
    return render_template('death.html')


if __name__=="__main__":
    app.run(debug=True)