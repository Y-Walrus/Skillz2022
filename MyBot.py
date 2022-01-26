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

def icebergs_distances(game, yegor_ice, team, lowest_to_highest=True):
    '''
    The function sorts all icebergs by distances from iceberg yegor_ice
    :param yegor_ice: The iceberg that we check the distances from.
    :type yegor_ice: Iceberg.
    :return: Icebergs sorted list
    :rtype: List of Iceberg
    '''

    if team == "all":
        icebergs = game.get_all_icebergs()

    elif team == "my":
        icebergs = game.get_my_icebergs()

    elif team == "enemy":
        icebergs = game.get_enemy_icebergs()

    else:
        print("THAT'S A PROBLEM!")  # TODO: potential fail here
    yegor_list = [ice for ice in icebergs if ice != yegor_ice]

    return yegor_list.sort(key=lambda x: yegor_ice.get_turns_till_arrival(x), reverse=lowest_to_highest)


def icebergs_amount(game, team, lowest_to_highest=True):
    '''
    The function sorts all icebergs by amount of penguins
    :param
    :type :
    :return:
    :rtype:
    '''

    if team == "all":
        icebergs = game.get_all_icebergs()

    elif team == "my":
        icebergs = game.get_my_icebergs()

    elif team == "enemy":
        icebergs = game.get_enemy_icebergs()

    else:
        print("THAT'S A PROBLEM!")  # TODO: potential fail here
    yegor_list = [ice for ice in icebergs]

    return yegor_list.sort(key=lambda x: x.penguin_amount, reverse=lowest_to_highest)


def enemy_penguins_at_arrival(game, my, enemy):
    amount = enemy.penguin_amount + enemy.penguins_per_turn * my.get_turns_till_arrival(enemy)
    for pg in game.get_my_penguin_groups():
        real_amount = pg.penguin_amount
        for ene_pg in game.get_enemy_penguin_groups():
            if pg.source == my and pg.destination == enemy and ene_pg.source == enemy and ene_pg.destination == my:
                real_amount -= ene_pg.penguin_amount
        if real_amount < 0:
            real_amount = 0
        if pg.destination == enemy:
            amount -= real_amount
    for pg in game.get_enemy_penguin_groups():
        if pg.destination == enemy:
            amount += pg.penguin_amount

    return enemy.penguin_amount + enemy.penguins_per_turn * my.get_turns_till_arrival(enemy)

    # or (pg.destination==my and pg.source==enemy):


def yael(game):
    '''
    The function
    :param
    :type :
    :return:
    :rtype:
    '''
    maxes = []
    for i, my_iceberg in enumerate(game.get_my_icebergs()):

        enemies_list = [ice for ice in game.get_enemy_icebergs() if
                        my_iceberg.penguin_amount - enemy_penguins_at_arrival(game, my_iceberg, ice) > 0]
        # enemy penguin amount can't be negative
        # TODO: to consider collisions
        if enemies_list:
            maxim = max(enemies_list, key=lambda x: my_iceberg.get_turns_till_arrival(x) / (
                    my_iceberg.penguin_amount - enemy_penguins_at_arrival(game, my_iceberg, x)))
            maxes.append((my_iceberg, maxim, my_iceberg.get_turns_till_arrival(maxim) / (
                    my_iceberg.penguin_amount - enemy_penguins_at_arrival(game, my_iceberg, maxim))))

    print(maxes)
    if maxes:
        return max(maxes, key=lambda x: x[2])
    else:
        return None


def do_turn(game):
    """
    Makes the bot run a single turn

    :param game: the current game state
    :type game: Game
    """

    # TODO: defend this code or change it
    if game.turn == 1:
        game.get_my_icebergs()[0].upgrade()
    elif game.turn == 7:
        game.get_my_icebergs()[0].send_penguins(game.get_neutral_icebergs()[0], 11)
    elif game.turn == 12:
        game.get_my_icebergs()[0].send_penguins(game.get_neutral_icebergs()[1], 11)
    elif game.turn == 19:
        for neutral_iceberg in game.get_neutral_icebergs():
            if neutral_iceberg.id == 7:
                ice = neutral_iceberg  # TODO: might not be assigned
        game.get_my_icebergs()[0].send_penguins(ice, 13)  # consider sending each turn all production to the orange
    elif game.turn == 22:
        for neutral_iceberg in game.get_neutral_icebergs():
            if neutral_iceberg.id == 7:
                ice = neutral_iceberg  # TODO: might not be assigned
        game.get_my_icebergs()[1].send_penguins(ice, 5)
    elif game.turn > 22:
        best_move = yael(game)
        print(best_move)
        if best_move != None:
            ene_peng_at_arr = best_move[1].penguin_amount + best_move[1].penguins_per_turn * best_move[
                0].get_turns_till_arrival(best_move[1])
            best_move[0].send_penguins(best_move[1], enemy_penguins_at_arrival(game, best_move[0], best_move[1]) + 1)
