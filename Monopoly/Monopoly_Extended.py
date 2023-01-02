# Imports 
import random as rn
import time
import pickle
import numpy as np
import os
import winsound


### Global Variables and Configurations

players = {}
playersorder = []
yes_list = ['yes', 'yea', 'yup', 'y', '', ' ', 'ye']
start_time = time.time()

pass_go_cash = 300                                                  # DEFAULT: pass_go_cash = 200
start_money = 4000                                                  # DEFAULT: start_money = 3000
avg_networth = start_money
winning_condition_amount = 30000                                    # DEFAULT: winning_condition = 25000
max_prop_level = 5                                                  # DEFAULT: max_prop_level = 5 
dice_size = 6                                                       # DEFAULT: dice_size = 6
lives = 1                                                           # DEFAULT: lives = 2 
redepemtion_reward = False                                          # DEFAULT: FALSE, people are not revived.
bail_price = 200                                                    # DEFAULT: bail_price gets modified in the landed_on() jail section
real_life_dice = False                                              # Option to chose between real life dice, an system dice.
random_card = True                                                  # Set to True to get a random card once in a while. (spice up the game u know?)

# Increase of rent pr upgrade on south, west, north, east, to level 2, 3, 4, 5 or more
rates_profile = np.array([[3,2.5,1.6,1.15],[2.8,2.43,1.37,1.15],[2.6,2.55,1.23,1.15],[2.4,2.27,1.20,1.15]])  

lottery_wallet = 1000
stonk_start_value = 400                                             # DEFAULT:  start_value = 400  
stonk_minimum_value = stonk_start_value//2                          # DEFAULT:  stonk_minimum_value = start_value
stonk_max_value = 10000                                              # DEFAULT:  stonk_max_value = 5000   
bound_for_volatile_stonks = stonk_max_value//8                      # DEFAULT:  bound_for_volatile_stonks = stonk_max_value//4       
stonk_dist = "normal"                                               # DEFAULT:  stonk_dist = "normal" or "uniform"
#stonk_dist = "uniform"                                             # DEFAULT:  stonk_dist = "normal" or "uniform"
stonk_drop_to_value = stonk_max_value//10                           # DEFAULT:  stonk_drop_to_value = stonk_max_value/5 
phase1_bound = (0.96,1.08)                                          # DEFAULT:  phase1_bound = (0.96 , 1.08)
phase2_bound = (0.85,1.10)                                          # DEFAULT:  phase2_bound = (0.85 , 1.07)
phase3_bound = (0.92,1.18)                                          # DEFAULT:  phase3_bound = (0.95 , 1.20)
phase_crypto_bound = (0.73,1.35)
phase_change_rounds = 7                                             # DEFAULT:  phase_change_rounds = 7

loan_interest = 1.02                                                # DEFAULT:  loan_interest = 1.02       
initial_loan_interest = loan_interest

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

# The Richest player gives all other players 300 dollars
def chance_card_5(player):
    #print("chance_card_5")
    # Smoother
    print("  The Richest player gives all other players 300 dollars")
    richest_name = ''
    richest_amount = 0 
    for dude in playersorder:
        if players[dude]['Wallet'] > richest_amount:
            richest_name = dude
            richest_amount = players[dude]['Wallet']
    
    for new_dude in playersorder:
        players[new_dude]['Wallet'] += 300
        players[richest_name]['Wallet'] -= 300
    
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

# Property market! Increase all property levels on the board by +1!
def chance_card_8(player):
    #print("chance_card_8")
    # Neutrual
    print("  Property market raise! Increase all property levels on the board by +1!")
    print("  ")
    for prop in All_property_list:
        prop['level'] +=1 

# Recession! Decrease all properties level on the board by -1
def chance_card_9(player):
    #print("chance_card_9")
    # Neutrual
    print("  Property market fall! Decrease all properties level on the board by -1!")
    for prop in All_property_list:
        prop['level'] -=1 
    pass

# Chose a side of the board to reset to level 1
def chance_card_10(player):
    #print("chance_card_10")
    # Neutrual
    print("  You are a very angry person, with a very powerful card!")
    print("  Chose a side of the board decrease it by 2 levels!")
    for enum,side in enumerate(side_list):
        print(" {}.  {}".format(enum+1 ,side))
    print("")
    numba = option_number(player, exit_menu=False)
    if numba == None:
        numba = 1
    side_chosen = side_list[int(numba)]
    for prop in All_property_list:
        if prop['side'] == side_chosen:
            prop['level'] -= 2


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
    print("  Every player on the board pays 200$ to the Bank")
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

# All your stonks change phase to phase 1 stonks.
def chance_card_14(player):
    print("  All your stonks change phase to phase 1 stonks.")
    print("     Phase 1 rate: ",round((phase1_bound[0]-1)*100),"%  , ", round((phase1_bound[1]-1)*100) , "%")
    print("")
    if len(players[player]['Stonks']) > 0:
        for stonk in players[player]['Stonks']:
            stonk['phase'] = phase1
            stonk['phase_number'] = 1

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
    print("  You are a real estate geniuz! Sell all your properties for an additional 50"+"%"+" of their current price!")
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


def chance_card_17(player):
    global loan_interest

    print("  The BANK BANK OF 'MURICA are being generous! ")
    print("  A 1% interest is now present for the next {} rounds".format(phase_change_rounds - (players[player]['Turn']) % phase_change_rounds))
    print("")
    loan_interest = 1.01


def chance_card_17(player):
    global loan_interest

    print("  The BANK BANK OF 'MURICA are being straight up retarded! ")
    print("  A 0% interest is now present for the next {} rounds".format(phase_change_rounds - (players[player]['Turn']) % phase_change_rounds))
    print("")
    loan_interest = 1


def chance_card_18(player):

    print("")
    print("  Move to the West Location icon! ")
    print("")
    white_space(3)
    players[player]['Placement'] = 16
    landed_on(player)

def chance_card_19(player):
    print("")
    print("  Move to the East Location icon! ")
    print("")
    white_space(3)
    players[player]['Placement'] = 34
    landed_on(player)


def chance_card_20(player):
    print("")
    print("  Move to a random property on the board! ")
    print("")
    ran_num = rn.randint(1,35)
    while type(board_placement[ran_num]) == str:
        ran_num = rn.randint(1,35)

    print("  You moved to: {}".format(board_placement[ran_num]['name']))  # Should always return a property dict, hence ['name'], 
                                                                          # as long as the only dict variables in the list are properties.
    white_space(3)
    players[player]['Placement'] = ran_num
    landed_on(player)


def chance_card_21(player):
    global lottery_wallet
    print("")
    print("  If you have less than $1500 in your wallet, take $750 from the Lottery! ")
    print("  If you have more than $1500 in your wallet and the Lottery has more than $750 in it, ")
    print("  add $750 to the Lottery!")
    print("")
    if players[player]['Wallet'] >= 1500:
        print("  Thanks for the kind donation!")
        lottery_wallet += 750
        players[player]['Wallet'] -= 750
    elif (players[player]['Wallet'] < 1500) and (lottery_wallet >= 750):
        print("  Enjoy your Gainz!")
        lottery_wallet -= 750
        players[player]['Wallet'] += 750
    else: 
        print("  The Lottery did not have sufficient funds...")
        pass


def chance_card_22(player):
    # Sell all your stock for 85%, 90%, 95%, 100%, 105%, 110% of their value. (don't change the stonk price)
    # Implement dice roll with ascii art.
    pass


chance_cards = [chance_card_1, chance_card_2, chance_card_3, chance_card_4, chance_card_5, chance_card_6,
                chance_card_7, chance_card_8, chance_card_9, chance_card_10, chance_card_11, chance_card_12,
                 chance_card_13, chance_card_14, chance_card_15, chance_card_16, chance_card_17,
                 chance_card_18,chance_card_19, chance_card_20, chance_card_21]

# For testing purposes
#chance_cards = [chance_card_3]


########################################################           
# Treasure card functions

# Advance to Start and collect 200$
def treasure_card_1(player):
    #print("treasure_card_1")
    print("")
    print("  Advance to Start and collect 500$ !!!")
    print("")
    players[player]['Placement'] = 0
    players[player]['Wallet'] += 500
    landed_on(player)

# Every player on the board receives 200$
def treasure_card_2(player):
    #print("treasure_card_2")
    print("  Every player on the board receives 200$")
    for dude in playersorder:
        players[dude]['Wallet']+= 200
        
# Collect 200$ from each player        
def treasure_card_3(player):
    #print("treasure_card_3")
    print("  Collect 500$ from each player")
    for dude in playersorder:
        players[dude]['Wallet'] -= 500
        players[player]['Wallet'] += 500

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

# All of your stonks increase with 50%
def treasure_card_7(player):
    print("")
    print("  All of your stonks increase with "+'50%'+" in value!!!")
    print("  If any of your stonks passes the price ceiling at {}$".format(int(stonk_max_value)))
    print("  they are automatically sold for {}$ ".format(int(stonk_max_value)))
    print("")
    print("  If you don't have any stonks, receive a random one for free instead...")
    print("")
    if len(players[player]['Stonks']) > 0:
        for stonk in players[player]['Stonks']:
            old_price = stonk['price']
            stonk['price'] = int(1.5 * stonk['price'])
            if stonk['price'] > stonk_max_value:
                stonk['price'] = stonk_drop_to_value
                stonk['owner'] = None
                players[player]['Wallet'] += stonk_max_value
                players[player]['Stonks'].remove(stonk)
            stonk['price_history'].append(stonk['price'])
            stonk['percent_increase_pr_turn'] = round(stonk['price']*100 / old_price  ,  1)
    else:
        temp_list = []
        for stonk in stonks_list:
            if stonk['owner'] == None:
                temp_list.append(stonk['name'])
            else:
                continue

        if len(temp_list) == 0:
            print("") 
            print(" You have no stonks and there are no stonks for you to receive :( ") 
            return
        
        random_stonk_name = rn.choice(temp_list)
        for stonk in stonks_list:
            if stonk['name'] == random_stonk_name:
                stonk['owner'] = player
                players[player]['Stonks'].append(stonk)
                stonk['bought_price'] = 1
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

    if player != player_with_most_props:
        print("")
        print("  You collect {}$ from {} by having {} in level {}!".format(high_rent,player_with_most_props,prop_name,prop_level))
        print("")
    else:
        print("")
        print("  You have the most properties...")
        print("")

