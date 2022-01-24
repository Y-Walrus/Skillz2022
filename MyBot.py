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

    # Go over all of my icebergs.
    for my_iceberg in game.get_my_icebergs():
        # The amount of penguins in my iceberg.
        my_penguin_amount = my_iceberg.penguin_amount  # type: int

        # If there are any neutral icebergs.
        if game.get_neutral_icebergs():
            # Target a neutral iceberg.
            destination = game.get_neutral_icebergs()[0]  # type: Iceberg
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
