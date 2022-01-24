# The purpose of this code is to win the Skillz 2022 coding competition
# Creators: Ben Solomovitch, Ron Bar-El, Yael Meshar, Yegor Stolyarsky
# 01.2022 - ?

# modules we are allowed to import, don't add other imports!!

from penguin_game import *


# import collections
# import operator
# import random
# import re
# import math
# import itertools
# import traceback
# import abc


# note that there are functions we are not allowed to use


def do_turn(game):
    """
    Makes the bot run a single turn

    :param game: the current game state
    :type game: Game
    """

    ''' # can be bad if our first iceberg is attacked
    if game.get_neutral_icebergs():
        ice = game.get_neutral_icebergs()[0]
    if 19 < game.turn <= 29:
        for neutral_iceberg in game.get_neutral_icebergs():
            if neutral_iceberg.id == 7:
                ice = neutral_iceberg
        game.get_my_icebergs()[0].send_penguins(ice, game.get_my_icebergs()[0].penguin_amount)
    if 22 < game.turn <= 29:
        for neutral_iceberg in game.get_neutral_icebergs():
            if neutral_iceberg.id == 7:
                ice = neutral_iceberg
        game.get_my_icebergs()[1].send_penguins(ice, game.get_my_icebergs()[1].penguin_amount)    
    '''

    if game.turn == 1:
        game.get_my_icebergs()[0].upgrade()
    elif game.turn == 7:
        game.get_my_icebergs()[0].send_penguins(game.get_neutral_icebergs()[0], 11)
    elif game.turn == 12:
        game.get_my_icebergs()[0].send_penguins(game.get_neutral_icebergs()[1], 11)
    elif game.turn == 19:
        for neutral_iceberg in game.get_neutral_icebergs():
            if neutral_iceberg.id == 7:  # what if we are on the other side of the map
                ice = neutral_iceberg
        game.get_my_icebergs()[0].send_penguins(ice, 13)  # consider sending each turn all production to the orange
    elif game.turn == 22:
        for neutral_iceberg in game.get_neutral_icebergs():
            if neutral_iceberg.id == 7:
                ice = neutral_iceberg
        game.get_my_icebergs()[1].send_penguins(ice, 5)
    elif game.turn > 46:
        """
        max_amount = 0
        ice = game.get_my_icebergs()[0]
        for my_iceberg in game.get_my_icebergs():
            if my_iceberg.penguin_amount > max_amount:
                max_amount = my_iceberg.penguin_amount
                ice = my_iceberg
        """
        for ice in game.get_my_icebergs():
            closest_enemy = game.get_enemy_icebergs()[0]
            min_dist = 100
            for enemy_iceberg in game.get_enemy_icebergs():
                if ice.get_turns_till_arrival(enemy_iceberg) < min_dist:
                    min_dist = ice.get_turns_till_arrival(enemy_iceberg)
                    closest_enemy = enemy_iceberg

            print(closest_enemy.level, closest_enemy.penguins_per_turn)
            if ice.penguin_amount > closest_enemy.penguin_amount + closest_enemy.penguins_per_turn * min_dist:
                # Send penguins to the target.
                print ice, "sends", (closest_enemy.penguin_amount + 1), "penguins to", closest_enemy
                ice.send_penguins(closest_enemy, closest_enemy.penguin_amount + 1)
        '''
        # Go over all of my icebergs.
        for my_iceberg in game.get_my_icebergs():
            # The amount of penguins in my iceberg.
            my_penguin_amount = my_iceberg.penguin_amount  # type: int

            # If there are any neutral icebergs.
            if game.get_neutral_icebergs():
                # Target a neutral iceberg.
                destination = game.get_neutral_icebergs()[0]  # type: Iceberg
                #destination = game.get_enemy_icebergs()[0]  # type: Iceberg
            else:
                # Target an enemy iceberg.
                destination = game.get_enemy_icebergs()[0]  # type: Iceberg

            # The amount of penguins the target has.
            destination_penguin_amount = destination.penguin_amount  # type: int

            # If my iceberg has more penguins than the target iceberg.
            if my_penguin_amount > destination_penguin_amount:
                # Send penguins to the target.
                print my_iceberg, "sends", (destination_penguin_amount + 1), "penguins to", destination
                my_iceberg.send_penguins(destination, destination_penguin_amount + 1)
        '''