# Pick any property (even if its owned by a player) and add it to your hand
def treasure_card_12(player):
    print("  Pick any property (even if its owned by a player) and add it to your hand.")
    print("")
    for enum,prop in enumerate(All_property_list):
        print(" {:<2}.  {:<30} level:{:<2}  color:{:<10}  price: ${:<4}  rent: ${:<4}  owner:{}  ".format(enum+1 ,prop['name'], prop['level'], prop['color'] ,prop['price'], prop['rent'], prop['owner']))
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
        print("  Collect $600 for each player there is in the game!!!")
        players[player]['Wallet'] += (600 * len(playersorder))
    
    else: 
        print("  Collect $300 for each player there is in the game")
        players[player]['Wallet'] += (300 * len(playersorder))

# All of your stonks change to Phase 3
def treasure_card_14(player):
    print("")
    print("  All of your stonks change to Phase 3 !!! ") 
    print("")
    print("  If you don't have any stonks, receive a random one for free instead AND set it to Phase 3...")
    print("")
    if len(players[player]['Stonks']) > 0:
        for stonk in players[player]['Stonks']:
            stonk['phase'] = phase3
            stonk['phase_number'] = 3

    else:
        temp_list = []
        for stonk in stonks_list:
            if stonk['owner'] == None:
                temp_list.append(stonk['name'])
            else:
                continue

        if len(temp_list) == 0:
            print("") 
            print(" You have no stonks and there are no stonks for you to receive :( ") 
            return
        
        random_stonk_name = rn.choice(temp_list)
        for stonk in stonks_list:
            if stonk['name'] == random_stonk_name:
                stonk['phase'] = phase3
                stonk['phase_number'] = 3
                stonk['owner'] = player
                stonk['bought_price'] = 1
                players[player]['Stonks'].append(stonk)
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
        print("")
        players[player]['Wallet'] += players[player]['Networth']*0.25

    else: 
        print("  Take 10"+"%"+" of your Networth and add it to your wallet!")
        print("")
        players[player]['Wallet'] += players[player]['Networth']*0.10
        

def treasure_card_18(player):

    print("")
    print("  Recieve $300 and move to the South Location icon! ")
    print("")
    white_space(3)
    players[player]['Placement'] = 7
    players[player]['Wallet'] += 300
    landed_on(player)


def treasure_card_19(player):

    print("")
    print("  Recieve $300 and move to the North Location icon! ")
    print("")
    white_space(3)
    players[player]['Placement'] = 25
    players[player]['Wallet'] += 300
    landed_on(player)


