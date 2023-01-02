# Imports 
import random as rn
import time
import pickle
import numpy as np
import os

### Global Variables and Configurations

players = {}
playersorder = []
yes_list = ['yes', 'yea', 'yup', 'y', '', ' ', 'ye']
start_time = time.time()

pass_go_cash = 300                                                  # DEFAULT: pass_go_cash = 200
start_money = 3000                                                  # DEFAULT: start_money = 3000
avg_networth = start_money
winning_condition_amount = 30000                                    # DEFAULT: winning_condition = 20000
max_prop_level = 5                                                  # DEFAULT: max_prop_level = 5 
dice_size = 6                                                       # DEFAULT: dice_size = 6
lives = 1                                                           # DEFAULT: lives = 2 
redepemtion_reward = False                                          # DEFAULT: FALSE, people are not revived.
bail_price = 200                                                    # DEFAULT: bail_price gets modified in the landed_on() jail section
real_life_dice = False                                              # Option to chose between real life dice, an system dice.
random_card = True                                                  # Set to True to get a random card once in a while. (spice up the game u know?)


lottery_wallet = 1000
stock_start_value = 500                                             # DEFAULT:  start_value = 400  
stock_minimum_value = int(stock_start_value/2)                      # DEFAULT:  stock_minimum_value = start_value
stock_max_value = 5000                                              # DEFAULT:  stock_max_value = 5000   
bound_for_volatile_stocks = stock_max_value/4                       # DEFAULT:  bound_for_volatile_stocks = stock_max_value/4       
stock_dist = "normal"                                               # DEFAULT:  stock_dist = "normal" or "uniform"
#stock_dist = "uniform"                                             # DEFAULT:  stock_dist = "normal" or "uniform"
stock_drop_to_value = stock_max_value/5                             # DEFAULT:  stock_drop_to_value = stock_max_value/5 
phase1_bound = (0.96,1.08)                                          # DEFAULT:  phase1_bound = (0.96 , 1.08)
phase2_bound = (0.85,1.07)                                          # DEFAULT:  phase2_bound = (0.85 , 1.07)
phase3_bound = (0.95,1.20)                                          # DEFAULT:  phase3_bound = (0.95 , 1.20)
phase_change_rounds = 7                                             # DEFAULT:  phase_change_rounds = 7


  




roundcount = 0

side_list = ['South', 'West', 'North', 'East']
color_list = ['Brown', 'Grey', 'Pink', 'Orange', 'Red', 'Yellow', 'Green', 'Blue']

Brown_1 = {"name": "Old Kent Road" , "price": 60, "original_price":60 , "rent":20, "level" : 1 , "owner": None, "side": "South", "mortgaged":False , "color" : "Brown"} 
Brown_2 = {"name": "Whitechapel Road" , "price": 60, "original_price":60 , "rent":20, "level" : 1 , "owner": None, "side": "South", "mortgaged":False, "color" : "Brown"} 
Grey_1 = {"name": "The Angel Islington", "price": 100, "original_price":100 , "rent":30, "level" : 1 , "owner": None, "side": "South", "mortgaged":False, "color" : "Grey"}
Grey_2 = {"name": "Euston Road", "price": 100, "original_price":100 , "rent":30, "level" : 1 , "owner": None, "side": "South", "mortgaged":False, "color" : "Grey"}
Grey_3 = {"name": "Pentonville Road", "price": 120, "original_price":120 , "rent":40, "level" : 1 , "owner": None, "side": "South", "mortgaged":False, "color" : "Grey"}
Pink_1 = {"name": "Pall Mall", "price": 140, "original_price":140 , "rent":50, "level" : 1 , "owner": None, "side": "West", "mortgaged":False, "color" : "Pink"}
Pink_2 = {"name": "Whitehall", "price": 140, "original_price":140 , "rent":50, "level" : 1 , "owner": None, "side": "West", "mortgaged":False, "color" : "Pink"}
Pink_3 = {"name": "Northumberland Avenue", "price": 160, "original_price":160 , "rent":60, "level" : 1 , "owner": None, "side": "West", "mortgaged":False, "color" : "Pink"}
Orange_1 = {"name": "Bow Street", "price": 180, "original_price":180 , "rent":70, "level" : 1 , "owner": None, "side": "West", "mortgaged":False, "color" : "Orange"}
Orange_2 = {"name": "Marlborough Street" , "price": 180, "original_price":180 , "rent":70, "level" : 1 , "owner": None, "side": "West", "mortgaged":False, "color" : "Orange"}
Orange_3 = {"name": "Vine Street", "price": 200, "original_price":200 , "rent":80, "level" : 1 , "owner": None, "side": "West", "mortgaged":False, "color" : "Orange"}
Red_1 = {"name": "Strand", "price": 220, "original_price":220 , "rent":90, "level" : 1 , "owner": None, "side": "North", "mortgaged":False, "color" : "Red"}
Red_2 = {"name": "Fleet Street", "price": 220, "original_price":220 , "rent":90, "level" : 1 , "owner": None, "side":"North", "mortgaged":False, "color" : "Red"}
Red_3 = {"name": "Trafalgar Square", "price": 240, "original_price":240 , "rent":100, "level" : 1 , "owner": None, "side":"North", "mortgaged":False, "color" : "Red"}
Yellow_1 = {"name": "Leicester Square", "price": 260, "original_price":260 , "rent":110, "level" : 1 , "owner": None, "side":"North", "mortgaged":False, "color" : "Yellow"}
Yellow_2 = {"name": "Coventry Street", "price": 260, "original_price":260 , "rent":110, "level" : 1 , "owner": None, "side":"North", "mortgaged":False, "color" : "Yellow"}
Yellow_3 = {"name": "Piccadilly", "price": 280, "original_price":280 , "rent":120, "level" : 1 , "owner": None, "side":"North", "mortgaged":False, "color" : "Yellow"}
Green_1 = {"name": "Regent Street", "price": 300, "original_price":300 , "rent":130, "level" : 1 , "owner": None, "side":"East", "mortgaged":False, "color" : "Green"}
Green_2 = {"name": "Oxford Street", "price": 300, "original_price":300 , "rent":130, "level" : 1 , "owner": None, "side":"East", "mortgaged":False, "color" : "Green"}
Green_3 = {"name": "Bond Street", "price": 320, "original_price":320 , "rent":150, "level" : 1 , "owner": None, "side":"East", "mortgaged":False, "color" : "Green"}
Blue_1  = {"name": "Park Lane", "price": 350, "original_price":350 , "rent":175, "level" : 1 , "owner": None, "side":"East", "mortgaged":False, "color" : "Blue"}
Blue_2  = {"name": "Mayfair", "price": 400, "original_price":400 , "rent":200, "level" : 1 , "owner": None, "side":"East", "mortgaged":False, "color" : "Blue"}


All_property_list = [Brown_1,Brown_2,Grey_1,Grey_2,Grey_3,Pink_1,Pink_2,Pink_3,Orange_1,Orange_2,Orange_3,Red_1
                ,Red_2,Red_3,Yellow_1,Yellow_2,Yellow_3,Green_1,Green_2,Green_3,Blue_1,Blue_2]


# Creating the Game board 

Start = 0
Event = 0
Location_icon = 0 
Visit_jail = 0
Go_to_jail = 0
Free_park = 0

# For user information 
board_placement_names = {0: "Start" , 1: "Old Kent Road", 2:"Event" , 3: "Whitechapel Road", 4: "Event", 5: "The Angel Islington", 
                   6: "Euston Road", 7: "Location icon", 8: "Pentonville Road", 9:"Visit jail", 10: "Pall Mall" , 11: "Event", 
                   12: "Whitehall", 13: "Northumberland Avenue", 14: "Bow Street" ,
                   15: "Marlborough Street", 16: "Location icon", 17: "Vine Street" , 18: "Free park" , 19: "Strand", 20: "Event",
                   21: "Fleet Street", 22: "Trafalgar Square", 23: "Leicester Square" , 24: "Coventry Street" , 25: "Location icon" , 
                   26: "Piccadilly" , 27: "Go to jail", 28: "Regent Street", 29: "Event", 30: "Oxford Street", 31: "Bond Street", 
                   32: "Event" , 33: "Park Lane", 34: "Location icon", 35:"Mayfair" , "jail": "Jail"}


# For functionality # THE REAL BOARD
board_placement = {0: "Start" , 1: Brown_1, 2:"Event" , 3: Brown_2, 4: "Event", 5: Grey_1, 6: Grey_2, 7: "Location_icon", 
                   8: Grey_3, 9:"Visit_jail", 10: Pink_1 , 11: "Event", 12: Pink_2, 13: Pink_3, 14: Orange_1 ,
                   15: Orange_2, 16: "Location_icon", 17: Orange_3 , 18: "Free_park" , 19: Red_1, 20: "Event",
                   21: Red_2, 22: Red_3, 23:Yellow_1 , 24:Yellow_2 , 25: "Location_icon" , 26: Yellow_3 ,
                   27: "Go_to_jail", 28: Green_1, 29: "Event", 30: Green_2, 31: Green_3, 32: "Event" , 33: Blue_1
                   , 34: "Location_icon", 35:Blue_2 , "jail": "Jail"}


# TEMPORARY BOARD WITH MOSTLY EVENT TILES AND GO TO JAIL AT 2!!!!
#board_placement = {0: "Start" , 1: Brown_1, 2:"Visit_jail" , 3: "Visit_jail", 4: "Event", 5: "Visit_jail", 6: Grey_2, 7: "Location_icon", 
#                   8: Grey_3, 9:"Visit_jail", 10: "Visit_jail" , 11: "Event", 12: "Visit_jail", 13: "Visit_jail", 14: Orange_1 ,
#                   15: Orange_2, 16: "Location_icon", 17: Orange_3 , 18: "Free_park" , 19: Red_1, 20: "Event",
#                   21: Red_2, 22: Red_3, 23:Yellow_1 , 24:Yellow_2 , 25: "Location_icon" , 26: "Event" ,
#                   27: "Go_to_jail", 28: "Event", 29: "Event", 30: "Event", 31: "Event", 32: "Event" , 33: "Event"
#                   , 34: "Location_icon", 35:"Event" , "jail": "Jail"}





########################################################    
# Chance card functions

# Choose a color set on the board an increase all the properties in it by +1 level
def chance_card_1(player):
    #print("chance_card_1")
    # Possitive
    print("  Choose a color set on the board an increase all the properties in it by +1 level.")
    print("")
    for enum,color in enumerate(color_list):
        print("{}.  {}".format(enum +1 ,color))
    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 1
    color_chosen = color_list[numba]
    print("Color set chosen: ", color_chosen)
    
    for prop in All_property_list:
        if prop['color'] == color_chosen:
            prop['level'] += 1

# Choose a color set on the board an decrease all the properties in it by -1 level
def chance_card_2(player):
    # Negative
    print("  Choose a color set on the board an decrease all the properties in it by -1 level.")
    for enum,color in enumerate(color_list):
        print("{}.  {}".format(enum +1 ,color))
    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 1
    color_chosen = color_list[numba]
    print("color_chosen: ", color_chosen)
    
    for prop in All_property_list:
        if prop['color'] == color_chosen:
            prop['level'] -= 1

# Choose ANY property on the board an set it to level 5
def chance_card_3(player):
    #print("chance_card_3")
    # Possitive
    print("  Choose ANY property on the board an set it to level 5.")
    white_space(2)
    #choice = None
    for enum,prop in enumerate(All_property_list):
        if prop['owner'] != None:
            print(" {}.  {:<25}   Level: {:<4}   Rent: {:<4}   Owner: {:<15}".format(enum+1 
            ,prop['name'], prop['level'], prop['rent'], prop['owner']))
        else:
            print(" {}.  {:<25}   Level: {:<4}   Rent: {:<4}   Owner:  ".format(enum+1 
            ,prop['name'], prop['level'], prop['rent']))

    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 1
    prop_chosen = All_property_list[numba]
    prop_chosen['level'] = 5    

# Chose a side of the board and decrease all property levels by -1
def chance_card_4(player):
    #print("chance_card_4")
    # Negative
    print("  Chose a side of the board and decrease all property levels by -1.")
    for enum,side in enumerate(side_list):
        print(" {}.  {}".format(enum+1 ,side))
    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 1
    side_chosen = side_list[numba]
    for prop in All_property_list:
        if prop['side'] == side_chosen:
            prop['level'] -= 1
    print("")
    print("  All properties on the {} side has had their level decreased by -1.".format(side_chosen))

# The Richest player gives all other players 200 dollars
def chance_card_5(player):
    #print("chance_card_5")
    # Smoother
    print("  The Richest player gives all other players 200 dollars")
    richest_name = ''
    richest_amount = 0 
    for dude in playersorder:
        if players[dude]['Wallet'] > richest_amount:
            richest_name = dude
            richest_amount = players[dude]['Wallet']
    
    for new_dude in playersorder:
        players[new_dude]['Wallet'] += 200
        players[richest_name]['Wallet'] -= 200
    
    print("  Thank you",richest_name + '. You now have',int(players[richest_name]['Wallet']),"in your Wallet.")
    white_space(4)

# Collect 100$ for each property you own
def chance_card_6(player):
    #print("chance_card_6")
    # Possitive
    print("  Collect 100$ for each property you own from the bank.")
    amount_you_own = 0
    for prop in players[player]['Property']:
        amount_you_own += 1

    players[player]['Wallet'] += 100*amount_you_own 
    print("")
    print("  You collect {}$ !!!".format(100*amount_you_own))
    print("")

# Pay the bank 100$ for each property you own
def chance_card_7(player):
    #print("chance_card_7")
    # Negative
    global lottery_wallet
    print("  Pay the bank 100$ for each property you own.")
    amount_you_own = 0
    for prop in players[player]['Property']:
        amount_you_own += 1
    players[player]['Wallet'] -= (100* amount_you_own)
    lottery_wallet += (100* amount_you_own)
    print("")
    print("  You paid {}$ !!! OUCH.".format(100*amount_you_own) )
    print("")

# Inflation! Increase all property levels on the board by +1!
def chance_card_8(player):
    #print("chance_card_8")
    # Neutrual
    print("  Inflation! Increase all property levels on the board by +1!")
    print("  ")
    for prop in All_property_list:
        prop['level'] +=1 

# Recession! Decrease all properties level on the board by -1
def chance_card_9(player):
    #print("chance_card_9")
    # Neutrual
    print("  Recession! Decrease all properties level on the board by -1!")
    for prop in All_property_list:
        prop['level'] -=1 
    pass

# Chose a side of the board to reset to level 1
def chance_card_10(player):
    #print("chance_card_10")
    # Neutrual
    print("  You are a very angry person, with a very powerful card!")
    print("  Chose a side of the board to reset to level 1.")
    for enum,side in enumerate(side_list):
        print(" {}.  {}".format(enum+1 ,side))
    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 1
    side_chosen = side_list[int(numba)]
    for prop in All_property_list:
        if prop['side'] == side_chosen:
            prop['level'] = 1

# Earthquake on the random side of the board! All property levels decrease by 3 levels. 
def chance_card_11(player):
    #print("chance_card_11")
    numba = rn.randint(0,3)
    side_chosen = side_list[numba]
    for prop in All_property_list:
        if prop['side'] == side_chosen:
            prop['level'] -= 3
            if prop['level'] < 1: 
                prop['level'] = 1 
    print("  Earthquake on the {} side of the board! All property levels on that side decrease by 3 levels.".format(side_chosen))
    

# Every player on the board pays 200$
def chance_card_12(player):
    #print("treasure_card_2")
    global lottery_wallet
    print("  Every player on the board pays 200$")
    for dude in playersorder:
        players[dude]['Wallet']-= 200
        lottery_wallet += 200

# Pay the bank 150$ for each property you own.
def chance_card_13(player):
    #print("chance_card_7")
    # Negative
    global lottery_wallet
    print("  Pay the bank 150$ for each property you own.")
    amount_you_own = 0
    for prop in players[player]['Property']:
        amount_you_own += 1
    players[player]['Wallet'] -= (150* amount_you_own)
    lottery_wallet += (150* amount_you_own)
    print("")
    print("  You paid {}$ !!! OUCH.".format(150*amount_you_own) )
    print("")

