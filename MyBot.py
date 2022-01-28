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
    """
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
    """
    return amount
    # return amount - works bad (which is probably logical)

    # or (pg.destination==my and pg.source==enemy):


def yael(game):
    '''
    The function chooses the best combination of attacking-attacked icebergs
    :param game
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

    # print(maxes)
    if maxes:
        return max(maxes, key=lambda x: x[2])
    else:
        return None


def yegor_yael(game):
    """
    Evaluates our situation in comparison to the enemy's situation
    :param: game
    :type: game
    :return: numEvaluate
    :rtype: penguin
    """
    my_penguins = sum([ice.penguin_amount for ice in game.get_my_icebergs()])
    my_penguins += sum([ice.penguin_amount for ice in game.get_my_penguin_groups()])

    enemy_penguins = sum([ice.penguin_amount for ice in game.get_enemy_icebergs()])
    enemy_penguins += sum([ice.penguin_amount for ice in game.get_enemy_penguin_groups()])

    my_production = sum([ice.penguins_per_turn for ice in game.get_my_icebergs()])
    enemy_production = sum([ice.penguins_per_turn for ice in game.get_enemy_icebergs()])
    my_penguins += my_production * 20
    enemy_penguins += enemy_production * 20

    return my_penguins - enemy_penguins


def get_all_distances(game):
    for ice_a in game.get_all_icebergs():
        for ice_b in game.get_all_icebergs():
            print(ice_a.get_turns_till_arrival(ice_b))


def yegortziahu(game, my_iceberg):
    if len(game.get_my_icebergs()) == 1:
        return 0
    else:  # TODO Check if amount penguins is relevant.
        return my_iceberg.penguin_amount + my_iceberg.penguins_per_turn * 20 - sum(
            [my_iceberg.get_turns_till_arrival(ice) for ice in game.get_my_icebergs() if my_iceberg != ice]) / (
                       len(game.get_my_icebergs()) - 1)
        # return my_iceberg.penguins_per_turn * 20 - sum(
        #    [my_iceberg.get_turns_till_arrival(ice) for ice in game.get_my_icebergs() if my_iceberg != ice]) / (
        #                   len(game.get_my_icebergs()) - 1)


def iceberg_values(game):
    my_icebergs = game.get_my_icebergs()
    yegor_list = [(ice, yegortziahu(game, ice)) for ice in my_icebergs]
    # print(yegor_list)
    return sorted(yegor_list, key=lambda x: x[1], reverse=True)


def help_barel(game, iceberg_in_trouble):
    owner = 1

    attackers = [(-ene.penguin_amount, ene.turns_till_arrival) for ene in game.get_enemy_penguin_groups() if
                 ene.destination == iceberg_in_trouble]
    defenders = [(my.penguin_amount, my.turns_till_arrival) for my in game.get_my_penguin_groups() if
                 my.destination == iceberg_in_trouble]
    attackers.extend(defenders)
    attackers.sort(key=lambda x: x[1])

    warning_list = []
    real_amount = iceberg_in_trouble.amount
    enemy_pgs = [enemy_pg for enemy_pg in game.get_enemy_penguin_groups() if enemy_pg.destination == iceberg_in_trouble]
    while enemy_pgs:
        attacking_amount = enemy_pgs[0].penguin_amount
        # add collisions
        for my_pg in game.get_my_penguin_groups():
            if my_pg.turns_till_arrival <= enemy_pgs[0].turns_till_arrival:
                attacking_amount -= my_pg
        if attacking_amount > 0:
            real_amount -= attacking_amount
            real_amount += iceberg_in_trouble.penguins_per_turn * enemy_pgs[0].turns_till_arrival  # minus what was already added
            if real_amount <= 0:
                warning_list.append((-1 * real_amount + 1, enemy_pgs[0].turns_till_arrival))
        enemy_pgs.pop(0)

    return warning_list

    """
    while attackers:
        real_amount += attackers[0][0] + owner * (attackers[0][1] * iceberg_in_trouble.penguins_per_turn)
        if real_amount < 0:
            return -real_amount
    """
    """
            owner *= -1
            real_amount *= -1
        attackers.pop(0)

    return real_amount * owner
    """


def help_barel_list(game):
    return [(ice, help_barel(game, ice)) for ice in game.get_my_icebergs()].sort(key=lambda x: x[1], reverse=True)


def request_help(game):
    # consider + instead of *, consider smth instead of sum
    yael_list = [(ice, -1 * sum([val[0] for val in help_barel(game, ice)]) * yegortziahu(game, ice),
                  -1 * help_barel(game, ice) + 1)
                 for ice in game.get_my_icebergs() if help_barel(game, ice) <= 0]
    yael_list.sort(key=lambda x: x[1], reverse=True)
    return yael_list


def do_turn(game):
    """
    Makes the bot run a single turn

    :param game: the current game state
    :type game: Game
    """
    print(iceberg_values(game))
    print(yegor_yael(game))
    # print(get_all_distances(game))
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
        """
        defenders_list = iceberg_values(game) # (ice, value)
        defenders_list.reverse()
        list_to_defend = request_help(game)  # (ice, value, needed_to_defend + ice.penguins_per_turn * )
        # TODO: consider defending more than one ice
        ice_to_defend = list_to_defend[0]
        defending_amount = 0
        while defending_amount < ice_to_defend[2]:
            defending_amount += defenders_list[0][0].penguin_amount
            defenders_list.pop(0)
        """

        best_move = yael(game)
        # print(best_move)
        if best_move is not None:
            # TODO: see why sends -17 penguins, hm
            best_move[0].send_penguins(best_move[1], enemy_penguins_at_arrival(game, best_move[0], best_move[1]) + 1)
# if our production is better dont do anythinh
