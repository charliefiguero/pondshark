#!/usr/bin/env python

"""
terminal app for poker stats
"""

import glob
import os
import random

import parser
import player

HAND_HISTORY_DIR_PATH = "/Users/charlesfiguero/Library/Application Support/PokerStarsUK/HandHistory/ToiletBaby"

def find_most_recent_file():
    list_of_files = glob.glob(HAND_HISTORY_DIR_PATH + '/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def print_game_player_stats(game):
    last_game_players = parser.get_players(game)

    player_names = last_game_players.keys()
    for name in player_names:
        p = player_cache[name]
        p.print_stats()

    print()

def shark_fact():
    shark_facts = [
    "sharks do not have bones",
    "shark skin feels like sandpaper",
    "most sharks have tongues"
    ]

    print()
    print(f"!!!SHARK FACTtack!!! : {shark_facts[random.randint(0,2)]}")
    print()

# init
parser = parser.Parser()
player_cache = {}

# get most recent game report
most_recent_file_path = find_most_recent_file()
lines = parser.get_lines(most_recent_file_path)
games = parser.get_games(lines)

# build/update player cache
for game in games:
    new_players = parser.parse_game(game)

    for player_name, player in new_players.items():
        if not player_name in player_cache.keys():
            player_cache[player_name] = player

        else:
            player_cache[player_name] += player

# print to screen
last_game = games[-1]
print_game_player_stats(last_game)
print(most_recent_file_path)
shark_fact()







