# The purpose of this code is to win the Skillz 2022 coding competition
# Creators: Ben Solomovitch, Ron Bar-El, Yael Meshar, Yegor Stolyarsky
# 01.2022 - ?

# modules we are allowed to import, don't add other imports!!


from penguin_game import *

# import collections
# import operator
import random


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
        print "THAT'S A PROBLEM!"  # TODO: potential fail here
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
        print "THAT'S A PROBLEM!"  # TODO: potential fail here
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


def yael(game, ices_not_attack):
    '''
    The function chooses the best combination of attacking-attacked icebergs
    :param game
    :type :
    :return:
    :rtype:
    '''
    maxes = []
    for my_iceberg in game.get_my_icebergs():
        # if my_iceberg not in ices_not_attack:

        if not [ene_pg for ene_pg in game.get_enemy_penguin_groups() if ene_pg.destination == my_iceberg]:
            if my_iceberg.penguin_amount > 30:
                enemies_list = [ice for ice in game.get_enemy_icebergs() if
                                my_iceberg.penguin_amount - enemy_penguins_at_arrival(game, my_iceberg, ice) > 0]
                # enemy penguin amount can't be negative
                # TODO: to consider collisions
                if enemies_list:
                    maxim = max(enemies_list, key=lambda x: my_iceberg.get_turns_till_arrival(x) / (
                            my_iceberg.penguin_amount - enemy_penguins_at_arrival(game, my_iceberg, x)))
                    maxes.append((my_iceberg, maxim, my_iceberg.get_turns_till_arrival(maxim) / (
                            my_iceberg.penguin_amount - enemy_penguins_at_arrival(game, my_iceberg, maxim))))

    # print maxes
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
            print ice_a.get_turns_till_arrival(ice_b)


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
    # print yegor_list
    return sorted(yegor_list, key=lambda x: x[1], reverse=True)


def help_barel(game, iceberg_in_trouble):
    owner = 1

    attackers = [(-ene.penguin_amount, ene.turns_till_arrival) for ene in game.get_enemy_penguin_groups() if
                 ene.destination == iceberg_in_trouble]
    defenders = [(my.penguin_amount, my.turns_till_arrival) for my in game.get_my_penguin_groups() if
                 my.destination == iceberg_in_trouble]
    attackers.extend(defenders)
    attackers.sort(key=lambda x: x[1])
    print iceberg_in_trouble.penguin_amount, attackers

    warning_list = []
    real_amount = iceberg_in_trouble.penguin_amount
    pg_groups = attackers
    enemy_pgs = [enemy_pg for enemy_pg in game.get_enemy_penguin_groups() if enemy_pg.destination == iceberg_in_trouble]
    sum_closest = 0
    while pg_groups:
        closest_distance = pg_groups[0][1]
        sum_closest += closest_distance
        pg_groups = [(pg[0], pg[1] - closest_distance) for pg in pg_groups]

        pg_arrived = [pg[0] for pg in pg_groups if pg[1] == 0]
        pg_groups = pg_groups[len(pg_arrived):]
        sum_pg_arrived = sum(pg_arrived)
        real_amount += iceberg_in_trouble.penguins_per_turn * closest_distance + sum_pg_arrived
        if real_amount <= 0:
            # warning_list[sum_closest] = warning_list.get(sum_closest, 0) + (-1 * real_amount + 1)
            warning_list.append((-1 * real_amount + 1, sum_closest))

            # add collisions

    return warning_list


def send_help(game):
    defence_succeed = []
    warning_lists = create_warning_lists(game)
    print warning_lists
    if warning_lists:
        warning_lists.sort(key=lambda x: yegortziahu(game, x[0]), reverse=True)
        for ice_to_defend, ice_warnings in warning_lists:
            for needed_amount, time_to_deliever in ice_warnings:  # in sorted(ice_warnings.items(), key=lambda x: x[0]):
                possible_defenders = []
                for my in game.get_my_icebergs():
                    if ice_to_defend.get_turns_till_arrival(my) <= time_to_deliever and ice_to_defend != my:
                        sum_ene_pg = sum([ene_pg.penguin_amount for ene_pg in game.get_enemy_penguin_groups() if
                                          ene_pg.destination == my])
                        if my.penguin_amount - sum_ene_pg > 20:  # this was 5!!! any num larger than 5 worked so far. on 5 Code Frozen crashed
                            possible_defenders.append(my)

                # possible_defenders.sort(lambda x: yegortziahu(game, x[0]))
                if possible_defenders:
                    sum_of_defenders = sum([my.penguin_amount for my in possible_defenders])
                    print "sum_of_defeners:", sum_of_defenders
                    print "len(possible_defenders):", len(possible_defenders)
                    if sum_of_defenders >= needed_amount:
                        defence_succeed.append(ice_to_defend)
                        for ice in possible_defenders:
                            ratio = float(ice.penguin_amount) / float(sum_of_defenders)
                            amount_to_send = int(ratio * needed_amount) + 1
                            if ice.penguin_amount < amount_to_send:
                                print "ice.penguin_amount < amount_to_send"
                                amount_to_send -= 1
                            ice.send_penguins(ice_to_defend, amount_to_send)
                            print "ratio:", str(ratio)
                            print "amount_to_send:", str(amount_to_send)

    return defence_succeed