# All your stocks change phase to phase 1 stocks.
def chance_card_14(player):
    print("  All your stocks change phase to phase 1 stocks.")
    print("     Phase 1 rate: ",round((phase1_bound[0]-1)*100),"%  , ", round((phase1_bound[1]-1)*100) , "%")
    print("")
    if len(players[player]['Stocks']) > 0:
        for stock in players[player]['Stocks']:
            stock['phase'] = phase1
            stock['phase_number'] = 1

def chance_card_15(player):
    #print("chance_card_11")
    numba = rn.randint(0,3)
    side_chosen = side_list[numba]
    for prop in All_property_list:
        if prop['side'] == side_chosen:
            prop['level'] += 2
    print("  Asian tourists are invading the {} side of the board! All property levels on that side increase by +2.".format(side_chosen))
    

def chance_card_16(player):
    print("")
    print("  You are a real estate genius! Sell all your properties for an additional 50"+"%"+" of their current price!")
    print("  Additionally, you gain 2 Immunity!")
    print("")
    #amount_of_props_to_sell = len(players[player]['Property'])
    money_gained = 0
    players[player]['Immunity'] += 2

    for prop in All_property_list:
        if prop['owner'] == player:
            players[player]['Property'].remove(prop)
            prop['owner'] = None
            players[player]['Wallet'] += prop['price']*1.5
            money_gained += int(prop['price']*1.5)
            #amount_of_props_to_sell -= 1

    print("")
    print("   You sold every property you own and got {}$. Go make some money!!".format(round(money_gained)))
    print("")    

chance_cards = [chance_card_1, chance_card_2, chance_card_3, chance_card_4, chance_card_5, chance_card_6,
                chance_card_7, chance_card_8, chance_card_9, chance_card_10, chance_card_11, chance_card_12,
                 chance_card_13, chance_card_14, chance_card_15, chance_card_16]

#chance_cards = [chance_card_3]


########################################################           
# Treasure card functions

# Advance to Start and collect 200$
def treasure_card_1(player):
    #print("treasure_card_1")
    print("  Advance to Start and collect 500$ !!!")
    players[player]['Placement'] = 0
    players[player]['Wallet'] += 500

# Every player on the board receives 200$
def treasure_card_2(player):
    #print("treasure_card_2")
    print("  Every player on the board receives 200$")
    for dude in playersorder:
        players[dude]['Wallet']+= 200
        
# Collect 200$ from each player        
def treasure_card_3(player):
    #print("treasure_card_3")
    print("  Collect 200$ from each player")
    for dude in playersorder:
        players[dude]['Wallet'] -= 200
        players[player]['Wallet'] += 200

# Congratulations! you got all properties from random color set or a side! (66% / 33%).
def treasure_card_4(player):
    flip_coin = rn.randint(1,3)
    if flip_coin == 1:
        numba = rn.randint(0,3)
        side_chosen = side_list[numba]
        for prop in All_property_list:
            if prop['side'] == side_chosen:
                if prop['owner'] != None:
                    old_player = prop['owner']
                    players[old_player]['Property'].remove(prop)
                prop['owner'] = player
                players[player]['Property'].append(prop)
                

        print("")
        print("  Congratulations! {} got all properties on the {} side!".format(player,side_chosen))
        print("  If any player has previously owned any of these properties, take them away from that person")
        print("  and add it to your hand.")
        print("")
        print("  This happens approximately 1 out of {} times when someone lands on an Event tile!!!".format(len(treasure_cards)*4*3))
        print("")
                
    else:      
        color = rn.choice(color_list)
        
        for prop in All_property_list:
            if prop['color'] == color:
                if prop['owner'] != None:
                    old_player = prop['owner']
                    players[old_player]['Property'].remove(prop)
                prop['owner'] = player
                players[player]['Property'].append(prop)

        print("")
        print("  Congratulations! {} got all properties from the {} color set!".format(player,color))
        print("  If any player has previously owned any of these properties, take them away from that person")
        print("  and add it to your hand.")
        print("")


# Collect 400$ from each player
def treasure_card_5(player):
    #print("treasure_card_5")
    print("  Collect 400$ from each player")
    for dude in playersorder:
        players[dude]['Wallet'] -= 400
        players[player]['Wallet'] += 400

# Grant immunity from paying rent the next TWO times
def treasure_card_6(player):
    #print("treasure_card_6")
    print("  Grant immunity from paying rent the next TWO times you land on a property who belongs to someone else.")
    players[player]['Immunity'] += 2
    print("")

# All of your stocks increase with 50%
def treasure_card_7(player):
    print("")
    print("  All of your stocks increase with "+'50%'+" in value!!!")
    print("  If any of your stocks passes the price ceiling at {}$".format(int(stock_max_value)))
    print("  they are automatically sold for {}$ ".format(int(stock_max_value)))
    print("")
    print("  If you don't have any stocks, receive a random one for free instead...")
    print("")
    if len(players[player]['Stocks']) > 0:
        for stock in players[player]['Stocks']:
            old_price = stock['price']
            stock['price'] = int(1.5 * stock['price'])
            if stock['price'] > stock_max_value:
                stock['price'] = stock_drop_to_value
                stock['owner'] = None
                players[player]['Wallet'] += stock_max_value
                players[player]['Stocks'].remove(stock)
            stock['price_history'].append(stock['price'])
            stock['percent_increase_pr_turn'] = round(stock['price']*100 / old_price  ,  1)
    else:
        temp_list = []
        for stock in stocks_list:
            if stock['owner'] == None:
                temp_list.append(stock['name'])
            else:
                continue

        if len(temp_list) == 0:
            print("") 
            print(" You have no stocks and there are no stocks for you to receive :( ") 
            return
        
        random_stock_name = rn.choice(temp_list)
        for stock in stocks_list:
            if stock['name'] == random_stock_name:
                stock['owner'] = player
                players[player]['Stocks'].append(stock)
                stock['bought_price'] = int(stock['price'])
                return

    
# Collect rent from the bank equal to the average rent of your active properties
def treasure_card_8(player):
    #print("treasure_card_8")
    print("  Collect rent from the bank equal to the average rent of your active properties.")
    avg_rent = 0
    mortgaged = 0
    amount_of_props = 1

    for prop in players[player]['Property']:
        if prop['mortgaged'] == False:
            avg_rent += (prop['rent'])
        else:
            mortgaged += 1
    if len(players[player]['Property']) >= 1:
        amount_of_props = len(players[player]['Property'])

    if amount_of_props == mortgaged:
        amount_of_props +=1
        # This is to stop from dividing by zero... Look at the equation below.

    new_avg_rent = int(avg_rent / (amount_of_props- mortgaged ) )

    print("")
    print("  You collect {}$ from the bank!".format(int(new_avg_rent)))
    print("")
    players[player]['Wallet'] += new_avg_rent

# Collect rent from the bank equal to the property of yours which has the highest active rent
def treasure_card_9(player):
    #print("treasure_card_9")
    print("  Collect rent from the bank equal to the property of yours which has the highest active rent.")
    high_rent = 0
    prop_name = ''
    prop_level = 1
    for prop in players[player]['Property']:
        if prop['rent'] > high_rent:
            if prop['mortgaged'] == False:
                prop_name = prop['name']
                high_rent = prop['rent']
                prop_level = prop['level']
    print("")
    print("  You collect {}$ from the bank by having {} in level {}!".format(high_rent,prop_name,prop_level))
    print("")
    players[player]['Wallet'] += high_rent

# Collect rent from the richest player equal to the property of yours which has the highest active rent
def treasure_card_10(player):
    #print("treasure_card_10")
    print("  Collect rent from the richest player equal to the property of yours which has the highest active rent.")
    high_rent = 0
    prop_name = ''
    prop_level = 1
    richest_name = ''
    richest_amount = 0 
    
    for prop in players[player]['Property']:
        if prop['rent'] > high_rent:
            if prop['mortgaged'] == False:
                prop_name = prop['name']
                prop_level = prop['level']
                high_rent = prop['rent']

    for dude in playersorder:
        if players[dude]['Wallet'] > richest_amount:
            richest_name = dude
            richest_amount = players[dude]['Wallet']

    players[player]['Wallet'] += high_rent
    players[richest_name]['Wallet'] -= high_rent 

    if player != richest_name:
        print("")
        print("  You collect {}$ from {} by having {} in level {}!".format(high_rent,richest_name,prop_name,prop_level))
        print("")
    else:
        print("")
        print("  You are the richest boi...")
        print("")


# Collect rent from the player who owns the most amount of properties
def treasure_card_11(player):
    #print("treasure_card_11")
    print("  Collect rent from the player who owns the most amount of properties." + "\n" +
             "  The rent is equal to the rent of the porperty you own which has the highest active rent.")

    high_rent = 0
    prop_name = player
    prop_level = 1
    player_with_most_props = player
    richest_amount = 0 

    for prop in players[player]['Property']:
        if prop['rent'] > high_rent:
            if prop['mortgaged'] == False:
                prop_name = prop['name']
                high_rent = prop['rent']
                prop_level = prop['level']


    for dude in playersorder:
        if dude != player:
            if len(players[dude]['Property']) >= len(players[player_with_most_props]['Property']):
                player_with_most_props = dude

    
    players[player_with_most_props]['Wallet'] -= high_rent
    players[player]['Wallet'] += high_rent

    print("")
    print("  You collect {}$ from {} by having {} in level {}!".format(high_rent,player_with_most_props,prop_name,prop_level))
    print("")

# Pick any property (even if its owned by a player) and add it to your hand
def treasure_card_12(player):
    #print("treasure_card_12")
    print("  Pick any property (even if its owned by a player) and add it to your hand.")
    print("")
    for enum,prop in enumerate(All_property_list):
        print(" {}.  {}".format(enum+1 ,prop['name']))
    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 0
    prop_chosen = All_property_list[int(numba)]

    if prop_chosen['owner'] != None:
        old_owner = prop_chosen['owner']
        players[old_owner]['Property'].remove(prop_chosen)
        
    prop_chosen['owner'] = player
    players[player]['Property'].append(prop_chosen)

# Every player on the board receives 200 or 600
def treasure_card_13(player):
    ran_num = rn.randint(1,4)
    
    if ran_num == 3:
        print("  This happens approximately 1 out of {} times when someone lands on an Event tile!!!".format(len(treasure_cards)*4*4))
        print("  Collect 600$!!! from each player")
        for dude in playersorder:
            players[dude]['Wallet'] -= 600
            players[player]['Wallet'] += 600
    
    else: 
        print("  Collect 200$ from each player")
        for dude in playersorder:
            players[dude]['Wallet'] -= 200
            players[player]['Wallet'] += 200

# All of your stocks change to Phase 3
def treasure_card_14(player):
    print("")
    print("  All of your stocks change to Phase 3 !!! ") 
    print("    Phase 3 rate: ",round((phase3_bound[0]-1)*100),"%  , ", round((phase3_bound[1]-1)*100) , "%")
    print("")
    print("  If you don't have any stocks, receive a random one for free instead AND set it to phase 3...")
    print("")
    if len(players[player]['Stocks']) > 0:
        for stock in players[player]['Stocks']:
            stock['phase'] = phase3
            stock['phase_number'] = 3

    else:
        temp_list = []
        for stock in stocks_list:
            if stock['owner'] == None:
                temp_list.append(stock['name'])
            else:
                continue

        if len(temp_list) == 0:
            print("") 
            print(" You have no stocks and there are no stocks for you to receive :( ") 
            return
        
        random_stock_name = rn.choice(temp_list)
        for stock in stocks_list:
            if stock['name'] == random_stock_name:
                stock['phase'] = phase3
                stock['phase_number'] = 3
                stock['owner'] = player
                stock['bought_price'] = int(stock['price'])
                players[player]['Stocks'].append(stock)
                return


# Add a random property that you don't own to your hand.
def treasure_card_15(player):
    
    prop = rn.choice(All_property_list)
    while prop['owner'] == player:
        prop = rn.choice(All_property_list)

    if prop['owner'] != None:
        old_player = prop['owner']
        players[old_player]['Property'].remove(prop)
    prop['owner'] = player
    players[player]['Property'].append(prop)
    print("")
    print("   Add a random property that you don't own to your hand!")
    print("")
    print("   You received {} at level {} for free!".format(prop['name'] ,prop['level'] ))
    print("")


# Advance to Free Park (Jackpot!)
def treasure_card_16(player):
    print("")
    print("  Advance to Free Park and take the Jack Pot !!! ")
    print("")
    players[player]['Placement'] = 18
    input(" press Enter to continue... ")
    landed_on(player)


# Add 10% of your networth to your wallet!
def treasure_card_17(player):
    ran_num = rn.randint(1,4)
    
    if ran_num == 3:
        print("")
        print("  Take 25"+"%"+" of your Networth and add it to your wallet!!!")
        print("  This happens approximately 1 out of {} times when someone lands on an Event tile!!!".format(len(treasure_cards)*4*4))
        print("")
        players[player]['Wallet'] += players[player]['Networth']*0.25

    else: 
        print("  Take 10"+"%"+" of your Networth and add it to your wallet!")
        print("")
        players[player]['Wallet'] += players[player]['Networth']*0.10
        




treasure_cards = [treasure_card_1,treasure_card_2,treasure_card_3,treasure_card_4,treasure_card_5,treasure_card_6
                 ,treasure_card_7, treasure_card_8, treasure_card_9, treasure_card_10, treasure_card_11
                ,treasure_card_12, treasure_card_13, treasure_card_14, treasure_card_15,treasure_card_16,
                treasure_card_17]


########################################################    
# Curse Cards

# Pay rent equal to the rent of one of your properties to the poorest player
def curse_card_1(player):
    print("  Pay rent equal to the rent of one of your active properties to the poorest player in the game.")
    print("  Property chosen by random.")
    print("")
    if len(players[player]['Property']) == 0: 
        print("  You don't have any property, meaning that this cards effect does not occour...")
        print("")
        return

    else:
        temp_active_list = []
        for prop in players[player]['Property']:
            if prop['mortgaged'] == False:
                temp_active_list.append(prop)
        
        if len(temp_active_list) == 0: 
            print("  You don't have any active property, meaning that this cards effect does not occour...")
            print("")
            return

        random_prop = rn.choice(temp_active_list)
        players[player]['Wallet'] -= random_prop['rent']

        poorest_player = player
        for dude in playersorder:
            if players[dude]['Wallet'] < players[poorest_player]['Wallet']:
                poorest_player = dude
        
        players[poorest_player]['Wallet'] += random_prop['rent']
        print("")
        print("")
        print("  {} paid {}$ to {}".format(player,random_prop['rent'],poorest_player))
        print("")

# Pay rent equal to the rent of one of your random properties to the player with the lowest Networth
def curse_card_2(player):
    print("  Pay rent equal to the rent of one of your properties to the player with the lowest Networth in the game.")
    print("  Property chosen by random.")
    print("")
    if len(players[player]['Property']) == 0: 
        print("  You don't have any property, meaning that this cards effect does not occour...")
        print("")
    else:
        random_prop = rn.choice(players[player]['Property'])
        players[player]['Wallet'] -= random_prop['rent']

        poorest_player = player
        for dude in playersorder:
            if players[dude]['Networth'] < players[poorest_player]['Networth']:
                poorest_player = dude
        
        players[poorest_player]['Wallet'] += random_prop['rent']
        print("")
        print("")
        print("  {} paid {}$ to {}".format(player,random_prop['rent'],poorest_player))
        print("")
   
# Pay rent equal to the highest rent of your properties to the player with the lowest Networth
def curse_card_3(player):
    print("  Pay rent equal to the highest rent of your properties to the player with the lowest Networth in the game.")
    print("")
    print("")
    if len(players[player]['Property']) == 0: 
        print("  You don't have any property, meaning that this cards effect does not occour...")
        print("")
    else:
        highest_prop = None
        highest_amount = -1
        for prop in All_property_list:
            if prop['owner'] == player:
                if prop['rent'] > highest_amount:
                    highest_amount = prop['rent']
                    highest_prop = prop

        players[player]['Wallet'] -= highest_prop['rent']

        poorest_player = player
        for dude in playersorder:
            if players[dude]['Networth'] < players[poorest_player]['Networth']:
                poorest_player = dude
        
        players[poorest_player]['Wallet'] += highest_prop['rent']
        print("")
        print("")
        print("  {} paid {}$ to {}".format(player,highest_prop['rent'],poorest_player))
        print("")