def treasure_card_20(player):
    global lottery_wallet
    print("")
    print("  Take 50% of the JACKPOT!!! ")
    print("  Add ${} to your wallet.".format(lottery_wallet//2))
    print("")
    white_space(3)
    players[player]['Wallet'] += lottery_wallet//2
    lottery_wallet = lottery_wallet//2


def treasure_card_21(player):
    #print("treasure_card_11")
    print("  Swap your wallet with the player who has the thickest wallet")
    print(" ")

    richest_name = ''
    richest_amount = 0 
    for dude in playersorder:
        if players[dude]['Wallet'] > richest_amount:
            richest_name = dude
            richest_amount = players[dude]['Wallet']

    if richest_name == player:
        print("  You are the richest boi!")
    else:
        print("  {} and {} swapped their wallets!".format(player,richest_name))

    players[richest_name]['Wallet'] = players[player]['Wallet']
    players[player]['Wallet'] = richest_amount
    

def treasure_card_22(player):
    ran_num = rn.randint(1,4)

    richest_name = ''
    richest_amount = 0 
    for dude in playersorder:
        if players[dude]['Networth'] > richest_amount:
            richest_name = dude
            richest_amount = players[dude]['Networth']
    
    if ran_num == 3:
        print("")
        print("  Take 20"+"%"+" of the Networth of the wealthiest player and add it to your wallet!!!")
        print("")
        players[player]['Wallet'] += players[richest_name]['Networth']*0.20

    else: 
        print("  Take 10"+"%"+" of the Networth of the wealthiest player and add it to your wallet!")
        print("")
        players[player]['Wallet'] += players[richest_name]['Networth']*0.10


def treasure_card_23(player):
    #print("treasure_card_11")
    ran_num = rn.randint(1,4)
    percentage = 0.25
    if ran_num == 3:
        percentage = 0.5


    print("  Take {}% of the money in the richest players Wallet and move it to your own!".format(int(percentage*100)))
    print(" ")

    richest_name = ''
    richest_amount = 0 
    for dude in playersorder:
        if players[dude]['Wallet'] > richest_amount:
            richest_name = dude
            richest_amount = players[dude]['Wallet']

    if richest_name == player:
        print("  You are the richest boi!")
    else:
        print("  {} took {} from {}'s wallet!".format(int(player,richest_amount*percentage,richest_name)))

    players[richest_name]['Wallet'] -= int(richest_amount* percentage)
    players[player]['Wallet'] += int(richest_amount* percentage)




treasure_cards = [treasure_card_1,treasure_card_2,treasure_card_3,treasure_card_4,treasure_card_5,treasure_card_6
                 ,treasure_card_7, treasure_card_8, treasure_card_9, treasure_card_10, treasure_card_11
                ,treasure_card_12, treasure_card_13, treasure_card_14, treasure_card_15,treasure_card_16,
                treasure_card_17, treasure_card_18, treasure_card_19, treasure_card_20, treasure_card_21, treasure_card_22,
                treasure_card_23]

# For testing purposes.
# treasure_cards = [treasure_card_18, treasure_card_19, treasure_card_20, treasure_card_21, treasure_card_22,
#                 treasure_card_23]


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

# The player with the most most money invested in stonks has ONE (random) of their stonks turn phase 2
def curse_card_4(player):
    print("  The player with the most most money invested in stonks has ONE of their stonks change")
    print("  to a phase 2 stonk.   Phase 2 rate:  ",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
    print("")
    who_has_most_val_stonks = player
    highest_stonk_val = 0
    for player in playersorder:
        player_stonk_val = 0
        for stonk in players[player]['Stonks']:
            player_stonk_val += stonk['price']
        if player_stonk_val > highest_stonk_val:
            highest_stonk_val = player_stonk_val
            who_has_most_val_stonks = player

    if len(players[who_has_most_val_stonks]['Stonks']) > 0:
        stonk_to_phase_2 = rn.choice(players[who_has_most_val_stonks]['Stonks'])
        stonk_to_phase_2['phase'] = phase2
        stonk_to_phase_2['phase_number'] = 2
        print("")
        print("  {} one of your stonks is now in phase 2 !".format(who_has_most_val_stonks , stonk_to_phase_2['name'] ))
        print("")
    else:
        print("You don't have any stonks...")

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
            if prop['level'] >= highest_level:
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

# All of your stonks change phase to phase 2 stonks (REAL BAD)
def curse_card_11(player):
    print("  All your stonks change phase to phase 2 stonks.")
    print("     Phase 2 rate: ",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
    print("")
    if len(players[player]['Stonks']) > 0:
        for stonk in players[player]['Stonks']:
            stonk['phase'] = phase2
            stonk['phase_number'] = 2

# All of your stonks decrease with 50%
def curse_card_12(player):
    print("")
    print("  All of your stonks decrease with "+'50%'+" in value!!!")
    print("")
    if len(players[player]['Stonks']) > 0:
        for stonk in players[player]['Stonks']:
            old_price = stonk['price']
            stonk['price'] = int(0.5 * stonk['price'])
            if stonk['price'] <= stonk_minimum_value:
                stonk['price'] = stonk_minimum_value
            stonk['price_history'].append(stonk['price'])
            stonk['percent_increase_pr_turn'] = round(stonk['price']*100 / old_price  ,  1)


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
    


def curse_card_15(player):
    print("  Elon Musk made a dank tweet about Doge Coin!")
    print("  All stonk prices drop 30% and all crypto currencies increase with 40%!!!")
    print("")

    for stonk in stonks_list:
        if stonk['name'] in ['Bit Coin', 'Ethereum','Doge Coin']:
            old_price = stonk['price']
            stonk['price'] = int(stonk['price']* 1.4)
            stonk['price_history'].append(stonk['price'])
            stonk['percent_increase_pr_turn'] = round(stonk['price']*100 / old_price  ,  1)
        else:
            old_price = stonk['price']
            stonk['price'] = int(stonk['price']* 0.7)
            stonk['price_history'].append(stonk['price'])
            stonk['percent_increase_pr_turn'] = round(stonk['price']*100 / old_price  ,  1)


def curse_card_16(player):
    random_stonks = rn.choices(stonks_list, k=3)

    print("  r/WallStreetBets are doing autistic shit again on Robin Hood!!!")
    print("  Mayfair decreases by 2 levels! and ")
    print("  {}, {}, and {}, increase by 30%!".format(random_stonks[0]['name'],random_stonks[1]['name'],random_stonks[2]['name']))

    Blue_2['level'] -= 2

    for stonk in random_stonks:
        old_price = stonk['price'] 
        stonk['price'] = int(stonk['price']* 1.3)
        stonk['price_history'].append(stonk['price'])
        stonk['percent_increase_pr_turn'] = round(stonk['price']*100 / old_price  ,  1)
    print("")

def curse_card_17(player):
    global loan_interest
    random_stonks = rn.choices(stonks_list, k=3)

    print("  The BANK BANK OF 'MURICA is being super stingy! ")
    print("  A 3% interest is now present for the next {} rounds".format(phase_change_rounds - (players[player]['Turn']) % phase_change_rounds))
    print("")
    loan_interest = 1.03

def curse_card_18(player):
    global loan_interest
    random_stonks = rn.choices(stonks_list, k=3)

    print("  The BANK BANK OF 'MURICA is being CRAZY stingy! ")
    print("  A 4% interest is now present for the next {} rounds".format(phase_change_rounds - (players[player]['Turn']) % phase_change_rounds))
    print("")
    loan_interest = 1.04


def curse_card_19(player):

    print("")
    print("  The slimy Player Credit Default Swap broker has gone bankrupt!")
    print("  If you own a swap, it is voided!")
    print("")
    for deriv in players[player]['Derivatives']:
        if deriv['type'] == "player_credit_default_swap":
            players[player]['Derivatives'].remove(deriv)


def curse_card_20(player):
    global lottery_wallet
    print("")
    print("  You decided to do something whole hearted <3 ")
    print("  Donate 5% of you wallet to good will (Free Park Lottery)")
    print("  ")
    print("")
    donation = int(players[player]['Wallet'] * 0.05)
    players[player]['Wallet'] -= donation
    lottery_wallet += donation


def curse_card_21(player):
    global lottery_wallet
    print("")
    print("  You decided to do something stupid you might not be able to afford... ")
    print("  Donate 15% of your Networth to good will (Free Park Lottery)")
    print("  ")
    print("")
    donation = int(players[player]['Networth'] * 0.15)
    players[player]['Wallet'] -= donation
    lottery_wallet += donation


def curse_card_22(player):
    # Sell all your stock for 70% of their value. (don't change the stonk price)
    pass

def curse_card_23(player):
    # reduce property by 1, shootings from opposing side gang membersæ
    pass



cursed_cards = [curse_card_1,curse_card_2,curse_card_3,curse_card_4,curse_card_5,curse_card_6, curse_card_7,
                curse_card_8,curse_card_9, curse_card_10, curse_card_11, curse_card_12, curse_card_13,
                curse_card_14, curse_card_15, curse_card_16, curse_card_17, curse_card_18, curse_card_19, 
                curse_card_20, curse_card_21]


### Functions 

def play(sound_string):
    return winsound.PlaySound("sounds\\{}".format(sound_string),winsound.SND_FILENAME)

def clearscreen():
    for _ in range(20):
        print("")

def white_space(numba):
    for _ in range(numba):
        print("")

def load_game_pickle(new_player = False, remove_player = False):
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
    global stonks_list
    global All_property_list
    global board_placement
    global max_prop_level
    global loaded_time_diff

    max_prop_level = pickle_dict['max_prop_level']
    players = pickle_dict['players']
    playersorder = pickle_dict['playersorder']
    lottery_wallet = pickle_dict['lottery_wallet']
    stonks_list = pickle_dict['stonks_list']
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
                'stonks_list':stonks_list , 'All_property_list':All_property_list , 'max_prop_level': max_prop_level
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
    print(" ██████   ██████    ███████    ██████   █████    ███████    ███████████     ███████    █████       █████ █████")
    print("░░██████ ██████   ███░░░░░███ ░░██████ ░░███   ███░░░░░███ ░░███░░░░░███  ███░░░░░███ ░░███       ░░███ ░░███ ")
    print(" ░███░█████░███  ███     ░░███ ░███░███ ░███  ███     ░░███ ░███    ░███ ███     ░░███ ░███        ░░███ ███")
    print(" ░███░░███ ░███ ░███      ░███ ░███░░███░███ ░███      ░███ ░██████████ ░███      ░███ ░███         ░░█████ ")
    print(" ░███ ░░░  ░███ ░███      ░███ ░███ ░░██████ ░███      ░███ ░███░░░░░░  ░███      ░███ ░███          ░░███")
    print(" ░███      ░███ ░░███     ███  ░███  ░░█████ ░░███     ███  ░███        ░░███     ███  ░███      █    ░███ ")
    print(" █████     █████ ░░░███████░   █████  ░░█████ ░░░███████░   █████        ░░░███████░   ███████████    █████ ")
    print("░░░░░     ░░░░░    ░░░░░░░    ░░░░░    ░░░░░    ░░░░░░░    ░░░░░           ░░░░░░░    ░░░░░░░░░░░    ░░░░░")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")

    time.sleep(1)                                                                                                                   
                                                                                                    
    print("                                           ./((((##%%%&&&&(.                           ")             
    print("                                        %&%%##((((#%%&&&&&&%%                          ")             
    print("                                      (@&&%%%#(//(##%&&&@&&%%                          ")             
    print("                                      #@@&&&%#((//(#%%&&&&&%%                          ")             
    print("                                       #@@&&%%###(##%%&&&&%%%(/,                       ")             
    print("                                        &@@&&&%####&&@@@&&&&&&&&&&#                    ")             
    print("                                        .@&%&@@@@@@@@@@@&&&&@@@@&&&%                   ")             
    print("                                     .%@@@@@@@%/***,,,,,,,.,.,,,(@@*                   ")             
    print("                                    (@@@@@*,,,,,,...........,,,,,,.                    ")             
    print("              ...                     %@@,,./,,.......,..,..,,,,,,,    ")             
    print("              .,.                      .,,.,*.,,.....,.((,,,,,,,,.,*   ")             
    print("     .,,,,.,,,,,,.                     ,,....... .,.........,,,,,,,,.,  ")             
    print("  ..,,,,,,,,,,,., .#%%%&&&#*            ,,**,  .**    ,,,,. ,,,,,,,,.  ")             
    print("     ,,........, ,%%########%%&&@%,     . ..               ,,,,,***     ")             
    print("           ..,,,.%&&%%%%#########%%%%&@&*.,...,(%%%#/*,,,***,*****      ")             
    print("                 (@@&&&&%%%%%########%#%&@@@*,*,**,*,,*,********       ")             
    print("                     ,%@&&&&%%%%%%###%%####%,..,***,*****///,          ")             
    print("                         .&@&&&%%%%%%%%#####/ ,** **.. ../&@@@@@@@/                    ")             
    print("                             ,@@&&%&%%%#####(*,**/*,..,%%&&%%%%&&&@@@&.                ")             
    print("                                ,@&@&%%%%####     .,,%%%&&%%%%&&&&%%&&@@,              ")             
    print("                                   @&%%%%%%##/     %%%%%&&&%%%@&&%%%%%%&&&.            ")             
    print("                                  (@&%%%%%%%%%   (%%&&&&&&&%%%@@&%%%&&@@@&&%           ")             
    print("                                  &&%%%%%%%%%%,,&&&&&&&&&@@&&&@@@&@@@@&&&&&&&/         ")             
    print("                                  &&%%%%%%%%&%&&&&&&&&&&&&@@@@@@&&&&&&&%%&&&&&(        ")             
    print("                                 ,@&&%%%%%%%%&&&&&&&&&@@/,.,,,&&&&&&&&&&&&&&&&%        ")             
    print("                                 *&&&%%%%%%%%&&&&&&&&&%,,...,&*&&@&&&&&&@@@@@#         ")             
    print("                                 *@&&&%%%%%&&&&&&&&@@%,,,,...*#@@@@%#//*.              ")             
    print("                                 /&&&%%%%%&&&&&&&&&@#,,,,,..,.  %&                     ")             
    print("                                 #&&%%%%%%&&&&%%%%&%/,,,,,,..  (&,                     ")             
    print("                                 &&%%%%%%%&&&%%%%%%%&#.,,,,,...&(                      ")             
    print("                                 %&&&%%%%&&@@@@@@@&&&&&,,*.,,.*%                       ")             
    print("                                 (&&%%%%%&@@@@&&&%%&&&&@,.   *&.                       ")                                          
    print("                                 ,@&&&%&&@@@&&&&%%&&&&&@     &/                        ")             
    print("                              #@@@@&&&&&%%%%%%%%%&&&&&@     #%                         ")             
    print("                           %%%%%%%%%%%%%%%%%%%%%&&&&&(     *%.                         ")                                          
    print("                           *%%%%&&%%%%%%%%%&&&&&@&@/       %,                          ")                                          
    print("                            .%%&&&&&&&&&&&@@@@@@/         ((                           ")                                          
    print("                            .%%@@%@@@@@@@@@@@@@@(        .#                            ")                                          
    print("                             %&&@%&  .@@&&&&&&&&&        #,                            ")                                          
    play("drums.wav")
    print("\n"*10)
    print("")
    print("                                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    ")
    print("                                $$                             $$    ")
    print("                                $$     MONOPOLY REMASTERED     $$    ")
    print("                                $$                             $$    ")
    print("                                $$       Second Edition        $$    ")
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
    print("                     Type 3.  Load Game & add an extra player")
    print("                                        ")
    print("                     Type 4.  Remove a player & Load Game")
    white_space(10)
    numba = input("                Write the number here: ")
    #numba = None

    global loaded_time_diff
    loaded_time_diff = 0 

    if numba == '2':
        load_game_pickle(new_player = False, remove_player = False)

    elif numba == '3':
        print(" This feature is not yet implemented")
        print(" Reload the game...")
        return
        #load_game_pickle(new_player = True, remove_player = False)

    elif numba == '4':
        print(" This feature is not yet implemented")
        print(" Reload the game...")
        return
        #load_game_pickle(new_player = True, remove_player = True)


    else:
        print("")
        print("              Quick rules:")
        print("              ")
        print("                 - Win by either making everyone else bankrupt, or gaining {}$ in Networth.".format(winning_condition_amount))
        print("                 - Buy Properties, Stonks, and other investments to increase your Networth!")
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

            players[x] = {"Wallet": start_money, "Property": [], "Stonks": [] , "Luck": 0.5, "Placement": 0
            , 'Immunity': 0 , 'Lives':lives , 'Networth':start_money, 'Turn': roundcount
            , 'Debt': 0 , "Loan_terms_left": 0, 'Derivatives' : [], "Turns_in_jail" : 0}
            playersorder.append(x)

            # if x == "Charlotte":
            #     players[x]["Wallet"] += 3000

        play("eriglar.wav")
        
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
        prop['price'] = int(round(prop['original_price'] + (cur_round*5) + prop['rent']*0.4 , -1 ))

def reset_prop_level():                # resets property levels for properties which are not owned by players.
    for prop in All_property_list:
        if prop['owner'] == None:
            prop['level'] = 1
            prop['mortgaged'] = False

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
            play("owenwowson3.wav")
            

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
                play("donald-trump-bing-bong.wav")
                #input(" press Enter to continue...")
                return

            else:
                players[cur_placement["owner"]]['Wallet'] += cur_placement["rent"]
                players[player]['Wallet'] -= cur_placement["rent"]
                print("")
                print(" You landed on {}'s property! Pay {}$ ".format(cur_placement['owner']  ,        
                        cur_placement['rent']))
                print("")
                play(rn.choice(["trump_thank_you_{}.wav".format(i) for i in range(1,4)]))
                time.sleep(0.5)
                cur_placement['level'] += 1
                #input(" press Enter to continue...")
                broke_af(player)

        
        
    else: 
        global bail_price
        global avg_networth

        if cur_placement == "Jail":
            players[player]['Turns_in_jail'] += 1
            dice_size = 6- players[player]['Turns_in_jail']
            bail_price = 200                # updated so that the previous bail price doesn't interfere.
            if bail_price < 0.1*players[player]['Networth']:
                bail_price = int(round(0.1*players[player]['Networth'] , -1))
            else:
                pass
                #bail_price = 200

            white_space(2)
            print(" You may either pay 10"+'%'+" of your Networth to get out of jail, or try to roll a double ")
            print(" with two {}-sided dice.".format(dice_size))
            print(" You may not leave jail until one of the two options are fulfilled!")
            print(" You are NOT garenteed to leave jail after three rounds.")
            print("")
            print(" Type 1 to pay {}$ ".format(bail_price))
            print(" Type 2 to attempt to roll doubles  Dice size: {}".format(6- players[player]['Turns_in_jail']))
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
                players[player]['Turns_in_jail'] = 0

            elif jail_choice == '3' and players[player]['Immunity'] > 0 :
                # Pay some money to get to visit fail tile
                white_space(4)
                print(" You paid 1 Immunity for a bail!".format(bail_price))
                print(" You're out of jail now! ")
                play("donald-trump-bing-bong.wav")
                players[player]['Placement'] = 9            # placement 9 is the "visiting jail" tile.
                players[player]['Immunity'] -= 1
                players[player]['Turns_in_jail'] = 0

            else:
                print("")
                dice_roll_ascii_art()
                input(" press Enter to roll the dice!")
                print("")
                print(" Rolling the dice!!! ")
                print("")
                print("")
                roll_1 = rn.randint(1, dice_size)
                roll_2 = rn.randint(1, dice_size)
                print(" You rolled : " , roll_1 , "and" , roll_2 )
                print("")
                if roll_1 == roll_2:
                    players[player]['Turns_in_jail'] = 0
                    print(" You rolled doubles!")
                    print(" You're out of jail now! ")
                    print("")
                    #input(" press Enter to continue...")
                    players[player]['Placement'] = 9     # Visit jail tile.
                    play("yea_boi_short.wav")
                    
                else:
                    print(" You're still in jail :( ")
                    print("")
                    play("det-er-mit-holds-skyld.wav")
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
            white_space(2)
            #input("  Press Enter to continue ...")
            #white_space(10)
            players[player]['Wallet'] += lottery_wallet
            lottery_wallet = 0

            print("  Because you landed on Free park, advance 7 steps to the next location icon.")
            print("")
            white_space(3)
            players[player]['Placement'] = 25
            return landed_on(player)


        elif cur_placement == "Start":
            # Landed on start, advance to location icon.
            print("  Because you landed on Start, advance 7 steps to the next location icon.")
            print("")
            white_space(3)
            players[player]['Placement'] = 7
            return landed_on(player)

            
        elif cur_placement == "Location_icon":
            #Options to do shit for 100$ or/and trade or stuff idk? 
            loc_price_rate = int((players[player]['Turn'])*5)
            terror_fine =  int(players[player]['Networth']*0.05 - 200)
            if terror_fine < 100:
                terror_fine = 100
            if terror_fine >= 400:
                terror_fine = 400

            if players[player]['Wallet'] > loc_price_rate + 200:
                players[player]['Wallet'] -= loc_price_rate
                lottery_wallet += loc_price_rate
                print("  ")
                white_space(4)
                print("  You landed on the Location Icon! Pay {}$ and choose a mandatory benefit".format(loc_price_rate))
                print("  ")
                print("  You have the following options and you can only choose ONE:")
                print("  NO FUCKING BACKSIES!")
                print("  ")
                print("               * Location Menu *")
                print("")
                print("          {}'s Wallet: ${}".format(player, players[player]['Wallet']))
                print("________________________________________________________________________")
                print("")
                print("1.  Travel to a destination                  cost: $0 Extra ")
                print("2.  Hire a lawyer, and take a location       cost: $1.5*(Property price) Extra")
                print("3.  Buy 1x Immunity for the next rent        cost: $400 Extra ")
                print("4.  Enter the Player Credit Default Swap     cost: $0 Extra ")
                #if players[player]['Turn'] >= 10 and players[player]['Networth'] < avg_networth*0.8 :                                # cancling out terrorism as it wasn't used.
                #    print("5.  Bomb a property                          cost: You go to Jail +  ${} fine".format(int(terror_fine)))  # cancling out terrorism as it wasn't used.
                print("")
                print("0.  Exit the menu                            cost: $0 Extra")
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
                                    print("{:<3}  {:<25} colorset: {:<10}  level:{:<3}  rent:${:<4}  owner:{:<15}  ".format(
                                        integer+1, board_placement_names[integer], prop['color'], prop['level'] ,
                                        prop['rent'] ,  owner ))
                                else:
                                     print("{:<3}  {:<25} colorset: {:<10}  price: ${}".format(
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
                    print("  compensation for this dirty white collar crime...")
                    white_space(3)
                    print("  {}'s Wallet : ${}".format(player, int(players[player]['Wallet'])))
                    print("")
                    print("  Choose your desired property to sue for!")
                    print("")
                    sue_price = 0
                    for enum,prop in enumerate(All_property_list):
                        if prop['owner'] == None or prop['owner'] == player:
                            continue
                        if prop['price'] < 300:
                            sue_price = 150 + prop['price']
                        else:
                            sue_price = int(1.5*(prop['price']))

                        print(enum+1,"  {:<25}    cost of lawsuit {}$".format(prop['name'] , sue_price)) 
                    print("")
                    print("0    If you changed your mind...")

                    white_space(2)
                    numba = option_number(player)

                    for enum,prop in enumerate(All_property_list):
                        if prop['price'] < 300:
                            sue_price = 300 + prop['price']
                        else:
                            sue_price = 1.5*(prop['price'])
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
                    # Grant 1 immunity for a total of ($400)
                    players[player]['Wallet'] -= 400
                    players[player]['Immunity'] += 1

                elif numba == 4:
                    credit_default_swap_menu(player)

                elif numba == 5:
                    return  # cancling out terrorism as it wasn't used.
                    play("Allahu Akbar.wav")
                    if players[player]['Networth'] < avg_networth*0.8:
                        # Do a drive by 
                        print("  Choose the target of your drive-by!")
                        print("  Remember, you get jail time and you have to pay a fine of ${}".format(int(terror_fine)))
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
                print("  You are too poor to buy use these benefits. You need {}$ more".format(int(loc_price_rate+200 - players[player]['Wallet'])))
                print("")
                print("  You need a surplus of $200 in addition to the location rate at {}$ ".format(int(loc_price_rate)))
                print("  {}'s Wallet: ${}".format(player, int(players[player]['Wallet'])))
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
            play("ladies-and-gentlemen-we-got-him.wav")
            return extraturn
            
        else: 
            pass

##########################  DERIVATIVES  ################################

def credit_default_swap_menu(player):

    # If player has def
    if len(players[player]['Derivatives']) >= 1: 
        print(" ")
        print("  You already have a credit default swap.")
        print("  Wait until your position has expired!")
        print("  ")
        return 

    print("")
    print("")
    print("  This is credit default swap menu.")
    print("  In this menu, you may place a swap on any player in the game, ")
    print("  with the aim of guessing who has the lowest networth after a set amount of rounds.")
    print("  The swap expires after 4, 8, or 12 rounds, with scaled returns of 1.1 ,1.5, 2.1 times respectively.")
    print("  After choosing a player and runtime, you choose a fixed premium to pay pr. round until expiry. The payment is made at the end of the turn.")
    print("  IF a player is unable to make a single a payment, the position is voided and the payments potential are lost.")
    print("")
    print("  ")
    print("  Once the swap expires, an incorrect guess will yield no returns.")
    print("  HOWEVER, if you guess correctly, you receive  {} * (run time) * (premium price) * (scaled returns) ".format(len(playersorder)))
    print("")

    avg_networth = sum([players[dude]['Networth'] for dude in playersorder]) // len(playersorder)
    scaled_returns = {4:1.1 ,8:1.5, 12:2.1}

    for idx,dude in enumerate(playersorder):
        if dude == player:
            continue
        networth_ratio =  (players[dude]['Networth'] / avg_networth)
        networth_percantage =  (players[dude]['Networth'] / sum([players[dude]['Networth'] for dude in playersorder]))*100
        for idx2,runtime in enumerate([4,8,12]):
            return_pr_dollar =  float(scaled_returns[runtime]) * len(playersorder) * networth_ratio
            print("  {}    Name: {:<20}  Runtime: {:<2}   Market share: {:.2f}%     Return pr. dollar : ${:.2f}".format((idx*3 + idx2 + 1),dude, runtime, networth_percantage, return_pr_dollar))
    print("")

    numba = option_number(player)  

    print("")
    premium = input("  Choose your premium to pay each round for {} rounds: ".format((numba%3 +1)*4))
    if (type(premium) == str) and (premium in ['', " " ,None]):
        premium = 50
    elif type(eval(premium)) != int:
        print("  Please write an integer!!! Last try!")
        premium = input("  Choose your premium to pay each round for {} rounds: ".format((numba%3 +1)*4))
    else:
        pass
    premium = int(premium)
    print("Chosen premium:", premium)  

    break_out = False 
    for idx,dude in enumerate(playersorder):
        if break_out:
            break
        networth_ratio =  (players[dude]['Networth'] / avg_networth)
        networth_percantage =  (players[dude]['Networth'] / sum([players[dude]['Networth'] for dude in playersorder]))*100
        for idx2,runtime in enumerate([4,8,12]):
            return_pr_dollar =  float(scaled_returns[runtime]) * len(playersorder) * networth_ratio

            if (idx*3 + idx2) == numba:
                players[player]['Derivatives'].append({'type': "player_credit_default_swap" ,'player': dude , 'premium' : premium, 'remaing_run_time': runtime, 
                'potential_gain': int(return_pr_dollar*runtime*premium) , "runtime": runtime , 'trading_cost' : premium*runtime })
                
                print("Position data: ", players[player]['Derivatives'][0])

                break_out = True
                break
    play("oh_shots_fired.wav")
    input("  press Enter to continue...")


def player_lost_check_swaps(player_lowest_networth):
    for player in playersorder:
        if len(players[player]['Derivatives']) > 0:
            for deriv in players[player]['Derivatives']:
                if deriv['type'] == 'player_credit_default_swap':  # only for player_credit_default_swap         
                    if player_lowest_networth == deriv['player']:
                        proportion_paid = int((deriv['runtime'] - deriv['remaing_run_time']) / deriv['runtime'] )
                        deriv['potential_gain'] *= proportion_paid # Adjusting for amount of times paid.

                        if deriv['potential_gain'] >= 2500:
                            print("")
                            print("  {}, your Player Credit Default Swap has expired in the money!!!".format(player))
                            print("  Enjoy your the anthem of success and sick gainz of: ${}".format(deriv['potential_gain']))
                            print("")
                            print("")
                            print("            |       ")
                            print("           / \       ")
                            print("          / _ \       ")
                            print("         |.o '.|       ")
                            print("         |'._.'|       ")
                            print("         |     |       ")
                            print("       ,'|  |  |`.       ")
                            print("      /  |  |  |  \       ")
                            print("      |,-'--|--'-.|        ")
                            print("")
                            print("")  
                            play("coffin_dance.wav")                  
                        else:
                            print("")
                            print("  {}, your Player Credit Default Swap has expired in the money!!!".format(player))
                            print("  Enjoy your small potato gainz of: ${}".format(deriv['potential_gain']))
                            print("")
                            print("")
                            play("trump_small_potatos.wav")
                            
                        players[player]['Wallet'] += deriv['potential_gain']
                        players[player]['Derivatives'].remove(deriv)
                        input("  press Enter to continue...")

                    else:
                        pass 


def checking_swaps(player):
    if len(players[player]['Derivatives']) > 0:
        for deriv in players[player]['Derivatives']:
            if deriv['type'] == 'player_credit_default_swap':  # only for player_credit_default_swap
                deriv['remaing_run_time'] -= 1
                players[player]['Wallet'] -= deriv['premium']

                if deriv['remaing_run_time'] == 0:
                    # cash money bby
                    player_lowest_networth = ""
                    lowest_networth = 999999999
                    for dude in playersorder:
                        temp_networth = players[dude]['Networth']
                        if temp_networth < lowest_networth:
                            lowest_networth = temp_networth
                            player_lowest_networth = dude
                    
                    if player_lowest_networth == deriv['player']:
                        if deriv['potential_gain'] >= 2500:
                            print("")
                            print("  {}, your Player Credit Default Swap has expired in the money!!!".format(player))
                            print("  Enjoy your the anthem of success and sick gainz of: ${}".format(deriv['potential_gain']))
                            print("")
                            print("")
                            print("            |       ")
                            print("           / \       ")
                            print("          / _ \       ")
                            print("         |.o '.|       ")
                            print("         |'._.'|       ")
                            print("         |     |       ")
                            print("       ,'|  |  |`.       ")
                            print("      /  |  |  |  \       ")
                            print("      |,-'--|--'-.|        ")
                            print("")
                            print("")  
                            play("coffin_dance.wav")                  
                        else:
                            print("")
                            print("  {}, your Player Credit Default Swap has expired in the money!!!".format(player))
                            print("  Enjoy your small potato gainz of: ${}".format(deriv['potential_gain']))
                            print("")
                            print("")
                            play("trump_small_potatos.wav")
                            
                        
                        
                        players[player]['Wallet'] += deriv['potential_gain']
                    else:
                        print("")
                        print("  {}, your Player Credit Default Swap has expired out of the money...".format(player))
                        print("  Your position has been removed...")
                        print("")
                        play("mission_failed_cod.wav")

                    players[player]['Derivatives'].remove(deriv)
                    
                    input("  press Enter to continue...")

                else: 
                    if players[player]['Wallet'] <= 0:
                        print("") 
                        print("  {}, your wallet balance went below 0, and your Player Credit Default Swap ".format(player))
                        print("  position on {} with potential payoff of {} is canceled...".format(deriv['player'], deriv['potential_gain'])) 
                        print("") 
                        players[player]['Derivatives'].remove(deriv)
                        play("mario_game_over.wav")
                        input("  press Enter to continue...")



###########################  STONKS START ##########################################

def stonk_menu(player):
    print()
    white_space(4)
    print("                $ $ $ $ $ $$ $ $ $ $ $  ")
    print("              $ $ $ $ $ $ $$ $ $ $ $ $ $ ")
    print("             $ $                      $ $               ") 
    print("            $ $                        $ $") 
    print("           $ $      - STONK MENU -      $ $ ")
    print("            $ $                        $ $                       PLAYER          : {}".format(player))
    print("             $ $                      $ $                        PHASE CHANGE IN : {} ROUNDS".format(phase_change_rounds - (players[player]['Turn']%phase_change_rounds)))
    print("              $ $ $ $ $ $ $$ $ $ $ $ $ $                         ROUND           : {} ".format(players[player]['Turn']))
    print("                $ $ $ $ $ $$ $ $ $ $ $                           DISTRIBUTION    : {}".format(stonk_dist))
    print("")
    print("")
    if stonk_dist == 'normal':
        print("                                                                                               Phase Rates :")
        print("    Penny stonk value   : ${} or lower".format(bound_for_volatile_stonks//2) , "      Volatility multiplier: 1.5"  ,"                     phase 1 mean:",round((phase1_mean)*100, 1),"%  ,  phase 1 stdev:", round((phase1_std)*100, 1) , "%")
        print("    Small stonk value   : ${} to ${}".format(bound_for_volatile_stonks//2, bound_for_volatile_stonks), "      Volatility multiplier: 1.2" ,"                     phase 2 mean:",round((phase2_mean)*100, 1),"%   ,  phase 2 stdev:", round((phase2_std)*100, 1) , "%")
        print("    Normal stonk value  : ${} to ${}".format(bound_for_volatile_stonks, stonk_max_value//2) , "     Volatility multiplier: 1" ,"                       phase 3 mean:",round((phase3_mean)*100, 1),"%  ,  phase 3 stdev:", round((phase3_std)*100, 1) , "%")
        print("    Big boi stonk value : ${} or larger".format(stonk_max_value//2) , "    Volatility multiplier: 0.8" ,"                     crypto  mean:",round((phase_crypto_mean)*100, 1),"%  ,  crypto  stdev:", round((phase_crypto_std)*100, 1) , "%")
    else:
        print("                                               Phase Rates :")
        print("                                                   phase 1 :",round((phase1_bound[0]-1)*100),"%  , ", round((phase1_bound[1]-1)*100) , "%")
        print("                                                   phase 2 :",round((phase2_bound[0]-1)*100),"%   , ", round((phase2_bound[1]-1)*100) , "%")
        print("                                                   phase 3 :",round((phase3_bound[0]-1)*100),"%  , ", round((phase3_bound[1]-1)*100) , "%")
        print("                                                   crypto  :",round((phase_crypto_bound[0]-1)*100),"%  , ", round((phase_crypto_bound[1]-1)*100) , "%")
    print("")
    print("                                                    Stonk Price Ceiling = {}$    Stonk Price Floor = {}$ ".format(stonk_max_value, stonk_minimum_value) )
    print("                                                                    ")
    print("          {}'s Wallet: ${}".format(player , int(players[player]['Wallet'])))
    print()
    print("___________________________________________________________________")
    print("")
    print("")
    print("    1. Buy Stonks")
    print("    2. Sell Stonks ")
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
        for enum,stonk in enumerate(stonks_list):
            if stonk['owner'] == None:
                print("{:<2}  {:<22}    price: {:<4}$   Increase this round: {:<5}    history: {}   ".format(enum+1 
                ,stonk['name'] , stonk['price'], str(round(stonk['percent_increase_pr_turn'] - 100 ,1 ))+'%' , stonk['price_history'] ))
        print("")
        print("0   Exit the menu")
        print("____________________________________________________________________________________")
        white_space(2)
        numba = option_number(player)
        if numba == None or numba == -1:
            print(" You did nothing. ")
            return stonk_menu(player)

        elif enough_money_to_buy(player,stonks_list[numba]['price']):
            for enum,stonk in enumerate(stonks_list):
                if enum == numba:
                    if stonk['owner'] == None:
                        stonk = stonks_list[enum]
                        stonk['owner'] = player
                        players[player]['Wallet'] -= stonk['price']
                        stonk['bought_price'] = int(stonk['price'])
                        players[player]['Stonks'].append(stonk)
                        print("")
                        print("  You have purchased the {} for {}$ ".format(stonk['name'],stonk['price']))
                        print("")
                    else:
                        print("")
                        print("  Somebody already owns thats stonk!!!")
                        print("")
                
            return stonk_menu(player)

        else:
            print("  You are too poor to buy that stonk. Try buying another one...")
            print("")
            return stonk_menu(player)


    if numba == 2:
        if len(players[player]['Stonks']) == 0:
            print("")
            print("  You don't own any stonks...")
            print("")
            return stonk_menu(player)
        white_space(2)
        for enum,stonk in enumerate(stonks_list):
            if stonk['owner'] == player:
                print("{:<2}  {:<22}  Bought Price: {:<5}$   Price: {:<5}$  Increase this round: {:<5}  History: {}   ".format(enum+1 
                ,stonk['name'], stonk['bought_price'] , stonk['price'] , str(round(stonk['percent_increase_pr_turn'] - 100 , 2 ))+'%' , stonk['price_history'] ))

        print("")
        print("0   Exit the menu")
        print("____________________________________________________________________________________")
        white_space(2)
        numba = option_number(player)
        if numba == None or numba == -1:
            print(" You did nothing. ")
            return stonk_menu(player)
        else:
            for enum,stonk in enumerate(stonks_list):
                if enum == numba:
                    stonk = stonks_list[enum]
                    stonk['owner'] = None
                    players[player]['Wallet'] += stonk['price']
                    players[player]['Stonks'].remove(stonk)
                    profit = stonk['price']-stonk['bought_price']
                    print("")
                    print("  You have sold the {} for {}$.   P/L:{}$".format(stonk['name'],stonk['price'], profit ))
                    print("")
                    stonk['bought_price'] = int(stonk['price'])

                    if profit >= 0:
                        play("trump_shiney.wav")
                    else:
                        play("why_are_you_gay.wav")

                    input("  Press Enter to return to stonk menu ...")

    return stonk_menu(player)

def ensure_crypto_stays_crypto():
    for stonk in stonks_list:
        if stonk['name'] in ['Bit Coin', 'Ethereum','Doge Coin']: # crypto list
            stonk['phase'] = phase_crypto
            stonk['phase_number'] = 4



def stonk_update_every_round():
    # Updates the stonk price depending on its "phase"
    # if stonk price < lowerbound: 
    #   stonk price = lowerbound
    # Have the phase in the dictionary of the stonk
    # if stonk reaches var(stonk_max_value) in stonk['price']

    # Order stocks such that they are pretty...

    for player in playersorder:
        cur_stock_list = players[player]['Stonks']
        ordered_stock_list = [stock for stock in stonks_list if stock in cur_stock_list ]
        players[player]['Stonks'] = ordered_stock_list

    for stonk in stonks_list:
        if len(stonk['price_history']) >= 8 :
            stonk['price_history'] = stonk['price_history'][-5:]

        if stonk_dist == "normal":
            phase1 = round(rn.normalvariate(phase1_mean , phase1_std) ,3)         # random float with a 3 decimal place
            phase2 = round(rn.normalvariate(phase2_mean , phase2_std) ,3)
            phase3 = round(rn.normalvariate(phase3_mean , phase3_std) ,3)
            phase_crypto = round(rn.normalvariate(phase_crypto_mean , phase_crypto_std) ,3)
        else:    # Note:  if stonk_dist == "uniform":
            phase1 = round(rn.uniform(phase1_bound[0],phase1_bound[1]) , 3)         # random float with a 3 decimal place
            phase2 = round(rn.uniform(phase2_bound[0],phase2_bound[1]) , 3)
            phase3 = round(rn.uniform(phase3_bound[0],phase3_bound[1]) , 3)
            phase_crypto = round(rn.uniform(phase_crypto_bound[0],phase_crypto_bound[1]) , 3)   

        if stonk['phase_number'] == 1:
            stonk['phase'] = phase1
        if stonk['phase_number'] == 2:
            stonk['phase'] = phase2
        if stonk['phase_number'] == 3:
            stonk['phase'] = phase3
        if stonk['phase_number'] == 4:
            stonk['phase'] = phase_crypto

        old_price = stonk['price']

        if (stonk['price'] < (bound_for_volatile_stonks//2)) and stonk['name'] not in ['Bit Coin', 'Ethereum','Doge Coin']:
            # Penny stonk go boom, avoid crypto cause its alrdy OP.
            stonk['price'] *= ((stonk['phase']**1.5) + 0.02)
        elif stonk['price'] < bound_for_volatile_stonks:
            # Small stonk, also go kinda boom
            stonk['price'] *= (stonk['phase']**1.2)
        elif stonk['price'] >= stonk_max_value//2:
            # Big stonk slow 
            stonk['price'] *= (stonk['phase']**0.8)
        else:
            # Normal stonk are normal
            stonk['price'] *= stonk['phase']

        stonk['price'] = int(stonk['price'])

        # print("old_price: ", old_price)
        # print("stonk['price']", stonk['price'])

        if stonk['price'] < stonk_minimum_value:
            stonk['price'] = int(stonk_minimum_value)
            
        elif stonk['price'] > stonk_max_value:
            stonk['price'] = int(stonk_drop_to_value)
        
        stonk['price_history'].append(int(stonk['price']))
        stonk['percent_increase_in_value'] = round(stonk['price']*100 /stonk['bought_price']  ,  1)
        stonk['percent_increase_pr_turn'] = round(stonk['price']*100 / old_price  ,  1)



def stonk_phase_change():
    global loan_interest
    global initial_loan_interest

    loan_interest = initial_loan_interest # Reset bank loan interest

    for stonk in stonks_list:
        
        
        if stonk_dist == "normal":
            phase1 = round(rn.normalvariate(phase1_mean , phase1_std) ,3)         # random float with a 3 decimal place
            phase2 = round(rn.normalvariate(phase2_mean , phase2_std) ,3)
            phase3 = round(rn.normalvariate(phase3_mean , phase3_std) ,3)
            phase_crypto = round(rn.normalvariate(phase_crypto_mean , phase_crypto_std) ,3)
        else:    # Note:  if stonk_dist == "uniform":
            phase1 = round(rn.uniform(phase1_bound[0],phase1_bound[1]) , 3)         # random float with a 3 decimal place
            phase2 = round(rn.uniform(phase2_bound[0],phase2_bound[1]) , 3)
            phase3 = round(rn.uniform(phase3_bound[0],phase3_bound[1]) , 3)
            phase_crypto = round(rn.uniform(phase_crypto_bound[0],phase_crypto_bound[1]) , 3)

        if stonk['name'] in ['Bit Coin', 'Ethereum','Doge Coin']: # crypto list
            stonk['phase'] = phase_crypto
            stonk['phase_number'] = 4
            stonk['price_history'] = [stonk['price']]
            continue # skip the last bit as it's only for stonks and not crypto

        phase_choice = rn.randint(1,3)
        if phase_choice == 1:
            stonk['phase'] = phase1
            stonk['phase_number'] = 1
        elif phase_choice == 2:
            stonk['phase'] = phase2
            stonk['phase_number'] = 2
        elif phase_choice == 3:
            stonk['phase'] = phase3
            stonk['phase_number'] = 3
        stonk['price_history'] = [stonk['price']]


    if sum([stonk['price'] for stonk in stonks_list])// len(stonks_list) <= stonk_max_value//5:
        # If average stonk value is above stonk_max_value/2, then pump up the Market BOI!
        for i in range(len(stonks_list) // 6):  
            # Add random phase 3 boiz in the market.
            stonk = rn.choice(stonks_list)
            while stonk['name'] in ['Bit Coin', 'Ethereum','Doge Coin']:
                stonk = rn.choice(stonks_list)
            stonk['phase'] = phase3
            stonk['phase_number'] = 3
    

    #stonk_update_every_round() # STONKS update once more during a phase_change

    # This call is placed in the start of every round too...
    print("")
    print("###################################### STONKS ##########################################################")
    print("")
    print("     $ $ $  PHASE CHANGE ! $ $ $")
    print("")
    print("     The stonks are now chaning their phase. They may each have one of three phases. ")
    print("")
    print("")
    if stonk_dist == 'normal':
        print("                                Phase Rates :")
        print("                                   phase 1 mean:",round((phase1_mean)*100, 1),"%  ,  phase 1 stdev:", round((phase1_std)*100, 1) , "%")
        print("                                   phase 2 mean:",round((phase2_mean)*100, 1),"%  ,  phase 2 stdev:", round((phase2_std)*100, 1) , "%")
        print("                                   phase 3 mean:",round((phase3_mean)*100, 1),"%  ,  phase 3 stdev:", round((phase3_std)*100, 1) , "%")
        print("                                   crypto  mean:",round((phase_crypto_mean)*100, 1),"%  ,  crypto  stdev:", round((phase_crypto_std)*100, 1) , "%")
    else:
        print("                                Phase Rates :")
        print("                                   phase 1 :",round((phase1_bound[0]-1)*100),"%  , ", round((phase1_bound[1]-1)*100) , "%")
        print("                                   phase 2 :",round((phase2_bound[0]-1)*100),"%  , ", round((phase2_bound[1]-1)*100) , "%")
        print("                                   phase 3 :",round((phase3_bound[0]-1)*100),"%  , ", round((phase3_bound[1]-1)*100) , "%")
        print("                                   crypto  :",round((phase_crypto_bound[0]-1)*100),"%  , ", round((phase_crypto_bound[1]-1)*100) , "%")
        
    print("")
    print("     All stonks will increase in price within the boundries of one of the phases!")
    print("     KEEP AN EYE ON THE YOUR stonkS PRICE HISTORY!")
    print("")
    print("    Tips for new people: ")
    print("        ")
    print("         1. Stonks take a random value decscribed above, and increase/decrease the price with some percent.")
    print("         2. Stonks that reach up to {}$ will crash down to {}$!".format(stonk_max_value,stonk_drop_to_value))
    print("         3. The stonk price ceiling is {}$ and the stonk price floor is {}$".format(stonk_max_value , int(stonk_minimum_value)))
    print("")
    print("")
    print("###################################### stonkS ##########################################################")
    print("")
    print("")
    print("")
    print("")
    input("   Press 'Enter' to continue ...")
    white_space(3)
    #print("   Here are some usefull stonk stats:")
    #for stonk in stonks_list:
    #    stonk
        

 

# Stonks Variables and Dictionaries

phase1_mean = (phase1_bound[0]+phase1_bound[1])/2     
phase2_mean = (phase2_bound[0]+phase2_bound[1])/2     
phase3_mean = (phase3_bound[0]+phase3_bound[1])/2     
phase_crypto_mean = (phase_crypto_bound[0]+phase_crypto_bound[1])/2

phase1_std = (phase1_mean - phase1_bound[0])/ 1.7       # 1.7 is an abritrary multiplier to determine a std.
phase2_std = (phase2_mean - phase2_bound[0])/ 1.7
phase3_std = (phase3_mean - phase3_bound[0])/ 1.7
phase_crypto_std = (phase_crypto_mean - phase_crypto_bound[0])/ 1.7

phase1 = round(rn.uniform(phase1_bound[0],phase1_bound[1]) , 2)
phase2 = round(rn.uniform(phase2_bound[0],phase2_bound[1]) , 2)
phase3 = round(rn.uniform(phase3_bound[0],phase3_bound[1]) , 2)
phase_crypto = round(rn.uniform(phase_crypto_bound[0],phase_crypto_bound[1]) , 2)

                                                                                                                                                                            
the_monopoly_stonk = {'name':'The Monopoly stonk' ,'price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None ,'price_history' : [], 'percent_increase_pr_round':0}
meat_industry_stonk = {'name':'Meat Industry stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value':1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
bank_stonk = {'name':'Bank stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value':1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0} 
tech_stonk = {'name':'Tech stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value':1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0} 
clothes_stonk = {'name':'Clothes stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
jewellery_store_stonk = {'name':'Jewellery store stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
sports_stonk = {'name':'Sports stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
food_chain_stonk = {'name':'Food Chain stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
gold = {'name':'Gold Commodity','price': stonk_start_value , 'phase': phase1 , 'phase_number':1 ,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
silver = {'name':'Silver Commodity','price': stonk_start_value , 'phase': phase1 , 'phase_number':1 ,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
platinum = {'name':'Platinum Commodity','price': stonk_start_value , 'phase': phase1 , 'phase_number':1 ,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
oil = {'name':'Oil Commodity','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
game_stonk = {'name':'Game Stonk','price': stonk_start_value , 'phase': phase1 , 'phase_number':1,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
bit_coin = {'name':'Bit Coin','price': stonk_start_value , 'phase': phase_crypto , 'phase_number':4,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
ethereum = {'name':'Ethereum','price': stonk_start_value , 'phase': phase_crypto , 'phase_number':4,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}
doge_coin = {'name':'Doge Coin','price': stonk_start_value , 'phase': phase_crypto , 'phase_number':4,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}

# bitch_coin = {'name':'Bitch Coin','price': stonk_start_value , 'phase': phase_crypto , 'phase_number':4,'bought_price':stonk_start_value , 'percent_increase_in_value': 1 , 'owner': None,'price_history' : [], 'percent_increase_pr_round':0}


stonks_list = [the_monopoly_stonk, meat_industry_stonk, bank_stonk,tech_stonk, clothes_stonk, jewellery_store_stonk
                ,sports_stonk, gold,silver,platinum, oil, food_chain_stonk, game_stonk , bit_coin, ethereum, doge_coin ]



###########################  STONKS END  ##########################################

        
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

    combined_networth =  int(sum([players[dude]['Networth'] for dude in playersorder]))

    player_lowest_networth = ""
    lowest_networth = 999999999
    for dude in playersorder:
        temp_networth = players[dude]['Networth']
        if temp_networth < lowest_networth:
            lowest_networth = temp_networth
            player_lowest_networth = dude


    time_diff = ( time.time() - start_time ) + loaded_time_diff
    if am_i_dead(player):
        return
    print("")
    print("                     {:<35}       ".format(player + "'s Positions"))
    print("")
    print(" #----------------------------------------------------------------------# ")
    print("    Round : {}                    Time played: {} hours  {} min  {} sec".format(players[player]['Turn'],
                int(time_diff//3600) , int((time_diff//60)%60) , int(time_diff%60 )))
    print("    {}'s Wallet      : ${:<6}".format(player, int(players[player]['Wallet'])) , '                                     Debt                  : ${}'.format(players[player]['Debt']))
    print("    {}'s Networth    : ${:<6}".format(player, int(players[player]['Networth'])) , '                                     Winning Condition     : ${}'.format(winning_condition_amount))
    if type(board_placement[players[player]['Placement']]) == str:
        name_loc = board_placement[players[player]['Placement']]
    else: 
        name_loc = board_placement[players[player]['Placement']]['name']
    cur_place = [name_loc , "  tile number:", players[player]['Placement']]
    print("    {}'s Placement   : {:<22}{}{:<2}".format(player, cur_place[0],cur_place[1],cur_place[2]) , "      Wealth in circulation : ${} ".format(combined_networth))
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
    print("    __________  {}'s Stonks  __________  amount:({}/{})  ".format(player ,len(players[player]['Stonks']) , len(stonks_list )))
    print("")
    for stonk in players[player]['Stonks']:
        print("   {:<23}:  Price: ${:<5}  Bought Price: ${:<5}  P/L: ${:<6} IPR: {:<6}  history: {}".format( stonk['name'] ,
        stonk['price']  , stonk['bought_price'], str(int(stonk['price'] - stonk['bought_price'])) , str(round(stonk['percent_increase_pr_turn'] - 100 ,1 ))+'%'  , stonk['price_history']  ))
    print("")
    if len(players[player]['Stonks']) >= 2:
        print("   {:<23}:  Price: ${:<5}  Bought Price: ${:<5}  P/L: ${:<6} IPR: {:<6.2f}% ".format( "Combined Stonks Value" 
                        ,  sum([ stonk['price'] for stonk in players[player]['Stonks']])
                        , sum([ stonk['bought_price'] for stonk in players[player]['Stonks']])
                        , sum([ (int(stonk['price'] - stonk['bought_price'])) for stonk in players[player]['Stonks']])
                        , sum([round(stonk['percent_increase_pr_turn'] - 100 ,1 )*int(stonk['price']) 
                            for stonk in players[player]['Stonks']])/sum([ stonk['price'] for stonk in players[player]['Stonks']])  
                        ))
        print("")
    if len(players[player]['Derivatives']) >= 1:
        for deriv in players[player]['Derivatives']:
            print("    __________  {}'s Derivatives  __________    ".format(player))
            print("")
            print("  Premium: ${}  Player: {}  RRT: {}  TRT: {}  Potential Payoff: ${}  In the money: {}".format(
                deriv['premium'] , deriv['player'], deriv['remaing_run_time'], deriv['runtime'], 
                deriv['potential_gain'], player_lowest_networth == deriv['player']
            ))
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
        broke_af(player) 
        if am_i_dead(player):
            return
        white_space(1)
        card_price = 150 + players[player]['Turn']*5
        if card_price > 300:
            card_price = 300

        print("       # # # # # End of Turn Menu # # # # #                            PLAYER:  {}".format(player))
        print("")
        print("          {}'s Wallet: ${}".format(player,int(players[player]['Wallet'])))
        print("")
        print("___________________________________________________________________")
        print("")
        print("  1. Mortgage/un-mortgage property")
        print("  2. Trade with player ")
        print("  3. Upgrade property")
        print("  4. Enter the Dank Bank of 'Murica")
        if len(playersorder) > 1:
            #if (players[player]['Turn'] + playersorder.index(player)) % len(playersorder) == 0:
            if (players[player]['Turn'] + playersorder.index(player)) % 2 == 0:                         # testing this option out.
                print("  5. Buy a Lucky Card  for",card_price,"$")
                print("  6. Buy or sell Stonks")

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
            bank_loan_menu(player)

        elif option == '5' or option == '5.':
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
        elif option == '6' or option == '6.':
            if (players[player]['Turn'] + playersorder.index(player)) % 2 == 0:
                stonk_menu(player)
            else:
                print("  You can't buy or sell stonks this turn ....")
        else:
            pass
        
        if not am_i_dead(player):
            end_turn_menu_used = True
            end_turn_menu(player)
    
    else:
        return


def not_enough_money_message():
    white_space(3)
    print("   You don't have enough money to do that $ $ $  :( ")
    white_space(3)

def one_turn(player):
    global chace_card_turn_counter

    #for i in range(7):
    #    drag_all_levels_by_1()
    #    bump_all_levels_by_1()
    ensure_crypto_stays_crypto()
    require_loan_payment(player) # Get that cash back to the bank.
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

    ensure_crypto_stays_crypto()
    checking_swaps(player)
    winning_condition(player)
    players[player]['Turn'] += 1
    chace_card_turn_counter = 0
    save_game_pickle()      # Saves game automatically.
    white_space(35)



def am_i_dead(player): 
    if players[player]['Lives'] <= 0:
        return True
    elif players[player]['Lives'] > 0:
        return False    


def sell_property(player, prop):
    if prop['mortgaged'] == False:
        players[player]['Wallet'] += int(prop['price'])
        prop['owner'] = None
        players[player]['Property'].remove(prop)

    else:
        prop['mortgaged'] = False
        players[player]['Wallet'] += int(prop['price']*0.5)
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
                    print("{:<2}  {:<25} sell for: ${:<5}   level: {:<2}   rent: ${:<4}   color: {:<7}  mortgaged: {}".format(enum+1 , prop['name'], int(prop['price']),
                               prop['level'] , prop['rent'] , prop['color'], prop['mortgaged'] ))
                else:
                    print("{:<2}  {:<25} sell for: ${:<5}   level: {:<2}   rent: ${:<4}   color: {:<7}  mortgaged: {}".format(enum+1 , prop['name'], int(prop['price']*0.5) , 
                                prop['level'] , prop['rent'] , prop['color'] , prop['mortgaged']))
                    
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


def bank_loan_menu(player):
    global loan_interest
    global avg_networth
    round_nr = players[player]['Turn']
    dankness_activated = False
    #players[player]['Debt'] 
    #players[player]['Loan_terms_left']
    max_loan = int(2000 * ((round_nr)//10))

    if max_loan <= 0: 
        print("  You are not eligible to obtain a loan yet.")
        print("  Wait for round {} to use the loan function".format(10)) #hardcoded for now, i'm tired...
        print("")
        return 

    networth_threshold = int(avg_networth * 1.2)

    if players[player]['Networth'] < (networth_threshold * 0.5):
        max_loan *= 2
        dankness_activated = True

    if (players[player]['Networth'] > (networth_threshold) ) and (players[player]['Loan_terms_left'] == 0):
        print("  You seem thirsty... Wanna make some more gainz?")
        print("  Well this bank makes no sense and only lends money to people below the Networth")
        print("  threshold of: ${}  which is {}% more than the average networth".format(networth_threshold, 20))
        print("  In other words, players who dominate in terms of networth are not welcome...")
        print("")
        return 

    print("")
    
    print('         _._._                       _._._      ')        
    print('        _|   |_                     _|   |_         ')        
    print('        | ... |_._._._._._._._._._._| ... |         ')      
    print('        | ||| |   o  DANK  BANK  o  | ||| |         ')    
    print('        | """ |  ""   \'MURICA   ""  | """ |         ')    
    print('   ())  |[-|-]| [-|-]  [-|-]  [-|-] |[-|-]|  ())    ')         
    print('  (())) |     |---------------------|     | (()))   ')          
    print(' (())())| """ |  """    """    """  | """ |(())())  ')           
    print(' (()))()|[-|-]|  :::   .-"-.   :::  |[-|-]|(()))()  ')           
    print(' ()))(()|     | |~|~|  |_|_|  |~|~| |     |()))(()  ')           
    print('    ||  |_____|_|_|_|__|_|_|__|_|_|_|_____|  ||     ')        
    print(' ~ ~^^ @@@@@@@@@@@@@@/=======\@@@@@@@@@@@@@@ ^^~ ~  ')           
    print('      ^~^~                                ~^~^      ')       


    print("")
    print("  DANK BANK OF 'MURICA loan menu")
    if dankness_activated:
        print("  ")
        print("  DANK LOANS activated! This is because your networth is under half the networth threshold!!!")
    print("")
    print("  Loans can only be obtained, while a player has $0 debt.")
    print("  The loan value is payed directly, or over a period of 12 terms.")
    print("  The first 2 turns the player pays nothing, while the remaining 10 turns, the players are forced to pay off their debt.")
    print("  The interest is multiplied to the remaining debt each turn, and a single time as an entry fee when the loan is obtained.")
    print("  Loan Status: ")
    print("") 

    if players[player]['Loan_terms_left'] == 0:
        # Eligible to obtain loan
        # Make maximum bank loan'
        print("  Networth threshold: ${}  Current Networth: ${}".format(networth_threshold, int(players[player]['Networth'])))
        print("  Maximum loan value: ${}".format(max_loan))
        print("  Interest pr. round: {}%".format(int(100*(loan_interest - 1))))    
        print("  Maximum loan cost : ${}".format(int(max_loan*(loan_interest**13)))) # 13 because 1 term is added as loan fees
        print("")
        print("  How much would you like to borrow?")
        print("")
        loan_amount = input() 

        if loan_amount in ("" or " "):
            print("\n \n  You didn't borrow any money.")
            return
        
        loan_amount = int(loan_amount)

        if loan_amount < 0:
            print("")
            print("  Ahhh... You think my retarded ass didn't think about how you can abuse")
            print("  compound interest for your benefit... Think again scrub...")
            print("")
            print("  Your negative loan value was turned positive")
            print("")
            loan_amount = abs(loan_amount)

        if loan_amount > max_loan:
            loan_amount = max_loan

        print("\n \n  You borrowed: {}".format(loan_amount))
        play("small-loan-of-a-million-dollars.wav")
        time.sleep(0.5)
        players[player]['Debt'] = int(loan_amount * loan_interest) # multiply debt with 1 loan_interest as start fee
        players[player]['Wallet'] += int(loan_amount)
        players[player]['Loan_terms_left'] = 12
        
    else: 
        # show player loan stats 
        # Let players pay debt off
        print("")
        print("  Wallet: ", players[player]['Wallet'])
        print("  You have an active loan with ${} left to pay, with {} turns left to pay it off.".format(players[player]['Debt'], players[player]['Loan_terms_left']))
        print("")
        pay_off_amount = input("  Enter the amount to pay off debt:")
        print("pay_off_amount:", pay_off_amount)
        if pay_off_amount in ("" or " "):
            return
        elif type(eval(pay_off_amount)) == int: 
            pay_off_amount = int(pay_off_amount)
            if enough_money_to_buy(player,pay_off_amount):
                if pay_off_amount >= players[player]['Debt']:
                    pay_off_amount = players[player]['Debt']
                    print("")
                    print("pay_off_amount was larger than debt, new pay_off_amount: ${}".format(pay_off_amount))
                    print("")
                pay_off_amount = int(pay_off_amount)
                players[player]['Debt'] -= pay_off_amount
                players[player]['Wallet'] -= pay_off_amount
                if players[player]['Debt'] == 0:
                    players[player]['Loan_terms_left'] = 0
                    players[player]['Debt'] == 0
                     

            else:
                not_enough_money_message()
        else:
            pass

        print("")
        print("")
        print("  Your remaining debt is now ${} with {} turns left to pay off.".format(players[player]['Debt'], players[player]['Loan_terms_left']))
        return
        


def require_loan_payment(player):
    global loan_interest

    if players[player]['Loan_terms_left'] <= 0:
        return
    else:
        players[player]['Loan_terms_left'] -= 1
        if players[player]['Loan_terms_left'] == 0:
            return
        players[player]['Debt'] = int(players[player]['Debt'] * loan_interest)
        

        if players[player]['Loan_terms_left'] <= 10:
            if players[player]['Loan_terms_left'] == 1:
                payment = int(players[player]['Debt'])
            else:
                # some economist help me with a rational fomula for uniform payments.
                # For now, the players just pays slightly less throughout the loan, with a peak at round 10
                payment = int(players[player]['Debt'] * (loan_interest**players[player]['Loan_terms_left']) // players[player]['Loan_terms_left'])

        else:
            payment = 0
        # require payment.
        players[player]['Debt'] -= int(payment)
        players[player]['Wallet'] -= int(payment) 
        
        
    




def upgrade_menu(player):
    global rates_profile
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
                    if   prop['side'] == 'South' : rate_bracket = rates_profile[0]
                    elif prop['side'] == 'West'  : rate_bracket = rates_profile[1]
                    elif prop['side'] == 'North' : rate_bracket = rates_profile[2]
                    elif prop['side'] == 'East'  : rate_bracket = rates_profile[3]
                    else: pass # should never happen as all sides are defined.
                    
                    # if a prop is level 3, future level is 4, and the index for that is 2
                    # if a prop is level 1, future level is 2, and the index for that is 0
                    future_level_index = prop['level'] - 1 
                    if future_level_index > 3:
                        future_level_index = 3  # max rent rate 
                    
                    future_rent = int(prop['rent'] * rate_bracket[future_level_index])
                    print("{:<2} {:<25} {:<10} upgrade price: {:<4}$     current level: {:<2}     rent: {:<4}$  next rent: ${:<4}".format(enum+1 ,prop['name'], prop['color'],
                                                            int(prop['price']*upgrade_multiplier), prop['level'], prop['rent'] , future_rent)  )
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
                    print("{:<2}  {:<25}  mortgage for: ${}  level: {}   rent: ${}   color: {}:".format(enum+1 , prop['name'], int(prop['price']*0.5) , 
                                prop['level'] , prop['rent'] , prop['color'] ))
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

    if (players[player]['Networth'] < 0) and (players[player]['Lives'] == 2) and(redepemtion_reward):
        players[player]['Wallet'] = start_money
        print("     {}, you are incredible...".format(player))
        print("                                                   ______________________________________________________________________ ")
        print("     You hit rock bottom...                       |                                                                      |    ")
        print("                                                  | ==================================================================== |    ")
        print("                                                  | |%/^\\%&%&%&%&%&%&%&%&{ Federal Reserve Note }%&%&%&%&%&%&%&%&//^\% | |    ")
        print("                                                  | |/inn\)===============------------------------===============(/inn\| |    ")
        print("                                                  | |\|UU/      $ $ $ MONEY THAT MEANS NOTHING AT ALL $ $ $       \|UU/| |    ")
        print("                                                  | |&\-/     ~~~~~~~~   ~~~~~~~~~~=====~~~~~~~~~~~  P8188928246   \-/&| |      ")
        print("     Redemption! you now have 1                   | |%//)  ___ ___   ___   ____    ___   ____   ___   _      __ __ (\\% | |    ")
        print("     life left                                    | |&(/  |   |   | /   \ |    \  /   \ |    \ /   \ | |    |  |   |\)&| |    ")
        print("                                                  | |%\\   | _   _ ||     ||  _  ||     ||  o  )     || |    |  |   |//%| |    ")
        print("     Everyone else looses their                   | |&\\\  |  \_/  ||  O  ||  |  ||  O  ||   _/|  O  || |___ |  ~   |//&| |    ")
        print("     redemption chance                            | |%\\)  |   |   ||     ||  |  ||     ||  |  |     ||     ||___,  |//%| |    ")
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
        input("  Press Enter to continue ... ")
        white_space(3)
        update_networth()
        for dude in playersorder:
            players[dude]['Lives'] = 1

    if players[player]['Wallet'] < 0:
        white_space(10)
        update_rent()
        while players[player]['Networth'] > 0 and players[player]['Wallet'] < 0:
            update_rent()
            player_stonk_val = 0
            player_mortg_val = 0
            player_sell_val = 0

            for stonk in players[player]['Stonks']:
                player_stonk_val += stonk['price']
            for prop in players[player]['Property']:
                if prop['mortgaged']:
                    player_sell_val += ( prop['price'] / 2)
                else:
                    player_mortg_val += ( prop['price'] / 2)
                    player_sell_val += ( prop['price'] )

            player_stonk_val = int(player_stonk_val)
            player_mortg_val = int(player_mortg_val)
            player_sell_val = int(player_sell_val)

            print("")
            print("")
            print("       # # # # # Broke Menu # # # # #")
            print("")
            print("")
            print("          You need to sell/mortgage some of your stuff!")
            print("          {}'s Wallet: ${}".format(player,players[player]['Wallet']))
            print("")
            print("___________________________________________________________________")
            print("")
            print("  1. Mortgage Property        value: ${}".format(player_mortg_val))
            print("  2. Sell Property            value: ${}".format(player_sell_val))
            print("  3. Sell Stonks              value: ${}".format(player_stonk_val))
            print("")
            print("  0. or 'Enter' to Exit")
            print("")
            print("___________________________________________________________________")
            
            play("oof.wav")

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
                stonk_menu(player)
                    
            
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
            print("     {}'s Wallet: ".format(player) , '${}'.format(players[player]['Wallet']))
            print("     {}'s Networth: ".format(player) , '${}'.format(players[player]['Networth']))
            print("     ")
            print("")
            print("    You LOST and you are now out of the game because you're broke. ")
            white_space(12)
            print("     ")
            play("he-fucked-up.wav")
            play("trump_bye.wav")
            play("mario_game_over.wav")

            input("  Pres Enter to continue ... ")

            player_lost_check_swaps(player)

            del playersorder[playersorder.index(player)]
            for prop in All_property_list:
                if prop['owner'] == player:
                    prop['owner'] = None
                    prop['mortgaged'] = False
            # CHANGE ALL OWNED PROPERTY TO "owner": None.
        
            return         
            
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
        print(" Property market levels are: 15,25,35,45,...")
        print("")


    lottery_wallet += 50

    if roundcount % phase_change_rounds == 0:
        stonk_phase_change()
    stonk_update_every_round()
    
    for player in playersorder:
        one_turn(player)
        winning_condition(player)


def mortgage_property(player, prop):
    if prop['mortgaged'] == False:
        players[player]['Wallet'] += int(prop['price']/2)
        prop['mortgaged'] = True
    # Changing rent to 0 for mortgaged property is done in the top of the update_rent() function.


def un_mortgage_property(player, prop):
    if prop['mortgaged'] == True:
        players[player]['Wallet'] -= int(prop['price']/2  +  prop['price']*0.1)     # 10% extra for the bank.
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
        print("   {}'s Wallet: ${}   ".format(person,players[person]['Wallet']))
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

        for stonk in players[player]['Stonks']:
            temp_networth += stonk['price']
        
        temp_networth -= players[player]['Debt']

        players[player]['Networth'] = temp_networth
        avg_networth += temp_networth
    
    avg_networth = avg_networth / len(playersorder)


def update_rent(): 

    global rates_profile
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
    print("  {}'s wallet : ${}".format(player, players[player]['Wallet']))
    print("  {}'s wallet : ${}".format(receiver, players[receiver]['Wallet']))
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
        play("Conga Roll.wav")
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

        sound = rn.choice(["Borat - Wawaweewa", "borat bang bang skeet skeet", "borat-great-success", "borat-its-a-very-nice", "borat-very-nice1", "borat-very-nice2"]) # Borat sounds
        play(sound + ".wav")
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
        play("lego-yoda-death-sound-effect.wav")
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
    play(rn.choice(["epic_victory_win.wav", "gangsta_paradise_keif.wav"]))
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
- Check buy stonk. Couldn't buy stonk for 454 even though i had 460. 


 

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
- Stonks implimented and working 
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

- Stonks Ideas (Implimented):
        There are three stonks in the game. They can each have one of the behaviors.
        These behaviors change every 5 rounds.
        1. has an expected value which is greater than 1         E(X) = 1.1 pr. turn
        2. has an expected value which is a little less than 1   E(X) = 0.95 pr. turn
        3. has an expected value which is sligtly greater than 1             E(X) = 1.02 pr. turn
        These three attributes shift every 5 turns, and nobody knows what is what, just like IRL.
        Do this with a uniform distribution of +-0.2 from the expected value.
        Stonk_minimum value = start_value

- Option for names and custom tiles
- names
- same price option
- different settings
- temaer, klubber og bar
- drugz and cartels
- gaming referencer

- lav aktie paa index fond

- abilities and upgrades for properties (brothels, drugs, cartel, mafia, shit like that)

- choose option at each property, with some sort of financial consequences, or jail because of actions
- these options could be go out expensive, cheap night out, focus on business, etcæ
- prices are defined by the upgrades of the property
- you pay the person owning the club.

- implement aktie skat, der gaar til free parking

- implement history for combined stonks value


BUGS: 


Fixed:
    (FIXED) - Don't let players in Jail get a chance card, even if they're the poorest.
    (FIXED) - cant exit sell menu if broke -_-
    (FIXED)-  Fix price history with stonks when loading in a game.
    (FIXED) - Remove Free park from Location icon
    (FIXED) - Change the random chance card to happen if and only if it is the poorest players turn. 
    (FIXED) - When mortgaging properties, a recursive loop happens, forcing the player to press enter multiple times, equal to the amount of properties morgaged whilst in that menu.





"""

if __name__ == "__main__":
    #Someone who was judging me was looking dirty at me, so i had to if main is name
     
    start_the_game()