def create_warning_lists(game):
    ice_list = [(ice, help_barel(game, ice)) for ice in game.get_my_icebergs()]
    return [w_l for w_l in ice_list if w_l[1]]


def benzion(game):
    if len(game.get_all_icebergs()) != 10 or len(game.get_my_icebergs()) != 1 or len(game.get_enemy_icebergs()) != 1:
        return False
    if game.get_my_icebergs()[0].penguin_amount != 21 or game.get_enemy_icebergs()[0].penguin_amount != 21:
        return False
    if game.get_my_icebergs()[0].get_turns_till_arrival(game.get_enemy_icebergs()[0]) != 29:
        return False

    neutral_dictionary = {[8, 11, 11, 14, 15, 15, 17, 22, 24]: 2, [7, 11, 11, 13, 15, 16, 17, 22, 24]: 2,
                          [6, 6, 7, 9, 11, 14, 14, 16, 17]: 2, [6, 6, 8, 9, 11, 11, 13, 15, 19]: 2}

    amount_dictionary = {[8, 11, 11, 14, 15, 15, 17, 22, 24]: 10, [7, 11, 11, 13, 15, 16, 17, 22, 24]: 10,
                         [6, 6, 7, 9, 11, 14, 14, 16, 17]: 20, [6, 6, 8, 9, 11, 11, 13, 15, 19]: 15}

    for ice in game.get_neutral_icebergs():
        this_list = icebergs_distances(game, ice, 'neutral')
        counter = 0
        for key, value in neutral_dictionary:
            counter += 1
            if key == this_list and ice.penguin_amount == amount_dictionary[key]:
                value -= 1
                if value == 0:
                    del neutral_dictionary[key]
                break
        if counter == 4:
            return False

    return True


def dist_from_enemy(game, my_iceberg):
    enemy_icebergs = game.get_enemy_icebergs()
    if enemy_icebergs:
        return sum([my_iceberg.get_turns_till_arrival(ice) for ice in enemy_icebergs]) / len(enemy_icebergs)
    else:
        return 0


def dist_from_my(game, my_iceberg):
    my_icebergs = game.get_my_icebergs()
    if len(my_icebergs) > 1:
        return sum([my_iceberg.get_turns_till_arrival(ice) for ice in my_icebergs if my_iceberg != ice]) / (
                    len(my_icebergs) - 1)
    else:
        return 0


def do_turn(game):
    """
    Makes the bot run a single turn

    :param game: the current game state
    :type game: Game
    """
    # if benzion(game):
    #    print "Benzion works!!!"
    # else:
    #    print "Benzion is tired :("

    print "TURN:", game.turn
    print "iceberg_values:", iceberg_values(game)
    print yegor_yael(game)
    # print get_all_distances(game)
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
    elif game.turn == 280 and len(game.get_neutral_icebergs()) == 2:  # THIS IS BAD!
        attacking_ice = game.get_my_icebergs()[0]
        possible_targets = [enemy_ice for enemy_ice in game.get_enemy_icebergs() if enemy_ice.penguin_amount < 3]
        if len(possible_targets) > 3:
            target_ice = possible_targets[3]
            if attacking_ice.can_send_penguins(target_ice, 3):  # game's can_send, not our function!
                attacking_ice.send_penguins(target_ice, 3)
    elif game.turn > 22:
        def_ices = send_help(game)
        print "ices were defended:", def_ices
        if not def_ices and sum([ice.penguins_per_turn for ice in game.get_enemy_icebergs()]) - sum(
                [ice.penguins_per_turn for ice in game.get_my_icebergs()]) > 0:
            for ice in game.get_my_icebergs():
                if ice.can_upgrade() and not [ene_pg for ene_pg in game.get_enemy_penguin_groups() if
                                              ene_pg.destination == ice] and not ice.already_acted:
                    ice.upgrade()
                    def_ices.append(ice)
                    break
        """ # this code beats code frozen
        if not def_ices:
            if game.get_my_icebergs()[0].can_upgrade():
                game.get_my_icebergs()[0].upgrade()
                def_ices.append(game.get_my_icebergs()[0])
        """

        # if random.random() < 0.1:
        best_move = yael(game, def_ices)
        # print best_move
        if best_move is not None:
            # TODO: see why sends -17 penguins, hm
            if not best_move[0].already_acted:
                best_move[0].send_penguins(best_move[1],
                                           enemy_penguins_at_arrival(game, best_move[0], best_move[1]) + 1)

        # could be better with Yupik, Sid
        distances = [(ice, abs(dist_from_enemy(game, ice) - dist_from_my(game, ice))) for ice in game.get_my_icebergs()]
        distances.sort(key=lambda x: x[1])
        middle_ice = distances[0][0]
        print middle_ice
        # if sum([ice.penguins_per_turn for ice in game.get_enemy_icebergs()]) - sum([ice.penguins_per_turn for ice in game.get_my_icebergs()]) <= 0:
        for ice in game.get_my_icebergs():
            if ice != middle_ice and not [ene_pg for ene_pg in game.get_enemy_penguin_groups() if
                                          ene_pg.destination == ice] and not ice.already_acted:
                ice.send_penguins(middle_ice, middle_ice.penguins_per_turn)
                print "sent to the front:", ice, middle_ice.penguins_per_turn

        # (middle_ice.penguins_per_turn OR 1
        # what should be the number where the 5 is

# if our production is better dont do anythinh