# The player with the most most money invested in stocks has ONE (random) of their stocks turn phase 2
def curse_card_4(player):
    print("  The player with the most most money invested in stocks has ONE of their stocks change")
    print("  to a phase 2 stock.   Phase 2 rate:  ",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
    print("")
    who_has_most_val_stocks = player
    highest_stock_val = 0
    for player in playersorder:
        player_stock_val = 0
        for stock in players[player]['Stocks']:
            player_stock_val += stock['price']
        if player_stock_val > highest_stock_val:
            highest_stock_val = player_stock_val
            who_has_most_val_stocks = player

    if len(players[who_has_most_val_stocks]['Stocks']) > 0:
        stock_to_phase_2 = rn.choice(players[who_has_most_val_stocks]['Stocks'])
        stock_to_phase_2['phase'] = phase2
        stock_to_phase_2['phase_number'] = 2
        print("")
        print("  {} one of your stocks is now in phase 2 !".format(who_has_most_val_stocks , stock_to_phase_2['name'] ))
        print("")
    else:
        print("You don't have any stocks...")

#  Go to MayFair, and run landed_on()
def curse_card_5(player):
    print("")
    print("  Advance to MayFair! ")
    print("")
    white_space(3)
    players[player]['Placement'] = 35
    landed_on(player)

# Highest Networth pays to lowest Networth
def curse_card_6(player):
    print("  The player with the highest Networth pays their highest rent to the player with the")
    print("  lowest Networth in the game.")
    print("")
    print("")
    biggest_boss = player
    for dude in playersorder:
        if players[dude]['Networth'] > players[biggest_boss]['Networth']:
            biggest_boss = dude

    if len(players[biggest_boss]['Property']) == 0: 
        print("  The player with most Networth has no properties, meaning that this cards effect does not occour...")
        print("")
    else:
        highest_prop = None
        highest_amount = -1
        for prop in players[biggest_boss]['Property']:
            if prop['rent'] > highest_amount:
                highest_prop = prop

        players[biggest_boss]['Wallet'] -= highest_prop['rent']

        poorest_player = player
        for dude in playersorder:
            if players[dude]['Networth'] < players[poorest_player]['Networth']:
                poorest_player = dude
        
        players[poorest_player]['Wallet'] += highest_prop['rent']
        print("")
        print("  {} paid {}$ to {}".format(biggest_boss,highest_prop['rent'],poorest_player))
        print("")
   
# NOT USED (MAKE ME)
def curse_card_7(player):
    print("")
    print("  Everyone loses their Immunity! ")
    print("")
    for player in playersorder:
        players[player]['Immunity'] = 0


# Give your highest level unmortgaged property to the player with the lowest Networth
def curse_card_8(player):
    print("")
    print("  Give your highest level unmortgaged property to the player with the lowest Networth in the game.")
    print("")
    poorest_player = player
    for dude in playersorder:
        if players[dude]['Networth'] < players[poorest_player]['Networth']:
            poorest_player = dude
    
    highest_level = 0
    prop_dict = None
    for prop in players[player]['Property']:
        if prop['mortgaged'] == False:
            if prop['level'] > highest_level:
                highest_level = prop['level']
                prop_dict = prop
        
    if prop_dict == None:
        print("  You don't have any unmortgaged property to give away...")

    elif poorest_player == player:
        print("  You have the lowest Networth which means nothing happens.")
    
    else:    
        prop['owner'] = poorest_player
        players[poorest_player]['Property'].append(prop)
        players[player]['Property'].remove(prop)

# You are feeling generous. Give 300$ to each player
def curse_card_9(player):
    #print("treasure_card_7")
    print("  You are feeling generous. Give 300$ to each player IF and only if you have more than 1200$ on you.")
    print("")
    print("  Past wallet balance: {}$".format(int(players[player]['Wallet'])))
    if players[player]['Wallet'] > 1200:
        for dude in playersorder:
            players[player]['Wallet'] -= 300
            players[dude]['Wallet'] += 300
        print("")
        print("  You did something good. Good for you :) ")
        print("")
        print("  Wallet balance after payment: {}$".format(int(players[player]['Wallet'])))
    else:
        print("")
        print("  Seems like you're a cheapskate...")
        print("")

# The player with the most amount properties gives their best property to the poorest
def curse_card_10(player):
    print("  The player with the most amount properties gives their best property to the player with the")
    print("  lowest Networth in the game.")
    print("")
    print("")
    biggest_boss = player
    for dude in playersorder:
        if len(players[dude]['Property']) > len(players[biggest_boss]['Property']):
            biggest_boss = dude

    if len(players[biggest_boss]['Property']) == 0: 
        print("  Nobody has any properties, meaning that this cards effect does not occour...")
        print("")
    else:
        highest_prop = None
        highest_amount = -1
        for prop in players[biggest_boss]['Property']:
            if prop['price'] > highest_amount:
                highest_prop = prop

        poorest_player = player
        for dude in playersorder:
            if players[dude]['Networth'] < players[poorest_player]['Networth']:
                poorest_player = dude

        prop['owner'] = poorest_player
        players[biggest_boss]['Property'].remove(highest_prop)
        players[poorest_player]['Property'].append(highest_prop)
        
        ##########
        print("")
        print("  {} gives {} to {}".format(biggest_boss,highest_prop['name'],poorest_player))
        print("")
        # player with the highest networth gives two of their most expensive properties (defined by price) to the person with
        # the lowest networth. 

# All of your stocks change phase to phase 2 stocks (REAL BAD)
def curse_card_11(player):
    print("  All your stocks change phase to phase 2 stocks.")
    print("     Phase 2 rate: ",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
    print("")
    if len(players[player]['Stocks']) > 0:
        for stock in players[player]['Stocks']:
            stock['phase'] = phase2
            stock['phase_number'] = 2

# All of your stocks decrease with 50%
def curse_card_12(player):
    print("")
    print("  All of your stocks decrease with "+'50%'+" in value!!!")
    print("")
    if len(players[player]['Stocks']) > 0:
        for stock in players[player]['Stocks']:
            old_price = stock['price']
            stock['price'] = int(0.5 * stock['price'])
            if stock['price'] <= stock_minimum_value:
                stock['price'] = stock_minimum_value
            stock['price_history'].append(stock['price'])
            stock['percent_increase_pr_turn'] = round(stock['price']*100 / old_price  ,  1)


def curse_card_13(player):
    print("")
    print("  You are forced to sell a random property!")
    print("")
    prop = rn.choice(All_property_list)
    while prop['owner'] != player:
        prop = rn.choice(All_property_list)

    players[player]['Property'].remove(prop)
    prop['owner'] = None
    players[player]['Wallet'] += prop['price']
    print("")
    print("")
    print("   You sold {} for {}$ !".format(prop['name'] ,prop['price'] ))
    print("")


# All players sell their most expensive property,  or ALL property!
def curse_card_14(player):
    ran_num = rn.randint(1,5)
    print("")

    # All props... RESET
    if ran_num == 1: 
        
        print("  All players are forced to sell ALL of their property!!!")
        print("")
        for prop in All_property_list:
            owner = prop['owner'] 
            if owner != None:
                prop['owner'] = None
                players[owner]['Wallet'] += prop['price']
                players[owner]['Property'].remove(prop)
            else:
                continue

    # Most expensive prop 
    else:
        print("  All players are forced to sell their MOST expensive property!")
        print("")
        print("")
        for temp_player in playersorder:
            most_expensive_prop_name =''
            most_expensive_prop_dict = None
            most_expensive_price = 0
            for prop in All_property_list:
                if prop['owner'] == temp_player:
                    if prop['price'] > most_expensive_price:
                        most_expensive_price = prop['price']
                        most_expensive_prop = prop['name']
                        most_expensive_prop_dict = prop
            if most_expensive_prop_dict != None:
                most_expensive_prop_dict['owner'] = None
                players[temp_player]['Wallet'] += prop['price']
                players[temp_player]['Property'].remove(most_expensive_prop_dict)
                print(" {} sold {} for {}$".format(temp_player , most_expensive_prop, most_expensive_price))
            else:
                print(" {} doesn't own any property...".format(temp_player))
    print(" ")
    


cursed_cards = [curse_card_1,curse_card_2,curse_card_3,curse_card_4,curse_card_5,curse_card_6, curse_card_7,
                curse_card_8,curse_card_9, curse_card_10, curse_card_11, curse_card_12, curse_card_13,
                curse_card_14]


### Functions 

def clearscreen():
    for _ in range(20):
        print("")

def white_space(numba):
    for _ in range(numba):
        print("")

def load_game_pickle():
    # players[player]['Turn'] Incriments every turn a player has had. Then add the variable roundcount can determine 
    # whos turn it is, and be able to resume at the last known move. 
    # When loading a game, the game will work slightly hard coded to begin with, but as a new turn apears, 
    # the function will work just like the start_the_game() function does with an infinite loop.

    try:
        with open ("Saved_Games/load_monopoly_game_progress.pickle", 'rb') as file:
            pickle_dict = pickle.load(file)   
    except:
        print("")
        print("  No saved games could be found! ")
        print("  Please reload the game, and start a new game.")
        print("")
        exit()

    global players
    global playersorder
    global lottery_wallet
    global stocks_list
    global All_property_list
    global board_placement
    global max_prop_level
    global loaded_time_diff

    max_prop_level = pickle_dict['max_prop_level']
    players = pickle_dict['players']
    playersorder = pickle_dict['playersorder']
    lottery_wallet = pickle_dict['lottery_wallet']
    stocks_list = pickle_dict['stocks_list']
    All_property_list = pickle_dict['All_property_list']
    loaded_time_diff = pickle_dict['time_played'] 

    for tile in board_placement:
        if type(board_placement[tile]) == dict:
            temp_tile = board_placement[tile]
            for prop in All_property_list:
                if prop['name'] == temp_tile['name']:
                    board_placement[tile] = prop


    cur_round = 100000000      
    # Checking for what round and whos turn it is. 
    for player in playersorder:
        if players[player]['Turn'] < cur_round:
            cur_round = players[player]['Turn']

    # Executing special turn until normal rounds work.
    for player in playersorder:
        if players[player]['Turn'] > cur_round:
            continue
        else:
            one_turn(player)

    roundcount = cur_round + 1

    while roundcount < 10000:
        one_round(roundcount)
        roundcount += 1



def save_game_pickle():
    # Save game is run Every time a player ends his/her turn.
    # The save game file should be over written.
    # 
    # As far as it seems, it seems like the best idea to make a variable at the end of the script, which is a dictionary
    # of all the used dictionaries, lists, and variables. The key will be their variable name as a string.
    # 

    # MAKE A TEST VARIBLE HERE, SO IT DOESN'T OVERWRITE THE TEST FILE !
    global loaded_time_diff
    global time_diff
    
    time_diff = ( time.time() - start_time ) + loaded_time_diff
    
    pickle_dict = {'players':players , 'playersorder':playersorder , 'lottery_wallet':lottery_wallet , 
                'stocks_list':stocks_list , 'All_property_list':All_property_list , 'max_prop_level': max_prop_level
                , 'time_played' : time_diff}

    if os.path.exists("Saved_Games/load_monopoly_game_progress.pickle"):
        os.remove("Saved_Games/load_monopoly_game_progress.pickle")      # delete and replace.
    with open ("Saved_Games/load_monopoly_game_progress.pickle", 'wb') as file:
        pickle.dump(pickle_dict , file)


def start_the_game():
    # NOTE: ALWAYS RUN ME TO RUN THE REST OF THE SCRIPT! Just place 'start_the_game()' below the last code, if it isn't there already.
    clearscreen()
    print("")
    print("")
    print("")
    print("                                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    ")
    print("                                $$                             $$    ")
    print("                                $$       MONOPOLY REMADE       $$    ")
    print("                                $$                             $$    ")
    print("                                $$        First Edition        $$    ")
    print("                                $$                             $$    ")
    print("                                $$                             $$    ")
    print("                                $$       by Emil Haldan        $$    ")
    print("                                $$                             $$    ")
    print("                                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    ")
    print("")
    print("")
    print("")
    print("")
    print("               Welcome to Monopoly ! Do you want to make a new game, or resume your saved game?")
    print("")
    print("")
    print("")
    print("                     Type 1.  New Game")
    print("")
    print("                     Type 2.  Load Game")
    print("")
    white_space(10)
    numba = input("                Write the number here: ")
    #numba = None

    global loaded_time_diff
    loaded_time_diff = 0 

    if numba == '2':
        load_game_pickle()

    else:
        print("")
        print("              Quick rules:")
        print("              ")
        print("                 - Win by either making everyone else bankrupt, or gaining {} in Networth.".format(winning_condition_amount))
        print("                 - Buy Properties and Stocks to increase your Networth!")
        #print("                 - ")
        #print("                 - ")
        print("                  ")
        print("                  ")
        print("              ########################################################################")
        print("")
        print("                                  How many players are you ?:  ")
        print("")
        print("                                  Type the amount of players playing! ")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        player_amount = input()
        int(player_amount)      
        print("")    
        print("")
        print("                              ##############################")
        print("")
        print("                                  Type in your names:")
        print("")
        roundcount = 1
        for i in range(0, int(player_amount)):
            x = input()
            players[x] = {"Wallet": start_money, "Property": [], "Stocks": [] , "Luck": 0.5, "Placement": 0
            , 'Immunity': 0 , 'Lives':lives , 'Networth':start_money, 'Turn': roundcount }
            playersorder.append(x)
        
        white_space(6)
        while roundcount < 1000000:
            one_round(roundcount)
            roundcount += 1

def property_list_sorter(prop_list):
    temp = []
    for the_prop in All_property_list:
        for my_prop in prop_list:
            if my_prop == the_prop:
                temp.append(my_prop)
    return temp


def update_price():
    cur_round = 0
    for player in playersorder:
        if players[player]['Turn'] > cur_round:
            cur_round = players[player]['Turn']
    for prop in All_property_list:
        prop['price'] = int(round(prop['original_price'] + (cur_round*5) + prop['rent']*0.5 , -1 ))

def reset_prop_level():                # resets property levels for properties which are not owned by players.
    for prop in All_property_list:
        if prop['owner'] == None:
            prop['level'] = 1

def enough_money_to_buy(player,price):
    if players[player]['Wallet'] >= price:
        return True
    else:
        return False 


def landed_on(player):
    global lottery_wallet   
    cur_placement = board_placement[players[player]['Placement']]
    update_rent()
    broke_af(player)            # MAYBE HASH OUT....
    if am_i_dead(player):
        return
    if type(cur_placement) != str:  # Only properties have values in board_placement dict which are NOT strings.
        if cur_placement["owner"] == None:
            if enough_money_to_buy(player, cur_placement['price']):
                print("Do you wish to purchase", cur_placement['name'], "for ", cur_placement['price'], "$ ?")
                print("   Wallet:",players[player]['Wallet'],"$")
                print("")
                print("")
                print("If not, then an Auction will start.")
                print("")
                buy = input()
                if buy in yes_list:             # yes_list is a list of options to say "yes", Examples: yea, ye, y, *Enter*, and more...
                    cur_placement['owner'] = player                      # changing owner
                    players[player]['Property'].append(cur_placement)    # Adding property to owners list
                    players[player]['Wallet'] -= cur_placement['price']          
                    # BUY
                    white_space(2)
                    print("Add", cur_placement["name"], "to your hand.")
                    print("")
                    print("New Bank balance for {} : {}$".format(player ,int(players[player]['Wallet'])))
                    print("")
                    white_space(2)
                    #player_info(player)

                else:
                    start_auction(cur_placement)
                        
            else:
                print ("You're too poor to buy {} ... ".format(cur_placement['name']))
                print("You have : ", players[player]['Wallet'],"$")
                print("You need : ",  cur_placement['price'],"$")
                print("")
                input(" press Enter to continue to Auction...")
                start_auction(cur_placement)
            
        elif cur_placement["owner"] == player:
            if cur_placement['mortgaged']:
                print("")
                print("  Unfortunately this property is Mortgaged. Buy {} back for at the end turn menu".format(cur_placement['name']))
                print("  ")
                #print("  Current price: ", prop[''])
                print("")
                return

            # Upgade house by 1 level for free
            cur_placement['level'] += 1
            update_rent()
            players[player]['Wallet'] += int(cur_placement['rent']*0.2)
            print("")
            print("  {} upgraded +1 level and is now level {}!".format(cur_placement['name'],cur_placement['level']))
            print("  You also receive 20"+'%'+" of your rent for landing on your property")
            print("")
            print("  {}$ has been added to your Wallet.".format(int(cur_placement['rent']*0.2)))
            print("")
            print("")
            

        else:
        #Pay rent from player to owner

            if cur_placement['mortgaged']:
                print("")
                print("  {} owns this property BUT the property is mortgaged. Enjoy your stay for free.".format(cur_placement['owner']))
                print("")
                #input(" press Enter to continue...")
                return

            if players[cur_placement['owner']]['Placement'] == 'Jail' or players[cur_placement['owner']]['Placement'] == 'jail':
                print("")
                print("  {} owns this property BUT is currently in jail. Enjoy your stay for free.".format(cur_placement['owner']))
                print("")
                #input(" press Enter to continue...")
                return
            
            elif players[player]['Immunity'] > 0:
                players[player]['Immunity'] -= 1
                print("")
                print(" You're Immune to having to pay rent! You avoided paying {}$ !".format(cur_placement["rent"]))
                print(" You used one of your immunities on next rent! you have {} left.".format(players[player]['Immunity']))
                print("")
                #input(" press Enter to continue...")
                return

            else:
                players[cur_placement["owner"]]['Wallet'] += cur_placement["rent"]
                players[player]['Wallet'] -= cur_placement["rent"]
                print("")
                print(" You landed on {}'s property! Pay {}$ ".format(cur_placement['owner']  ,        
                        cur_placement['rent']))
                print("")
                cur_placement['level'] += 1
                #input(" press Enter to continue...")
                broke_af(player)

        
        
    else: 
        global bail_price
        global avg_networth

        if cur_placement == "Jail":
            bail_price = 200                # updated so that the previous bail price doesn't interfere.
            if bail_price < 0.1*players[player]['Networth']:
                bail_price = int(round(0.1*players[player]['Networth'] , -1))
            else:
                pass
                #bail_price = 200

            white_space(2)
            print(" You may either pay 10"+'%'+" of your Netwoth to get out of jail, or try to roll a double ")
            print(" with two 4-sided dice.")
            print(" You may not leave jail until one of the two options are fulfilled!")
            print(" You are NOT garenteed to leave jail after three rounds.")
            print("")
            print(" Type 1 to pay {}$ ".format(bail_price))
            print(" Type 2 to attempt to roll doubles")
            if players[player]['Immunity'] > 0: 
                print(" Type 3 to pay with 1 immunity")
            print("")
            print(" You have {}$ in your wallet.".format(players[player]['Wallet']))
            white_space(2)
            jail_choice = input()
            if jail_choice == '1' and players[player]['Wallet'] >= bail_price:
                # Pay some money to get to visit fail tile
                white_space(4)
                print(" You paid {}$ for a bail!".format(bail_price))
                print(" You're out of jail now! ")
                players[player]['Placement'] = 9            # placement 9 is the "visiting jail" tile.
                players[player]['Wallet'] -= bail_price
                lottery_wallet += bail_price

            elif jail_choice == '3' and players[player]['Immunity'] > 0 :
                # Pay some money to get to visit fail tile
                white_space(4)
                print(" You paid 1 Immunity for a bail!".format(bail_price))
                print(" You're out of jail now! ")
                players[player]['Placement'] = 9            # placement 9 is the "visiting jail" tile.
                players[player]['Immunity'] -= 1

            else:
                print("")
                dice_roll_ascii_art()
                input(" press Enter to roll the dice!")
                print("")
                print(" Rolling the dice!!! ")
                print("")
                print("")
                roll_1 = rn.randint(1, 4)
                roll_2 = rn.randint(1, 4)
                print(" You rolled : " , roll_1 , "and" , roll_2 )
                print("")
                if roll_1 == roll_2:
                    print(" You rolled doubles!")
                    print(" You're out of jail now! ")
                    print("")
                    #input(" press Enter to continue...")
                    players[player]['Placement'] = 9     # Visit jail tile.
                    
                else:
                    print(" You're still in jail :( ")
                    print("")
                    #input(" press Enter to continue...")
                
        
        elif cur_placement == "Free_park": 
            print(" ")
            white_space(15)
            print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("  $$                                             $$")
            print("  $$    CONGRATULATIONS! YOU WON THE LOTTERY!    $$")
            print("  $$             You won {:<24}$$".format(str(int(lottery_wallet))+'$')) # SPACING FIXED 00:32 2.Jul.19
            print("  $$                                             $$")
            print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("")
            white_space(13)
            #input("  Press Enter to continue ...")
            #white_space(10)
            players[player]['Wallet'] += lottery_wallet
            lottery_wallet = 0

            
            
        elif cur_placement == "Location_icon":
            #Options to do shit for 100$ or/and trade or stuff idk? 
            loc_price_rate = int((players[player]['Turn'])*5) + 200
            terror_fine =  int(players[player]['Networth']*0.05 - 200)
            if terror_fine < 300:
                terror_fine = 300

            if players[player]['Wallet'] > loc_price_rate + 300:
                players[player]['Wallet'] -= loc_price_rate
                lottery_wallet += loc_price_rate
                print("  ")
                white_space(4)
                print("  You landed on the Location Icon! Pay {}$ and choose a mandatory benefit".format(loc_price_rate))
                print("  ")
                print("  You have the following options and you can only choose ONE:")
                print("  ")
                print("               * Location Menu *")
                print("")
                print("          {}'s Wallet: {}$".format(player, players[player]['Wallet']))
                print("________________________________________________________________________")
                print("")
                print("1.  Travel to a destination                  cost: 0$ Extra ")
                print("2.  Hire a lawyer, and take a location       cost: 2*(Property price)$ Extra")
                print("3.  Buy 1x Immunity for the next rent        cost: 200$ Extra ")
                if players[player]['Turn'] > 10 and players[player]['Networth'] < avg_networth*0.8 :
                    print("4.  Bomb a property                          cost: You go to Jail +  {}$ fine".format(int(terror_fine)))
                print("")
                print("0.  Exit the menu                            cost: 0$ Extra")
                print("________________________________________________________________________")
                print("")
                print("")

                numba = option_number(player)
                numba += 1   # Cause numba become -1 of the typed number from option_number(player)
                white_space(2)
                if numba == 1:
                    # Travel to a destination
                    print(" Choose your desired location to travel to!")
                    print("")

                    for integer in board_placement:
                        # numbers 0:35 + 'jail' hence the if statement below.
                        if integer == 'jail':
                            continue
                        if integer == 18:  # Free park, aka. Jackpot.
                            continue
                        owner = ''    
                        for prop in All_property_list:
                            if prop['name'] == board_placement_names[integer]:
                                if prop['owner'] != None:
                                    owner = prop['owner']
                                    print("{:<3}  {:<25} colorset: {:<10}  level:{:<3}  rent:{:<4}$  owner:{:<15}  ".format(
                                        integer+1, board_placement_names[integer], prop['color'], prop['level'] ,
                                        prop['rent'] ,  owner ))
                                else:
                                     print("{:<3}  {:<25} colorset: {:<10}  price: {}$".format(
                                           integer+1, board_placement_names[integer], prop['color'], prop['price']))

                        #if owner == '':
                        #    print("{:<3}  {}".format(integer+1, board_placement_names[integer]))

                    print("")
                    print("0    If you changed your mind...")

                    white_space(2)
                    numba = option_number(player)

                    for enum,prop in enumerate(board_placement_names):
                        if numba == enum:
                            players[player]['Placement'] = enum
                            break

                    print("  Move your piece to {}! ".format(board_placement_names[numba]))
                    print("  ")
                    print("")
                    input("  press Enter to continue...")
                    landed_on(player)
                    
                elif numba == 2:
                    # Hire law firm
                    print("")
                    print("  You have hired a lawfirm to sue a player into getting one of their properties!")
                    print("")
                    print("  RULES: ")
                    print("  The price of the action is twice the price of the property if the price is greater than 300")
                    print("  Otherwise, the price of stealing the property is 300 + price of the property.")
                    print("  The person who lost their property will get 30"+'%'+" of the properties price as a.")
                    print("  compensation for this dirty white colar crime...")
                    white_space(3)
                    print("  {}'s Wallet :".format(player), int(players[player]['Wallet']))
                    print("")
                    print("  Choose your desired property to sue for!")
                    print("")
                    sue_price = 0
                    for enum,prop in enumerate(All_property_list):
                        if prop['owner'] == None or prop['owner'] == player:
                            continue
                        if prop['price'] < 300:
                            sue_price = 300 + prop['price']
                        else:
                            sue_price = 2*(prop['price'])

                        print(enum+1,"  {:<25}    cost of lawsuit {}$".format(prop['name'] , sue_price)) 
                    print("")
                    print("0    If you changed your mind...")

                    white_space(2)
                    numba = option_number(player)

                    for enum,prop in enumerate(All_property_list):
                        if prop['price'] < 300:
                            sue_price = 300 + prop['price']
                        else:
                            sue_price = 2*(prop['price'])
                        if enum == numba:
                            if enough_money_to_buy(player,sue_price):
                                old_owner = prop['owner']
                                prop['owner'] = player
                                players[old_owner]['Property'].remove(prop)
                                players[player]['Property'].append(prop)
                                players[player]['Wallet'] -= sue_price
                                players[old_owner]['Wallet'] += 0.3*prop['price']
                                break
                            else:
                                print("")
                                print("  You don't have enough money to do that!")
                                print("")
                    
                    pass
                elif numba == 3:
                    # Grant 1 immunity for a total of (200$)
                    players[player]['Wallet'] -= 200
                    players[player]['Immunity'] += 1

                elif numba == 4:
                    if players[player]['Networth'] < avg_networth*0.8:
                        # Do a drive by 
                        print("  Choose the target of your drive-by!")
                        print("  Remember, you get jail time and you have to pay a fine of 200$")
                        print("")
                        temp_input = input("  Press enter to continue...")
                        if temp_input in yes_list:

                            for integer in board_placement:
                                # numbers 0:35 + 'jail' hence the if statement below.
                                if integer == 'jail':
                                    continue
                                if integer == 18:  # Free park, aka. Jackpot.
                                    continue
                                owner = ''    
                                for prop in All_property_list:
                                    if prop['name'] == board_placement_names[integer]:
                                        if prop['owner'] != None:
                                            owner = prop['owner']
                                            print("{:<3}  {:<25} owner:{}".format(integer+1, board_placement_names[integer], owner ))
                                if owner == '':
                                    print("{:<3}  {:<25} ".format(integer+1, board_placement_names[integer]))

                            print("")
                            print("0    If you changed your mind...")

                            white_space(2)
                            numba = option_number(player)

                            players[player]['Placement'] = 'jail'
                            players[player]['Wallet'] -= ( roundcount * 7.5 + 200)

                            for enum,prop in enumerate(All_property_list):
                                if numba == enum:
                                    prop['level'] = prop['level'] // 2 
                                    break
                        else:
                            print("")
                            print("  Well done, you did the right thing...")
                            print("")
                    else:
                        not_enough_money_message()
                        

                else:
                    pass

            else:
                print("  You are too poor to buy use these benefits. You need {}$ more".format(int(loc_price_rate+300 - players[player]['Wallet'])))
                print("")
                print("  You need a surplus of 300$ in addition to the location rate at {}$ ".format(int(loc_price_rate)))
                print("  {}'s Wallet: {}$".format(player, int(players[player]['Wallet'])))
                print(" ")
            
            
        elif cur_placement == "Event":
            # Take a choice of Event cards, Chance, Extreme Chance, etc. 
            print("  You have landed on an Event tile and get to take a random card! ")
            chance_card_enroller(player)
            
        elif cur_placement == "Go_to_jail":
            fine = 100 * (players[player]['Turn']//8)
            players[player]['Placement'] = 'jail'
            players[player]['Wallet'] -= fine
            lottery_wallet += fine
            if players[player]['Turn'] >= 8:
                print("     Pay {}$ for committing crime.".format(fine))
            print("  You're going to jail and your turn ends now! ")
            print("  ")
            print("")
            print("            _____     _       _____  _____               ")
            print("           |_   _|   / \     |_   _||_   _|                ")
            print("             | |    / _ \      | |    | |                  ")
            print("         _   | |   / ___ \     | |    | |   _              ")
            print("        | |__' | _/ /   \ \_  _| |_  _| |__/ |             ")
            print("        `.____.'|____| |____||_____||________|             ")
            print("")                    
            print("")
            extraturn = False       # Prevents the player from actually taking another turn if the player goes to 
                                    # jail by landing on the "go to jail tile".
            #input(" press Enter to continue...")
            return extraturn
            
        else: 
            pass



###########################  STONKS  ##########################################

def stock_menu(player):
    print()
    white_space(4)
    print("                $ $ $ $ $ $$ $ $ $ $ $  ")
    print("              $ $ $ $ $ $ $$ $ $ $ $ $ $ ")
    print("             $ $                      $ $               ") 
    print("            $ $                        $ $") 
    print("           $ $      - STOCK MENU -      $ $ ")
    print("            $ $                        $ $                       PLAYER          : {}".format(player))
    print("             $ $                      $ $                        PHASE CHANGE IN : {} ROUNDS".format(phase_change_rounds - (players[player]['Turn']%phase_change_rounds)))
    print("              $ $ $ $ $ $ $$ $ $ $ $ $ $                         ROUND           : {} ".format(players[player]['Turn']))
    print("                $ $ $ $ $ $$ $ $ $ $ $                           DISTRIBUTION    : {}".format(stock_dist))
    print("")
    print("")
    if stock_dist == 'normal':
        print("                                                     Phase Rates :")
        print("                                                         phase 1 mean:",round((phase1_mean)*100, 1),"%  ,  phase 1 stdev:", round((phase1_std)*100, 1) , "%")
        print("                                                         phase 2 mean:",round((phase2_mean)*100, 1),"%  ,  phase 2 stdev:", round((phase2_std)*100, 1) , "%")
        print("                                                         phase 3 mean:",round((phase3_mean)*100, 1),"%  ,  phase 3 stdev:", round((phase3_std)*100, 1) , "%")
    else:
        print("                                                                 Phase Rates :")
        print("                                                                     phase 1 :",round((phase1_bound[0]-1)*100),"%  , ", round((phase1_bound[1]-1)*100) , "%")
        print("                                                                     phase 2 :",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
        print("                                                                     phase 3 :",round((phase3_bound[0]-1)*100),"%  , ", round((phase3_bound[1]-1)*100) , "%")
    print("")
    print("                                                    Stock Price Ceiling = {}$    Stock Price Floor = {}$ ".format(stock_max_value, stock_minimum_value) )
    print("                                                                    ")
    print("          {}'s Wallet: {}$".format(player , int(players[player]['Wallet'])))
    print()
    print("___________________________________________________________________")
    print("")
    print("")
    print("    1. Buy Stocks")
    print("    2. Sell Stocks ")
    print("")
    print("    0. or 'Enter' to Exit")
    print("")
    print("___________________________________________________________________")
    print("")
    white_space(5)
    numba = option_number(player)
    if numba == None or numba == -1:
        print(" You did nothing. ")
        return

    numba += 1

    if numba == 1:
        white_space(2)
        for enum,stock in enumerate(stocks_list):
            if stock['owner'] == None:
                print("{:<2}  {:<22}    price: {:<4}$   Increase this round: {:<5}    history: {}   ".format(enum+1 
                ,stock['name'] , stock['price'], str(round(stock['percent_increase_pr_turn'] - 100 ,1 ))+'%' , stock['price_history'] ))
        print("")
        print("0   Exit the menu")
        print("____________________________________________________________________________________")
        white_space(2)
        numba = option_number(player)
        if numba == None or numba == -1:
            print(" You did nothing. ")
            return stock_menu(player)

        elif enough_money_to_buy(player,stocks_list[numba]['price']):
            for enum,stock in enumerate(stocks_list):
                if enum == numba:
                    stock = stocks_list[enum]
                    stock['owner'] = player
                    players[player]['Wallet'] -= stock['price']
                    stock['bought_price'] = int(stock['price'])
                    players[player]['Stocks'].append(stock)
                    print("")
                    print("  You have purchased the {} for {}$ ".format(stock['name'],stock['price']))
                    print("")
            return stock_menu(player)

        else:
            print("  You are too poor to buy that stock. Try buying another one...")
            print("")
            return stock_menu(player)


    if numba == 2:
        if len(players[player]['Stocks']) == 0:
            print("")
            print("  You don't own any stocks...")
            print("")
            return stock_menu(player)
        white_space(2)
        for enum,stock in enumerate(stocks_list):
            if stock['owner'] == player:
                print("{:<2}  {:<22}  Bought Price: {:<4}$   Price: {:<4}$  Increase this round: {:<5}  History: {}   ".format(enum+1 
                ,stock['name'], stock['bought_price'] , stock['price'] , str(round(stock['percent_increase_pr_turn'] - 100 , 2 ))+'%' , stock['price_history'] ))

        print("")
        print("0   Exit the menu")
        print("____________________________________________________________________________________")
        white_space(2)
        numba = option_number(player)
        if numba == None or numba == -1:
            print(" You did nothing. ")
            return stock_menu(player)
        else:
            for enum,stock in enumerate(stocks_list):
                if enum == numba:
                    stock = stocks_list[enum]
                    stock['owner'] = None
                    players[player]['Wallet'] += stock['price']
                    players[player]['Stocks'].remove(stock)
                    print("")
                    print("  You have sold the {} for {}$.   profit:{}$".format(stock['name'],stock['price'], stock['price']-stock['bought_price'] ))
                    print("")
                    stock['bought_price'] = int(stock['price'])
                    input("  Press Enter to return to stock menu ...")

    return stock_menu(player)


def stock_update_every_round():
    # Updates the stock price depending on its "phase"
    # if stock price < lowerbound: 
    #   stock price = lowerbound
    # Have the phase in the dictionary of the stock
    # if stock reaches var(stock_max_value) in stock['price']


    for stock in stocks_list:
        if len(stock['price_history']) >= 8 :
            stock['price_history'] = stock['price_history'][-5:]

        if stock_dist == "normal":

            phase1 = round(rn.normalvariate(phase1_mean , phase1_std) ,3)         # random float with a 3 decimal place
            phase2 = round(rn.normalvariate(phase2_mean , phase2_std) ,3)
            phase3 = round(rn.normalvariate(phase3_mean , phase3_std) ,3)
        else:    # Note:  if stock_dist == "uniform":
            phase1 = round(rn.uniform(phase1_bound[0],phase1_bound[1]) , 3)         # random float with a 3 decimal place
            phase2 = round(rn.uniform(phase2_bound[0],phase2_bound[1]) , 3)
            phase3 = round(rn.uniform(phase3_bound[0],phase3_bound[1]) , 3)

        # print("phase1_mean:", phase1_mean)
        # print("phase2_mean:", phase2_mean)
        # print("phase3_mean:", phase3_mean)
        # print("")
        # print("phase1_std:", phase1_std)
        # print("phase2_std:", phase2_std)
        # print("phase3_std:", phase3_std)
        # print("")

        if stock['phase_number'] == 1:
            stock['phase'] = phase1
        if stock['phase_number'] == 2:
            stock['phase'] = phase2
        if stock['phase_number'] == 3:
            stock['phase'] = phase3

        # print("stock['phase']:", stock['phase'])

        old_price = stock['price']

        if stock['price'] < bound_for_volatile_stocks:
            stock['price'] *= (stock['phase']**1.2)
        else:
            stock['price'] *= stock['phase']

        stock['price'] = int(stock['price'])

        # print("old_price: ", old_price)
        # print("stock['price']", stock['price'])

        if stock['price'] < stock_minimum_value:
            stock['price'] = int(stock_minimum_value)
            
        elif stock['price'] > stock_max_value:
            stock['price'] = int(stock_drop_to_value)
        
        stock['price_history'].append(int(stock['price']))
        stock['percent_increase_in_value'] = round(stock['price']*100 /stock['bought_price']  ,  1)
        stock['percent_increase_pr_turn'] = round(stock['price']*100 / old_price  ,  1)



def stock_phase_change():

    for stock in stocks_list:
        phase1 = round(rn.uniform(phase1_bound[0],phase1_bound[1]) , 2)
        phase2 = round(rn.uniform(phase2_bound[0],phase2_bound[1]) , 2)
        phase3 = round(rn.uniform(phase3_bound[0],phase3_bound[1]) , 2)
        phase_choice = rn.randint(1,3)
        if phase_choice == 1:
            stock['phase'] = phase1
            stock['phase_number'] = 1
        elif phase_choice == 2:
            stock['phase'] = phase2
            stock['phase_number'] = 2
        elif phase_choice == 3:
            stock['phase'] = phase3
            stock['phase_number'] = 3
        stock['price_history'] = []

    #stock_update_every_round() # STONKS update once more during a phase_change

    # This call is placed in the start of every round too...
    print("")
    print("###################################### STOCKS ##########################################################")
    print("")
    print("     $ $ $  PHASE CHANGE ! $ $ $")
    print("")
    print("     The stocks are now chaning their phase. They may each have one of three phases. ")
    print("")
    print("")
    if stock_dist == 'normal':
        print("                                Phase Rates :")
        print("                                   phase 1 mean:",round((phase1_mean)*100, 1),"%  ,  phase 1 stdev:", round((phase1_std)*100, 1) , "%")
        print("                                   phase 2 mean:",round((phase2_mean)*100, 1),"%  ,  phase 2 stdev:", round((phase2_std)*100, 1) , "%")
        print("                                   phase 3 mean:",round((phase3_mean)*100, 1),"%  ,  phase 3 stdev:", round((phase3_std)*100, 1) , "%")
    else:
        print("                                Phase Rates :")
        print("                                   phase 1 :",round((phase1_bound[0]-1)*100),"%  , ", round((phase1_bound[1]-1)*100) , "%")
        print("                                   phase 2 :",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
        print("                                   phase 3 :",round((phase3_bound[0]-1)*100),"%  , ", round((phase3_bound[1]-1)*100) , "%")
    print("")
    print("     All stocks will increase in price within the boundries of one of the phases!")
    print("     KEEP AN EYE ON THE YOUR STOCKS PRICE HISTORY!")
    print("")
    print("    Tips for new people: ")
    print("        ")
    print("         1. Stocks take a random value decscribed above, and increase/decrease the price with some percent.")
    print("         2. Stocks that reach up to {}$ will crash down to {}$!".format(stock_max_value,stock_drop_to_value))
    print("         3. The stock price ceiling is {}$ and the stock price floor is {}$".format(stock_max_value , int(stock_minimum_value)))
    print("")
    print("")
    print("###################################### STOCKS ##########################################################")
    print("")
    print("")
    print("")
    print("")
    input("   Press 'Enter' to continue ...")
    white_space(3)
    #print("   Here are some usefull stock stats:")
    #for stock in stocks_list:
    #    stock
        

 

# Stocks Variables and Dictionaries

phase1_mean = (phase1_bound[0]+phase1_bound[1])/2    + 0.01  # 0.01 is just to spicy shit up.
phase2_mean = (phase2_bound[0]+phase2_bound[1])/2    - 0.01  # 0.01 is just to spicy shit up.
phase3_mean = (phase3_bound[0]+phase3_bound[1])/2    + 0.02  # 0.02 is just to spicy shit up.
phase1_std = (phase1_mean - phase1_bound[0])/ 1.7       # 1.7 is an abritrary multiplier to determine std.
phase2_std = (phase2_mean - phase2_bound[0])/ 1.7
phase3_std = (phase3_mean - phase3_bound[0])/ 1.7

phase1 = round(rn.uniform(phase1_bound[0],phase1_bound[1]) , 2)
phase2 = round(rn.uniform(phase2_bound[0],phase2_bound[1]) , 2)
phase3 = round(rn.uniform(phase3_bound[0],phase3_bound[1]) , 2)

phase_list = [phase1,phase2,phase3]

                                                                                                                                                                            
the_monopoly_stock = {'name':'The Monopoly stock' ,'price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None ,'price_history' : [], 'percent_increase_pr_round':0}
meat_industry_stock = {'name':'Meat Industry stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value':1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
bank_stock = {'name':'Bank stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value':1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0} 
tech_stock = {'name':'Tech stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value':1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0} 
clothes_stock = {'name':'Clothes stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
jewellery_store_stock = {'name':'Jewellery store stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
sports_stock = {'name':'Sports stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
food_chain_stock = {'name':'Food Chain stock','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
gold = {'name':'Gold Commodity','price': stock_start_value , 'phase': phase1 , 'phase_number':1 ,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
silver = {'name':'Silver Commodity','price': stock_start_value , 'phase': phase1 , 'phase_number':1 ,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
platinum = {'name':'Platinum Commodity','price': stock_start_value , 'phase': phase1 , 'phase_number':1 ,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
oil = {'name':'Oil Commodity','price': stock_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stock_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}


stocks_list = [the_monopoly_stock, meat_industry_stock, bank_stock,tech_stock, clothes_stock, jewellery_store_stock
                ,sports_stock, gold,silver,platinum, oil, food_chain_stock ]

#stocks_list = [the_monopoly_stock, bank_stock, jewellery_store_stock, gold, oil, food_chain_stock ]



###########################  STONKS  ##########################################

def remove_one_imunity_from_player(cur_rounds):
    players["player"]['Immunity_on_next_rent'] -= 1  
            
        
def roll_except():
    try:
        global roll_1
        global roll_2
        global roll
        print("")
        print("")
        print(" Try again and put your numbers like this")
        print(" ")
        print(" The below example shows how the numbers have to be typed in.")
        print("")
        print(" Example:2 6")
        print("")
        print("")
        string_roll = input(" Enter your dice roll!: ")
        string_roll = string_roll.split(' ')
        roll_1 = int(string_roll[0])
        roll_2 = int(string_roll[1])
        if roll_2 > 6 or roll_1 > 6:
            return roll_except()
        roll = roll_1 + roll_2
        print("")
        print(" You rolled : " , roll_1 , "and" , roll_2 )
        
        return roll,roll_1,roll_2
    except:
        return roll_except()


def dice_roll(player,turns):
    global lottery_wallet
    broke_af(player)
    if players[player]['Placement'] == 'jail':
        return
    if am_i_dead(player):
        return
    cur_turns = turns
    extraturn = False
    print("")
    dice_roll_ascii_art()
    if real_life_dice:
        print("")
        #print(" Type in your roll as two integers with a space inbetween")
        print("")
        string_roll = input(" Enter your dice roll!: ")
        print("")
        print("")

        roll, roll_1, roll_2 = roll_except()

    else:
        if turns > 1:
            print("")
            print("    You rolled doubles last time !")
            print("")
        print("")
        input(" press Enter to roll the dice!")
        print("")
        print(" Rolling the dice!!! ")
        print("")
        print("")
        roll_1 = rn.randint(1, dice_size)
        roll_2 = rn.randint(1, dice_size)        
        roll = roll_1 + roll_2
        print("")
        print(" You rolled : " , roll_1 , "and" , roll_2 )
    
    white_space(8)

    if roll_1 == roll_2:
        if cur_turns == 3: 
            # GO TO JAIL!
            fine = 100 * (players[player]['Turn']//8)
            print("  Oh no! You rolled doubles three times in a row.")
            print("  Pay a {}$ fine for the crime you have committed.".format(fine))
            print("  You are now placed in jail and your turn is over.")
            players[player]['Placement'] = 'jail'
            lottery_wallet += fine
            players[player]['Wallet'] -= fine

            return None
        else:
            extraturn=True
        cur_turns += 1

    if type(board_placement_names[players[player]['Placement']]) == str:
        print(" Move your brick {} steps and end at :       {}     {}  ".format(roll ,
         (board_placement_names[(players[player]['Placement'] + int(roll)) % 36]), 
         (players[player]['Placement'] + int(roll)) % 36) )

    else:
        print(" Move your brick to your destination. ")
    
    print("")
    white_space(10)
    print(" Continue when you have moved your brick. ")
    players[player]['Placement'] += int(roll)
    if players[player]['Placement'] >= 36:
        players[player]['Placement'] = players[player]['Placement'] % 36
        players[player]['Wallet'] += pass_go_cash
        white_space(2)

        print("                ")
        print("                 _____         _____ _____        _____ _______       _____ _______     _               ")
        print("                |  __ \ /\    / ____/ ____|      / ____|__   __|/\   |  __ \__   __|   | |        ")
        print("                | |__) /  \  | (___| (___       | (___    | |  /  \  | |__) | | |      | |        ")
        print("                |  ___/ /\ \  \___ \ ___ \       \___ \   | | / /\ \ |  _  /  | |      | |       ")
        print("                | |  / ____ \ ____) |___)        ____) |  | |/ ____ \| | \ \  | |      |_|      ")
        print("                |_| /_/    \_\_____/_____/      |_____/   |_/_/    \_\_|  \_\ |_|      (_)         ")
        print("")
        print(" {} passed START and collects {}$ to their wallet!".format(player,pass_go_cash))
        white_space(2)

    # note: Maybe include this section! 
    if players[player]['Placement'] != 'jail':
        if players[player]['Placement'] != 9:
            input(" Press Enter to continue...")
    white_space(4)
    
    landed_on(player)
    
    if extraturn == True:
        dice_roll(player,cur_turns)
        

def dice_roll_ascii_art():
    print("                                                    _______                 ")
    print("                                                   /\ o o o\                 ")
    print("                                                  /o \ o o o\_______                 ")
    print("                                                 <    >------>   o /|                 ")
    print("                                                  \ o/  o   /_____/o|                 ")
    print("                                                   \/______/     |oo|                 ")
    print("                                                         |   o   |o/                 ")
    print("                                                         |_______|/                 ")


def player_info(player):
    update_rent()
    broke_af(player)
    global loaded_time_diff
    global time_diff

    time_diff = ( time.time() - start_time ) + loaded_time_diff
    if am_i_dead(player):
        return
    print("")
    print("                     {:<35}       ".format(player + "'s Stuff"))
    print("")
    print(" #----------------------------------------------------------------------# ")
    print("    Round : {}                    Time played: {} hours  {} min  {} sec".format(players[player]['Turn'],
                int(time_diff//3600) , int((time_diff//60)%60) , int(time_diff%60 )))
    print("    {}'s Wallet      : ".format(player), int(players[player]['Wallet']) , '$')
    print("    {}'s Networth    : ".format(player), int(players[player]['Networth']) , '$                                     Winning Condition : {} $'.format(winning_condition_amount))
    if type(board_placement[players[player]['Placement']]) == str:
        name_loc = board_placement[players[player]['Placement']]
    else: 
        name_loc = board_placement[players[player]['Placement']]['name']
    cur_place = [name_loc , "  tile number:", players[player]['Placement']]
    print("    {}'s Placement   : ".format(player), cur_place[0],cur_place[1],cur_place[2])
    if players[player]['Immunity'] > 0:
        print("    {}'s Immunity    : ".format(player) , players[player]['Immunity'] )
    
    print("")
    print("    __________ {}'s Property __________  amount:({}/22)    ".format(player,len(players[player]['Property'])))
    print("")

    #This line calls a function which sorts the properties, cheapest to highest.
    players[player]['Property'] = property_list_sorter(players[player]['Property'])

    for prop in players[player]['Property']:
        mort_info = 'Active'
        if prop['mortgaged']:
            mort_info = 'Mortgaged'

        print("      {:<25}".format(prop['name']) + ":"," Price: {:<5}$".format(int(prop['price'])) ,  
        " Level: {:<2}/ {}".format(prop['level'], max_prop_level), "  Rent: {:<5}$".format(prop['rent'])
        , "  Side: {:<6}".format(prop['side']), "  Status: {:<10}".format(mort_info) 
        , " Colorset: {:<10}".format(prop['color'])) 

    print("")
    print("    __________  {}'s Stocks  __________  amount:({}/{})  ".format(player ,len(players[player]['Stocks']) , len(stocks_list )))
    print("")
    for stock in players[player]['Stocks']:
        print("   {:<23}:  Price: {:<4}$  Bought Price: {:<4}$  Profit: {:<6} IPR: {:<5}    history: {}".format( stock['name'] ,
        stock['price']  , stock['bought_price'], str(int(stock['price'] - stock['bought_price']))+'$' , str(round(stock['percent_increase_pr_turn'] - 100 ,1 ))+'%'  , stock['price_history']  ))
    print("")
    print(" #----------------------------------------------------------------------# ")
    
# The below line is for reference of the structure of a house. 
# {"name": "Old Kent Road" , "price": 60, "original_price":60 , "rent":20, "level" : 1 , "owner": None,
#            "side": "South", "mortgaged":False , "color" : "Brown"} 

chace_card_turn_counter = 0

def end_turn_menu(player):
    if am_i_dead(player) == False:
        global end_turn_menu_used
        global chace_card_turn_counter
        white_space(1)
        card_price = 150 + players[player]['Turn']*5
        if card_price > 350:
            card_price = 350

        print("       # # # # # End of Turn Menu # # # # #                            PLAYER:  {}".format(player))
        print("")
        print("          {}'s Wallet: {}$".format(player,int(players[player]['Wallet'])))
        print("")
        print("___________________________________________________________________")
        print("")
        print("  1. Mortgage/un-mortgage property")
        print("  2. Trade with player ")
        print("  3. Upgrade property")
        if len(playersorder) > 1:
            #if (players[player]['Turn'] + playersorder.index(player)) % len(playersorder) == 0:
            if (players[player]['Turn'] + playersorder.index(player)) % 2 == 0:                         # testing this option out.
                print("  4. Buy a Chance or Treasure (50% / 50%) card  for",card_price,"$")
                print("  5. Buy or sell Stocks")

                #brown_owned, grey_owned, pink_owned, orange_owned, red_owned, yellow_owned, green_owned, blue_owned = 0,0,0,0,0,0,0,0 
                #for prop in players[player]['Property']:

        else:
            print(" ")
        print("")
        print("  0. or 'Enter' to Exit")
        print("")
        print("___________________________________________________________________")
        white_space(2)
        option = input("  Type which option you wish to do: ")
        white_space(4)
        exit_list = ['0','0.','',' ']
        if option in exit_list:
            return end_turn_menu_used

        elif option == '1' or option == '1.':
            print("")
            print("  Do you wish to mortgage or un-mortgage some properties?")
            print("")
            print("")
            print("  Type 1 to Mortgage properties")
            print("")
            print("  Type 2 to Un-Mortgage properties")
            print("")
            print("")
            choice = input("")
            if choice == '1':
                mortgage_menu(player)
            elif choice == '2':
                un_mortgage_menu(player)
            else:
                pass
            
        elif option == '2' or option == '2.':
            trade_menu(player)
        elif option == '3' or option == '3.':
            # Upgrade property levels
            upgrade_menu(player)

        elif option == '4' or option == '4.':
            # 4. Buy a Chance,Cursed, or Treasure card 
            if chace_card_turn_counter == 1:   
                white_space(3)
                print("  You already bought a card this turn!")
                white_space(3)
                
            elif enough_money_to_buy(player,card_price):
                if (players[player]['Turn'] + playersorder.index(player)) % 2 == 0:
                    chace_card_turn_counter += 1
                    players[player]['Wallet'] -= card_price
                    chance_card_enroller(player,treasure_only=True)
                else:
                    print("  You can't buy a Card this turn.")
                    
                
            else:
                not_enough_money_message()
                

            pass
        elif option == '5' or option == '5.':
            if (players[player]['Turn'] + playersorder.index(player)) % 2 == 0:
                stock_menu(player)
            else:
                print("  You can't buy or sell stocks this turn ....")
        else:
            pass
        
        end_turn_menu_used = True
        end_turn_menu(player)
    
    else:
        return


def not_enough_money_message():
    white_space(5)
    print("   You don't have enough money to do that $ $ $  :( ")
    white_space(5)

def one_turn(player):
    global chace_card_turn_counter

    #for i in range(7):
    #    drag_all_levels_by_1()
    #    bump_all_levels_by_1()

    winning_condition(player)
    print("")
    white_space(8)
    print("  #################################   ")
    print("  ###                           ###  ")
    print("  ###                           ###  ")
    print("  ###                           ###  ")
    print("  ###                           ###  ")
    print("  ###     {:<17}     ### ".format(player+"'s Turn!"))
    print("  ###                           ###  ")
    print("  ###                           ###  ")
    print("  ###                           ###  ")
    print("  ###                           ###  ")
    print("  #################################   ")
    print("")
    white_space(5)
    # who has highest Networth?
    lowest_networth = player
    lowest_networth_amount = players[player]['Networth'] 
    for dude in playersorder:
        if players[player]['Networth'] > players[dude]['Networth']:
            lowest_networth = dude
            lowest_networth_amount = players[dude]['Networth']

    if len(playersorder) == 2 and players[player]['Placement'] != 'jail':
        if random_card and (players[player]['Turn'] + playersorder.index(player)) % len(playersorder) == 0 and  player == lowest_networth:
            flip_coin = rn.randint(1,2)
            if flip_coin == 1:
                print("    WOOOHOOO, FREE STUFF!!!")
                print("")
                print("    {} !! Take a FREE Chance, or Treasure card because you have the lowest Networth in the game!".format(player))
                print("  ")
                print("  ")
                print("             Turn: {}".format(player))
                print("  ")
                print("  ")
                chance_card_enroller(player,treasure_only=True)
                print("")
                input("  press Enter to continue...")

    elif len(playersorder) > 2 and players[player]['Placement'] != 'jail':
        if random_card  and  player == lowest_networth and (players[player]['Turn'] + playersorder.index(player)) % len(playersorder) == 0:
            print("    WOOOHOOO, FREE STUFF!!!")
            print("")
            print("    {} !! Take a FREE Chance, or Treasure card because you have the lowest Networth in the game!".format(player))
            print("  ")
            print("  ")
            print("             Turn: {}".format(player))
            print("  ")
            print("  ")
            chance_card_enroller(player, treasure_only=True)
            print("")
            input("  press Enter to continue...")
    
    white_space(18)
    player_info(player)
    
    print("")
    if players[player]['Placement'] != 'jail':
        dice_roll(player,1)
    else:
        landed_on(player)
    white_space(5)
    input("  press Enter to continue...")
    player_info(player)
    print("")
    if players[player]['Placement'] != 'jail':
        winning_condition(player)
        global end_turn_menu_used
        end_turn_menu_used = False
        end_turn_menu(player)
        if end_turn_menu_used:
            player_info(player)
            input("  Press Enter to end your turn! ")

    winning_condition(player)
    players[player]['Turn'] += 1
    chace_card_turn_counter = 0
    save_game_pickle()      # Saves game automatically.
    white_space(35)



def am_i_dead(player): 
    if players[player]['Lives'] == 0:
        return True
    elif players[player]['Lives'] > 0:
        return False    


def sell_property(player, prop):
    if prop['mortgaged'] == False:
        players[player]['Wallet'] += (prop['price'])
        prop['owner'] = None
        players[player]['Property'].remove(prop)

    else:
        prop['mortgaged'] = False
        players[player]['Wallet'] += (prop['price']*0.5)
        prop['owner'] = None
        players[player]['Property'].remove(prop)

    print("  {} has now been sold for {}".format(prop['name'], prop['price']/2))



def sell_prop_menu(player):
    print("")
    print("")
    if players[player]['Lives'] == 0:
        return

    if len(players[player]['Property']) > 0:
            white_space(3)
            print("  You have some properties you can mortgage. Here are your options.")
            print("")
            print("               $$ Sell Property Menu $$")
            print("")
            print("  Wallet balance: ", players[player]['Wallet'])
            print("________________________________________________________________________")
            print("")
            for enum,prop in enumerate(players[player]['Property']): 
                if prop['mortgaged'] == False:
                    print(enum+1 , " {:<25} sell for   :".format(prop['name']), prop['price'] , "$" )
                else:
                    print(enum+1 , " {:<25} sell for   :".format(prop['name']), prop['price']*0.5 , "$" )
                    
            print("")
            print("0  Exit the menu")
            print("")
            print("________________________________________________________________________")
            print("")
            print("")
            print("  Write the number of the property you want to mortgage below.")
            print("")
            print("")

            numba = option_number(player)

            if numba == -1:
                broke_af(player)

            for enum,prop in enumerate(players[player]['Property']): 
                if numba  == enum:
                    sell_property(player, prop)
        
    if players[player]['Wallet'] < 0 :
        if len(players[player]['Property']) == 0:
            return
        else:    
            sell_prop_menu(player)

    else:
        print("")
        print("  Wallet balance for {}: ".format(player), players[player]['Wallet'])
        print("")


def upgrade_menu(player):
    # slightly hardcoded to make upgrades cost the price of the place. 
    upgrade_multiplier = 0.5

    if players[player]['Lives'] == 0:
        return

    non_mortg_props = 0
    for prop in players[player]['Property']:
        if prop['mortgaged'] == False:
            non_mortg_props += 1

    if non_mortg_props == 0:
        print("")
        print("  You don't any active properties.")
        print("")
        return

    if len(players[player]['Property']) > 0:
            white_space(3)
            print("  You have some properties you can upgrade. Here are your options.")
            print("")
            print("               $$ Level Upgrade Menu $$")
            print("")
            print("  Max Property Level: ", max_prop_level )
            print("  Wallet balance: ", players[player]['Wallet'])
            print("________________________________________________________________________")
            print("")
            for enum,prop in enumerate(players[player]['Property']): 
                if prop['mortgaged'] == False:
                    print("{:<2} {:<25} {:<10} upgrade price: {:<4}$     current level: {:<2}     rent: {:<4}$".format(enum+1 ,prop['name'], prop['color'],
                                                            int(prop['price']*upgrade_multiplier), prop['level'], prop['rent'])  )
                else:
                    continue

            print("")
            print("0   Exit the menu")
            print("")
            print("________________________________________________________________________")
            print("")
            print("")
            print("  Write the number of the property you want to upgrade below.")
            print("")
            print("")

            numba = option_number(player)

            if numba == None or numba == -1:
                return

            for enum,prop in enumerate(players[player]['Property']): 
                if numba  == enum:
                    if prop['level'] == max_prop_level:
                        white_space(4)
                        print("  That property is alreaddy in the current max level!")
                        white_space(4)

                    elif enough_money_to_buy(player,prop['price']*upgrade_multiplier):
                        prop['level'] += 1
                        players[player]['Wallet'] -= prop['price']*upgrade_multiplier
                        update_rent()
                        white_space(10)
                        print("  {} has now been upgraded to level {} for {}".format(prop['name'], prop['level'], prop['price']*upgrade_multiplier))
                        white_space(5)
                    else:
                        not_enough_money_message()
    
    update_rent()
    upgrade_menu(player)


def mortgage_menu(player):

    if players[player]['Lives'] == 0:
        return

    mortg_left = 0
    for prop in players[player]['Property']:
        if prop['mortgaged'] == False:
            mortg_left += 1

    if mortg_left == 0:
        print("")
        print("  You don't have anymore property to morgage.")
        print("")
        return

    if len(players[player]['Property']) > 0:
            white_space(3)
            print("  You have some properties you can mortgage. Here are your options.")
            print("")
            print("               $$ Mortgage Menu $$")
            print("")
            print("  Wallet balance: ", players[player]['Wallet'])
            print("________________________________________________________________________")
            print("")
            for enum,prop in enumerate(players[player]['Property']): 
                if prop['mortgaged'] == False:
                    print(enum+1 , " {:<25} mortgage for   :".format(prop['name']), int(prop['price']*0.5) , "$" )
                else:
                    continue

            print("")
            print("0  Exit the menu")
            print("")
            print("________________________________________________________________________")
            print("")
            print("")
            print("  Write the number of the property you want to morgage below.")
            print("")
            print("")

            numba = option_number(player)

            if numba == None or numba == -1:
                return

            for enum,prop in enumerate(players[player]['Property']): 
                if numba  == enum:
                    mortgage_property(player, prop)
                    print("  {} has now been morgaged for {}".format(prop['name'], prop['price']/2))
        
    #if players[player]['Wallet'] < 0 :
    while players[player]['Wallet'] < 0 :
        mortg_sum = 0
        for prop in players[player]['Property']:   # Checks if the player has anything to morgage anymore.
            if prop['mortgaged'] == False:
                mortg_sum += 1
            else:
                continue
        
        if mortg_sum == 0:
            return
        else:    
            mortgage_menu(player)
    mortgage_menu(player)

    #print("")
    #print("  Wallet balance for {}: ".format(player), players[player]['Wallet'])
    #print("")


def un_mortgage_menu(player):
    mortg_left = 0
    for prop in players[player]['Property']:
        if prop['mortgaged'] == True:
            mortg_left += 1

    if mortg_left == 0:
        print("")
        print("  You don't have anymore property to un-mortgage.")
        print("")
        return

    if len(players[player]['Property']) > 0:
            white_space(3)
            print("  You have some properties you can buy back. Here are your options.")
            print("")
            print("")
            print("  Wallet balance: ", players[player]['Wallet'])
            print("________________________________________________________________________")
            print("")
            for enum,prop in enumerate(players[player]['Property']): 
                if prop['mortgaged'] == True:
                    print(enum+1 , " {:<25} buy back for   :".format(prop['name']), int(prop['price']*(0.5+0.1)) , "$" )
                else:
                    continue
                    
            print("")
            print("0  Exit the menu")
            print("")
            print("________________________________________________________________________")
            print("")
            print("")
            print("  Write the number of the property you want to morgage below.")
            print("")

            numba = option_number(player)

            if numba == None or numba == -1:
                return

            for enum,prop in enumerate(players[player]['Property']): 
                if numba == enum:
                    un_mortgage_property(player, prop)
            
            un_mortgage_menu(player)


def broke_af(player):

    if players[player]['Networth'] < 0 & players[player]['Lives'] == 2 & redepemtion_reward:
        players[player]['Wallet'] = start_money
        print("     {}'s lives left: ".format(player) , players[player]['Lives'])
        print("                                                   ______________________________________________________________________ ")
        print("     You hit rock bottom ...                      |                                                                      |    ")
        print("                                                  | ==================================================================== |    ")
        print("                                                  | |%/^\\%&%&%&%&%&%&%&%&{ Federal Reserve Note }%&%&%&%&%&%&%&%&//^\% | |    ")
        print("                                                  | |/inn\)===============------------------------===============(/inn\| |    ")
        print("                                                  | |\|UU/      $ $ $ MONEY THAT MEANS NOTHING AT ALL $ $ $       \|UU/| |    ")
        print("                                                  | |&\-/     ~~~~~~~~   ~~~~~~~~~~=====~~~~~~~~~~~  P8188928246   \-/&| |      ")
        print("     Redeption you now have 1                     | |%//)  ___ ___   ___   ____    ___   ____   ___   _      __ __ (\\% | |    ")
        print("     life left                                    | |&(/  |   |   | /   \ |    \  /   \ |    \ /   \ | |    |  |   |\)&| |    ")
        print("                                                  | |%\\   | _   _ ||     ||  _  ||     ||  o  )     || |    |  |   |//%| |    ")
        print("                                                  | |&\\\  |  \_/  ||  O  ||  |  ||  O  ||   _/|  O  || |___ |  ~   |//&| |    ")
        print("                                                  | |%\\)  |   |   ||     ||  |  ||     ||  |  |     ||     ||___,  |//%| |    ")
        print("                                                  | |&))/ |   |   ||     ||  |  ||     ||  |  |     ||     ||     /\((&| |    ")
        print("                                                  | |%//) |___|___| \___/ |__|__| \___/ |__|   \___/ |_____||____/  (\\%| |    ")
        print("     Good luck...                                 | |&//      R265402524K                    series: 36F234739       \\&| |    ")
        print("                                                  | |%/>  13                     _\\___//_    1932              13   <\%| |    ")
        print("                                                  | |&/^\    Treasurer  $______{Emil Haldan}_______$  Secretary    /^\&| |    ")
        print("                                                  | |/inn\                ))--------------------((                /inn\| |    ")
        print("                                                  | |)|UU(================/ ONE THOUSAND DOLLARS \================)|UU(| |    ")
        print("                                                  | |{===}%&%&%&%&%&%&%&%&%a%a%a%a%a%a%a%a%a%a%a%a%&%&%&%&%&%&%&%&{===}| |    ")
        print("                                                  | ==================================================================== |    ")
        print("                                                  |______________________________________________________________________|    ")    
        input("  Pres Enter to continue ... ")
        white_space(3)




    if players[player]['Wallet'] < 0:
        white_space(10)
        update_rent()
        while players[player]['Networth'] > 0 and players[player]['Wallet'] < 0:
            update_rent()
            player_stock_val = 0
            player_mortg_val = 0
            player_sell_val = 0

            for stock in players[player]['Stocks']:
                player_stock_val += stock['price']
            for prop in players[player]['Property']:
                if prop['mortgaged']:
                    player_sell_val += ( prop['price'] / 2)
                else:
                    player_mortg_val += ( prop['price'] / 2)
                    player_sell_val += ( prop['price'] )

            print("")
            print("")
            print("       # # # # # Broke Menu # # # # #")
            print("")
            print("")
            print("          You need to sell/mortgage some of your stuff!")
            print("          {}'s Wallet: {}$".format(player,players[player]['Wallet']))
            print("")
            print("___________________________________________________________________")
            print("")
            print("  1. Mortgage Property        value: {}".format(player_mortg_val))
            print("  2. Sell Property            value: {}".format(player_sell_val))
            print("  3. Sell Stocks              value: {}".format(player_stock_val))
            print("")
            print("  0. or 'Enter' to Exit")
            print("")
            print("___________________________________________________________________")
            white_space(3)
            numba = option_number(player)

            if numba == None or numba == -1:
                continue

            if type(numba) != int:
                continue

            numba += 1

            if numba == 1:
                mortgage_menu(player)

            elif numba == 2:
                sell_prop_menu(player)

            elif numba == 3:
                stock_menu(player)
                    
            
        white_space(3)
        if players[player]['Wallet'] > 0:
            return

        else:
            players[player]['Lives'] -= 1

        if players[player]['Lives'] == 0:
            # MAKE ME PRETTIER WITH ASCII ART !!!    
            white_space(15)        
            print("     ")
            print("     ")
            print("     {}'s lives left: ".format(player) , players[player]['Lives'])
            print("     {}'s Wallet: ".format(player) , players[player]['Wallet'],'$')
            print("     {}'s Networth: ".format(player) , players[player]['Networth'],'$')
            print("     ")
            print("")
            print("    You LOST and you are now out of the game because you're broke. ")
            white_space(15)
            print("     ")
            del playersorder[playersorder.index(player)]
            for prop in All_property_list:
                if prop['owner'] == player:
                    prop['owner'] = None
                    prop['mortgaged'] = False
            # CHANGE ALL OWNED PROPERTY TO "owner": None.

            input("  Pres Enter to continue ... ")
            return         
            

        elif players[player]['Lives'] == 1 & redepemtion_reward:
            players[player]['Wallet'] = 1000
            print("     {}'s lives left: ".format(player) , players[player]['Lives'])
            print("                                                   ______________________________________________________________________ ")
            print("     You hit rock bottom ...                      |                                                                      |    ")
            print("                                                  | ==================================================================== |    ")
            print("     You have lost one life, and                  | |%/^\\%&%&%&%&%&%&%&%&{ Federal Reserve Note }%&%&%&%&%&%&%&%&//^\% | |    ")
            print("     you are on your final life.                  | |/inn\)===============------------------------===============(/inn\| |    ")
            print("                                                  | |\|UU/      $ $ $ MONEY THAT MEANS NOTHING AT ALL $ $ $       \|UU/| |    ")
            print("     All your property has been                   | |&\-/     ~~~~~~~~   ~~~~~~~~~~=====~~~~~~~~~~~  P8188928246   \-/&| |      ")
            print("     paid for and her is 1000$                    | |%//)  ___ ___   ___   ____    ___   ____   ___   _      __ __ (\\% | |    ")
            print("     for you to go survive on.                    | |&(/  |   |   | /   \ |    \  /   \ |    \ /   \ | |    |  |   |\)&| |    ")
            print("     Place your brick back to start.              | |%\\   | _   _ ||     ||  _  ||     ||  o  )     || |    |  |   |//%| |    ")
            print("                                                  | |&\\\  |  \_/  ||  O  ||  |  ||  O  ||   _/|  O  || |___ |  ~   |//&| |    ")
            print("                                                  | |%\\)  |   |   ||     ||  |  ||     ||  |  |     ||     ||___,  |//%| |    ")
            print("                                                  | |&))/ |   |   ||     ||  |  ||     ||  |  |     ||     ||     /\((&| |    ")
            print("                                                  | |%//) |___|___| \___/ |__|__| \___/ |__|   \___/ |_____||____/  (\\%| |    ")
            print("     Good luck...                                 | |&//      R265402524K                    series: 36F234739       \\&| |    ")
            print("                                                  | |%/>  13                     _\\___//_    1932              13   <\%| |    ")
            print("                                                  | |&/^\    Treasurer  $______{Emil Haldan}_______$  Secretary    /^\&| |    ")
            print("                                                  | |/inn\                ))--------------------((                /inn\| |    ")
            print("                                                  | |)|UU(================/ ONE THOUSAND DOLLARS \================)|UU(| |    ")
            print("                                                  | |{===}%&%&%&%&%&%&%&%&%a%a%a%a%a%a%a%a%a%a%a%a%&%&%&%&%&%&%&%&{===}| |    ")
            print("                                                  | ==================================================================== |    ")
            print("                                                  |______________________________________________________________________|    ")    
            input("  Pres Enter to continue ... ")
            white_space(3)

    else:
        pass


def one_round(roundcount):
    global lottery_wallet
    print("")
    white_space(6)
    print("                             $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $                           ")
    print("                            $                               $")
    print("                            $      START OF NEW ROUND       $")
    print("                            $                               $")
    print("                             $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ ")
    print("")
    print("")
    print("")
    print("                              It is round # ", roundcount)
    white_space(10)
    #decay_function_for_test(200)

    #

    white_space(10)
    if roundcount%10 == 0:
        global max_prop_level
        max_prop_level += 1
        print("  ")
        print("  All property levels may increase up to level {} now!".format(max_prop_level))
        print("")
        input("  Press 'Enter' to continue...")
    white_space(4)

    if roundcount % 10 == 5 and roundcount >= 15:
        print(" ")
        chance_card_8(playersorder[0])
        print("")
        print(" This is scheduled to happend every 10 rounds!")
        print(" Inflation levels are: 15,25,35,45,...")
        print("")


    lottery_wallet += 50

    if roundcount % phase_change_rounds == 0:
        stock_phase_change()
    stock_update_every_round()
    
    for player in playersorder:
        one_turn(player)
        winning_condition(player)


def mortgage_property(player, prop):
    if prop['mortgaged'] == False:
        players[player]['Wallet'] += (prop['price']/2)
        prop['mortgaged'] = True
    # Changing rent to 0 for mortgaged property is done in the top of the update_rent() function.


def un_mortgage_property(player, prop):
    if prop['mortgaged'] == True:
        players[player]['Wallet'] -= (prop['price']/2  +  prop['price']*0.1)     # 10% extra for the bank.
        prop['mortgaged'] = False
        
        
def start_auction(prop):
    white_space(16)
    print(" # # # # # # # # # # # # #                        ___________          ")
    print("                                                  \         /             ")
    print("     AUCTION TIME !!!                              )_______(                          ")
    print('                                                   |"""""""|_.-._,.---------.,_.-._               ')
    print(" # # # # # # # # # # # # #                         |       | | |               | | ''-.     ")           
    print("                                                   |       |_| |_             _| |_..-'       ")
    print("                                                   |_______| '-' `'---------'` '-'         ")
    print('                                                   )"""""""(         ')
    print("                                                  /_________\         ")
    print("                                                  `'-------'`          ")
    print("                                                .-------------.           ")
    print("                                               /_______________\           ")
    print("  RULES:")
    print("  ")
    print("  The auction is done verbally between the players, and using a stopwatch on a smart phone")
    print("  which is placed at the center of the table for convenience. By starting the timer, the auction begins...")
    print("  To 'bid', one must press the 'lap' key on the timer, to do a new lap.")

    print("  These laps must be less than 7 seconds! ")
    print("  Once a lap passes 7 seconds, the stopwatch can be put stopped, and the last person to bid has won!")
    print("")
    print("  When you press enter, the auction will start, and the initial asking price is 20$ !")
    print("  Bids must be increment with atleast 20$ pr. time.")
    print("  ")
    print("  When the Auction is done, the computer will ask for the person who won, and how much that ")
    print("  person bid for the property.")
    white_space(5)
    for person in playersorder:
        print("   {}'s Wallet: {}   ".format(person,players[person]['Wallet']))
    white_space(5)
    input("  Pres Enter to continue ... ")

    # The auction starts in 3 , 2 , 1 , GO !
    # 7 Second while loop 1 sec interval:
    #    while ( 1 sec - time) > 0: 
    #       If current_time > 1 sec:
    #          break(inner while loop)
    #       https://stackoverflow.com/questions/15528939/python-3-timed-input  TIMED INPUT ALGO
    #      


    white_space(5)
    print("  Out of the people below, type the name of the person who won the auction.")
    print("")
    for enum,person in enumerate(playersorder):
        print(" {}  ".format(enum+1),person)
    print("")
    player = playersorder[0]
    numba = option_number(player)

    winner_of_auction = None
    for enum,person in enumerate(playersorder):
        if enum == numba:
            winner_of_auction = person

    try:
        for x in playersorder:
            if winner_of_auction == x:
                players[winner_of_auction]['Property'].append(prop)
                prop['owner'] = winner_of_auction
            else:
                continue       
    except KeyError:
        print("Try typing in the persons name again, just as it is displayed above...")
        winner_of_auction = input()
        players[winner_of_auction]['Property'].append(prop)
        prop['owner']
    print("")
    print("")
    print("How much did the person bid for the property? ")
    how_much = input()

    #if eval(how_much) == None:
    #    how_much = prop['price']/2
    if how_much == '':
        how_much = prop['price']/2
    elif how_much == ' ':
        how_much = prop['price']/2
    
    try:
        players[winner_of_auction]['Wallet'] -= int(how_much)
    except ValueError:
        print("Try typing in the money again, plain as a number, such as: 320 ")
        how_much = input()
        if eval(how_much) == None:
            how_much = prop['price']/2
        elif eval(how_much) == '':
            how_much = prop['price']/2
        elif eval(how_much) == ' ':
            how_much = prop['price']/2
        players[winner_of_auction]['Wallet'] -= int(how_much)
    print("")
    print(" {} won the auction of {} for {}$".format(winner_of_auction , prop['name'] , int(how_much)))
    print("")


def update_networth():
    global avg_networth
    avg_networth = 0 
    temp_networth = 0

    for player in playersorder:
        players[player]['Wallet'] = int(players[player]['Wallet'])
        temp_networth = players[player]['Wallet']

        for prop in players[player]['Property']:
            if prop['mortgaged'] == False:
                temp_networth += prop['price']
            else:
                temp_networth += ( prop['price'] / 2 )

        for stock in players[player]['Stocks']:
            temp_networth += stock['price']
        
        players[player]['Networth'] = temp_networth
        avg_networth += temp_networth
    
    avg_networth = avg_networth / len(playersorder)


def update_rent(): 
    # The rent has been customized but is made to fit the template of the original game
    # Data taken from www.falstad.com/monopoly.html
    # The array has coulmns as "ratio change from an increase in level", and 
    # the rows are South, East, North and West.
    # Example, Row 0 coulmn 0 represents the percentage change in rent from level 1 to 2, on the South side.
    # Example, Row 2 coulmn 3 represents the percentage change in rent from level 4 to 5, on the North side.
    # IF the levels excede 5, then the rate shall be constant for all types of properties.

    reset_prop_level()
    update_networth()       # update networth for players, it will be called again below.

    for player in playersorder:
        winning_condition(player)
    #mortgaged_rent = 0 

    level_1_rates = [20,20, 30,30,40, 50,50,60, 70,70,80, 90,90,100, 110,110,120, 130,130,150, 175,200]
    level_1_rates = [40,40, 50,50,60, 80,80,90, 95,95,100, 115,115,125, 130,130,140, 170,170,180, 190,200]

    
    rates_profile = np.array([[3,2.5,1.6,1.38],[2.8,2.43,1.37,1.25],[2.6,2.55,1.23,1.19],[2.4,2.27,1.20,1.16]])
    #rates_profile_ORIGINAL = np.array([[3,3,1.6,1.38],[3,2.83,1.37,1.25],[3,2.55,1.23,1.19],[3,2.27,1.20,1.16]])

    # Decreased at higher properties for fair play.
    #rates_profile = np.array([[3,3,1.6,1.38],[3,2.63,1.37,1.25],[3,2.35,1.23,1.19],[3,2.05,1.20,1.16]])

    rates = rates_profile

    for enum,prop in enumerate(All_property_list):
        side_of_map = prop['side']
        cur_level = prop['level']
        levels_past5 = 0
        levels_past1 = 0
        multiplier = 1

        if prop['level'] > max_prop_level:          # The upper level bound 
            prop['level'] = max_prop_level

        if prop['level'] < 1:               # The lower level bound
            prop['level'] = 1

        # if prop['mortgaged']:
        #     prop['rent'] = mortgaged_rent
        #     continue

        if side_of_map == 'South':
            if cur_level >= 6: 
                for x in rates[0,:]:
                    multiplier *= x
                levels_past5 = prop['level'] - 5

            elif cur_level == 1:
                # Do literally nothing since multiplier is already at 1 ...
                pass
            
            else:
                levels_past1 = prop['level'] - 1
                for index in range(levels_past1):
                    multiplier *= rates[0,index]

        elif side_of_map == 'West':
            if cur_level >= 6: 
                for x in rates[1,:]:
                    multiplier *= x
                levels_past5 = prop['level'] - 5

            elif cur_level == 1:
                # Do literally nothing since multiplier is already at 1 ...
                pass
            
            else:
                levels_past1 = prop['level'] - 1
                for index in range(levels_past1):
                    multiplier *= rates[1,index]

        elif side_of_map == 'North':
            if cur_level >= 6: 
                for x in rates[2,:]:
                    multiplier *= x
                levels_past5 = prop['level'] - 5

            elif cur_level == 1:
                # Do literally nothing since multiplier is already at 1 ...
                pass
            
            else:
                levels_past1 = prop['level'] - 1
                for index in range(levels_past1):
                    multiplier *= rates[2,index]

        elif side_of_map == 'East':
            if cur_level >= 6: 
                for x in rates[3,:]:
                    multiplier *= x
                levels_past5 = prop['level'] - 5

            elif cur_level == 1:
                # Do literally nothing since multiplier is already at 1 ...
                pass
            
            else:
                levels_past1 = prop['level'] - 1
                for index in range(levels_past1):
                    multiplier *= rates[3,index]

        if levels_past5 > 0:
            for numba in range(levels_past5):
                multiplier *= 1.15

        # COLOR SET BONUS!
        # Checking if player has all colors in color set. If so, increase rent by 30% !
        total_props_in_set = 0
        props_owned_in_set = 0
        for other_prop in All_property_list:
            if other_prop['color'] == prop['color']:
                total_props_in_set += 1
                if other_prop['mortgaged'] == False:
                    if other_prop['owner'] == player: 
                        props_owned_in_set += 1
        

        if total_props_in_set == props_owned_in_set:
            multiplier *= 1.3       # 30% increase if you have all the tiles!

        prop['rent'] = int(round(level_1_rates[enum] * multiplier , -1))

                       # 15% increase each time the place levels up beyond level 5.

    update_price()
    update_networth()


def bump_all_levels_by_1():
    for prop in All_property_list:
        prop['level'] += 1 

def drag_all_levels_by_1():
    for prop in All_property_list:
        prop['level'] -= 1 

def option_number(player,exit_menu = True):
        numba = input("Write the number here: ")
        if exit_menu:
            if numba == '0' or numba == '0.' or numba == '' or numba == ' ' or numba == None:
                numba = -1
                return numba
        try:
            numba = int(numba)
            numba -= 1
            return int(numba)
        except:
            print("  Please write a stand-alone number. You wrote:", numba)
            return option_number(player)
                

def trade_menu(player):
    white_space(5)
    print("  You have some options of people you may trade with. Here are your options.")
    print("")
    print("________________________________________________________________________")
    print("")
    for enum,receiver in enumerate(playersorder):
        if receiver != player:
            print(enum+1, " ",receiver)
    print("")
    print("0  Exit the menu")
    print("")
    print("________________________________________________________________________")
    print("")
    print("")
    print("  Write the number of the player you want to trade with.")
    print("")

    numba = option_number(player)

    for enum,receiver in enumerate(playersorder):
        if playersorder.index(receiver) == numba:
            trade_player = receiver
            receiver = trade_player
            break
    
    white_space(5)
    print("  Before you continue to the below section, both parties need to agree to a trade involving property and/or money.")
    print("  All properrty keep their upgrades, unless a color set is split, which destroys the bought upgrade.")
    print("")
    print("")

    # Give properties to receiver
    print("  Property options to give to {} from {}:".format(receiver , player ))
    print("")
    print("________________________________________________________________________")
    print("")
    for enum,prop in enumerate(players[player]['Property']): 
        print(enum+1 , " {:<25} Price:".format(prop['name']) , prop['price'] , "$" )           
    print("")
    print("0  Don't give any property to {}".format(receiver))
    print("")
    print("________________________________________________________________________")
    print("")
    print("")
    print("  Write the number of the property {} wants to give to {}".format(player , receiver ))
    print("")

    numba = option_number(player)

    for enum,prop in enumerate(players[player]['Property']): 
        if numba  == enum:
            prop['owner'] = receiver
            players[receiver]['Property'].append(prop)
            players[player]['Property'].remove(prop)

    print("")
    #input("  Press 'Enter' to continue to the properties {} can give to {}".format(receiver,player))
    print("")

    # Give properties to player
    print("  Property options to give to {} from {}:".format(player , receiver ))
    print("")
    print("________________________________________________________________________")
    print("")
    for enum,prop in enumerate(players[receiver]['Property']): 
        print(enum+1 , " {:<25} Price:".format(prop['name']) , prop['price'] , "$" )         
    print("")
    print("0  Don't give any property to {}".format(player))
    print("")
    print("________________________________________________________________________")
    print("")
    print("")
    print("  Write the number of the property {} wants to give to {}".format(receiver , player ))
    print("")
    
    numba = option_number(player)

    for enum,prop in enumerate(players[receiver]['Property']): 
        if numba  == enum:
            prop['owner'] = player
            players[receiver]['Property'].remove(prop)
            players[player]['Property'].append(prop)
    
    print("")
    #input("  Press 'Enter' to continue to exchange money")
    print("")

    # Exchange money with eachother
    print("")
    print("  {}'s wallet : ".format(player), players[player]['Wallet'])
    print("  {}'s wallet : ".format(receiver), players[receiver]['Wallet'])
    print("")
    print("")
    print("  Write the senders name, a 'space', then the receivers name, and then the amount of money being sent.")
    print("  format example: 'Player1 Player2 1000' , Player1 will give Player2 1000$ .")
    print("")
    print("  To skip this section press Enter")
    print("")
    
    def type_except(player):
        trade = input()
        if trade == '' or trade == ' ':
            return
        try:
            trade = trade.split(' ')
            money_giver = trade[0]
            money_receiver = trade[1]
            money_amount = int(trade[2])
            players[money_giver]['Wallet'] -= money_amount
            players[money_receiver]['Wallet'] += money_amount
        except:
            print(" You have written the wrong format, try again.")
            type_except(player)

    type_except(player)
    

def chance_card_enroller(player, treasure_only=False):
    
    # This section has been modified so that Chance and Treasure occour just a frequent.
    # In the final release chance cards are twice more likely to occour than other cards. 
    update_rent() # just sprinkling the boi.

    list_of_choices = ["chance_cards", "chance_cards", "treasure_cards" , "cursed_cards"] 
    if treasure_only:
        list_of_choices = ["chance_cards", "treasure_cards" ]


    card_pick = rn.choice(list_of_choices)
    #print(" THIS IS chance_treasure_int: ", chance_treasure_int)

    if card_pick == "chance_cards":
        list_of_choice = chance_cards
        print("                  You got a CHANCE card!")
        print("")
        print("                                                                                      ________             ")
        print("                                                                                   _jgN########Ngg_             ")
        print("                                                                                 _N##N@@/    \9NN##Np_             ")
        print("                  Player: {:<25}                             d###P            N####p             ".format(player))
        print("                                                                                \??/              T####             ")
        print("                                                                                                  d###P             ")
        print("                                                                                               _g###@F             ")
        print("                                                                                            _gN##@P             ")
        print("                                                                                          gN###F'             ")
        print("                                                                                         d###F             ")
        print("                                                                                        0###F             ")
        print("                                                                                        0###F             ")
        print("                                                                                        0###F             ")
        print("                                                                                        'NN@'             ")
        print("                                                                                                           ")
        print("                                                                                         ___             ")
        print("                                                                                        q###r             ")
        print("                                                                                         ???             ")


    elif card_pick == "treasure_cards":
        list_of_choice = treasure_cards
        print("                You got a TREASURE card!")
        print("")
        print("                                                                                         _.--.                      ")
        print("                                                                                     _.-'_:-'||                      ")
        print("                                                                                 _.-'_.-::::'||                      ")
        print("               Player: {:<25}                            _.-:'_.-::::::'  ||                      ".format(player))
        print("                                                                          .'`-.-:::::::'     ||                      ")
        print("                                                                         /.'`;|:::::::'      ||_                      ")
        print("                                                                        ||   ||::::::'     _.;._'-._                      ")
        print("                                                                        ||   ||:::::'  _.-!oo @.!-._'-.                      ")
        print("                                                                        \|   ||:::::.-!()oo @!()@.-'_.|                      ")
        print("                                                                         '.'-;|:.-'.&$@.& ()$%-'o.'\ ||                      ")
        print("                                                                           '>'-.!@%()@'@_%-'_.-o _.|'||                      ")
        print("                                                                            ||-._'-.@.-'_.-' _.-o  |'||                      ")
        print("                                                                            ||=[ '-._.-\ /.-'    o |'||                      ")
        print("                                                                            || '-.]=|| |'|      o  |'||                      ")
        print("                                                                            ||      || |'|        _| ';                      ")
        print("                                                                            ||      || |'|    _.-'_.-'                      ")
        print("                                                                            |'-._   || |'|_.-'_.-'                      ")
        print("                                                                             '-._'-.|| |' `_.-'                      ")
        print("                                                                                 '-.||_/.-'                      ")


    elif card_pick == "cursed_cards":
        print("                  You got a CURSED card!")
        print("                                                                                        _,.-------.,_                      ")
        print("                                                                                    ,;~'             '~;,                      ")
        print("                                                                                  ,;                     ;,                      ")
        print("                                                                                 ;       CURSED CARD       ;                      ")
        print("                  Player: {:<25}                            ,;                           ;,                      ".format(player))
        print("                                                                               ; ;      .           .      ; ;                      ")
        print("                                                                               | ;   ______       ______   ; |                      ")
        print('                                                                               |  `/~"     ~" . "~     "~\ " |           ')
        print("                                                                               |  ~  ,-~~~^~, | ,~^~~~-,  ~  |                      ")
        print("                                                                                |   |        }:{        |   |                      ")
        print("                                                                                |   l       / | \       !   |                      ")
        print('                                                                                .~  (__,.--" .^. "--.,__)  ~.           ')
        print("                                                                                |     ---;' / | \ `;---     |                      ")
        print("                                                                                 \__.       \/^\/       .__/                      ")
        print("                                                                                  V| \                 / |V                      ")
        print("                                                                                   | |T~\___!___!___/~T| |                      ")
        print("                                                                                   | |`IIII_I_I_I_IIII'| |                      ")
        print("                                                                                   |  \,III I I I III,/  |                      ")
        print("                                                                                    \   `~~~~~~~~~~'    /                      ")
        print("                                                                                      \   .       .   /                           ")
        print("                                                                                        \.    ^    ./                      ")
        print("                                                                                          ^~~~^~~~^                      ")
        print("")


        list_of_choice = cursed_cards

    #input("  Press 'Enter' to pick your card...")
    white_space(1)
    card_int = rn.randint(0, len(list_of_choice)-1 )
    #print(" THIS IS card_int : ", card_int)
    list_of_choice[card_int](player)                     # Calling the function.

    update_rent() # just sprinkling the boi.

    white_space(3)
    #input("  Press 'Enter' to continue...")


    # Random chose a list (Chance or Treasure)
    # Randomly chose a Chance/Treasure card from the list.
    # Display which of the sets were chosen, and after display the card that was given.
    # Call the function for that chance/treasure card, and continue to next turn.
    

def display_all_prop():
    for prop in All_property_list:
        #if prop['owner'] != None:
        print(prop)  


def winning_condition(player):
    if players[player]['Networth'] > winning_condition_amount:
        you_win(player)
    if len(playersorder) == 1:
        you_win(player)


def you_win(player):
    print("")
    # AAAAY, Some one wins the game with some amount of a money and property!
    # Display some stats of how amazing this guy was and how long it took him and so on.
    # Make some ASCII Baloons or someshit idk.
    white_space(30)
    print("")
    print("     __      __   ______   __    __        __       __   ______   __    __        __  __  __   ")
    print("    |  \    /  \ /      \ |  \  |  \      |  \  _  |  \ /      \ |  \  |  \      |  \|  \|  \  ")
    print("     \$$\  /  $$|  $$$$$$\| $$  | $$      | $$ / \ | $$|  $$$$$$\| $$\ | $$      | $$| $$| $$   ")
    print("      \$$\/  $$ | $$  | $$| $$  | $$      | $$/  $\| $$| $$  | $$| $$$\| $$      | $$| $$| $$   ")
    print("       \$$  $$  | $$  | $$| $$  | $$      | $$  $$$\ $$| $$  | $$| $$$$\ $$      | $$| $$| $$  ")
    print("        \$$$$   | $$  | $$| $$  | $$      | $$ $$\$$\$$| $$  | $$| $$\$$ $$       \$$ \$$ \$$   ")
    print("        | $$    | $$__/ $$| $$__/ $$      | $$$$  \$$$$| $$__/ $$| $$ \$$$$       __  __  __   ")
    print("        | $$     \$$    $$ \$$    $$      | $$$    \$$$ \$$    $$| $$  \$$$      |  \|  \|  \  ")
    print("         \$$      \$$$$$$   \$$$$$$        \$$      \$$  \$$$$$$  \$$   \$$       \$$ \$$ \$$  ")
    print("")
    white_space(8)
    print("     ", player, "won the game !!!")
    print("")
    print("     Round    : ",players[player]['Turn'])
    print("     Networth : ",players[player]['Networth'],"$")
    print("")
    print("")
    print("      THANK YOU FOR PLAYING!  ")
    print("")
    print("")
    white_space(4)
    exit()

def decay_function_for_test(numba):
    print("")
    print("")
    print(" DECAY FUNCTION ACTIVE. Each play looses 200$ pr round.")
    print("")
    print("")
    for player in playersorder:
        players[player]['Wallet'] -= numba
        



"""
TO-DO list of functionality:

- Curse, Chance, Treasure, change phase rates to make sense for normies.
- Check buy stock. Couldn't buy stock for 454 even though i had 460. 


 

- Polish up start menu
- Update Auction to actually WORK on the PC! 
- Make the reward for owning all props of a colorset, into something unique and usefull. 
    Ideas: 
    ### When having all three cards collected, one can buy the store set on the road. 
    # Find the stores on google maps when typing in the road.
    # That store or place will act as a beacon for a powerup, such as: 

    Power ups ____________________________________ #:
        Any         : Move +2 each time you roll
        Brown1      : A market place, possibly giving income, or something? idk
        Brown2      : A Gallery which gains income
        Teal        : 3 shops (Mc D, Nandos, Pizza)
        Pink1       : (cigs): Poison such as chance of leach at beginning of turn? 
        Pink 2&3    : (Hotel): Rent is increased by 50% on that colorset.
        Yellow      :
        Dark Blue   : Diamond shop or something (add money each turn), 


    Name of shop ____________________________________ #:
        Brown1: KFC (google maps)
        Brown2: Whitechapel Gallery (googel maps)
        Teal 1: idk
        Teal 2: Nandos, Pizza express, or Mc Donalds.
        Teal 3: Junk food again.
        Pink 1: Cigerette producer  
        Pink 2: Women of WWII monument (maybe not)
        Pink 3: Hotel
        Orange1:
        Orange2:
        Orange3:
        Yellow1: Covent garden (some flower market)
        Yellow2: Central London School
        Yellow3: 
        Green1 :
        Green2 :
        Green3 :
        Blue1  :
        Blue2  :

-    



Implimentated list:
- Add amount of props to player info.
- Reward for owning all colors in a set (30% increased rent)
- Add visualisation for passing GO!
- Impliment pickling each round, and being able to load the game from that round. 
- Add bonus for having a color set.
- Stocks implimented and working 
- Selling properties to the bank.
- Add Networth winning condition
- Travelling (location icon)
- Add lottery to FREE PARK!
- Create some cursed cards, bringing bad news for people.
- The properties level influence the price of the house. Build a function and call it in update rent.
- Chance cards added and implimented.
- Trade money and property now with a dummy proof UI.
- Mortgages and un-mortgage
- Going to and out of jail 
- Buying property
- Property level and rent 
- Turns and rounds 
- Player profile and wallet 
- Wallet limit
- Extra life & kick when you die default: 2 lives
- Choice of Real and system dice
- Immunity from rent system implimented.
- Add payment to lottery_wallet when paying for bail out of jail.
- Bail is equal to 10% of the current persons Networth, and bail should be unavailable if it isn't there as cash!
- Hire a law firm and pay them ( prop['price'] + (prop['rent']/5) ) to steal a card. The card keeps its level.

- Stocks Ideas (Implimented):
        There are three stocks in the game. They can each have one of the behaviors.
        These behaviors change every 5 rounds.
        1. has an expected value which is greater than 1         E(X) = 1.1 pr. turn
        2. has an expected value which is a little less than 1   E(X) = 0.95 pr. turn
        3. has an expected value which is sligtly greater than 1             E(X) = 1.02 pr. turn
        These three attributes shift every 5 turns, and nobody knows what is what, just like IRL.
        Do this with a uniform distribution of +-0.2 from the expected value.
        Stock_minimum value = start_value




BUGS: 


Fixed:
    (FIXED) - Don't let players in Jail get a chance card, even if they're the poorest.
    (FIXED) - cant exit sell menu if broke -_-
    (FIXED)- Fix price history with stocks when loading in a game.
    (FIXED) - Remove Free park from Location icon
    (FIXED) - Change the random chance card to happen if and only if it is the poorest players turn. 
    (FIXED) - When mortgaging properties, a recursive loop happens, forcing the player to press enter multiple times, equal to the amount of properties morgaged whilst in that menu.





"""


start_the_game()
