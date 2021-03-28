import player

class Parser():

    def get_lines(self, filepath, startbyte=0):
        """creates a list of lines starting from startbyte"""
        lines = []
        with open(filepath, 'rt') as reader:
            # for aline in reader:
            #     lines.append(aline)
            lines = reader.readlines()
                
        return lines

    def get_games(self, lines):
        list_of_games = []
        emptylist = True

        # ignore leading empty lines
        # while lines[0] == "":
        #     lines = lines[1:]

        # parse game
        game = []
        for line in lines:
            if line == "\n":
                continue

            if line.startswith("PokerStars"):
                if emptylist == True:
                    emptylist = False

                else:
                    list_of_games.append(game)
                    game = list()

            game.append(line)

        list_of_games.append(game)
        return list_of_games

    def get_players(self, game):
        # skip table info lines
        game = game[2:]

        # get seats & players
        players, game = self.__parse_players_and_seats(game)

        return players

    def __parse_players_and_seats(self, lines):
        """ get seats & players """
        players = {}

        while lines[0].startswith('Seat'):
            # parse num & player
            cur_line = lines[0]
            seat_num    = cur_line[ cur_line.find(' ')+1 : cur_line.find(':') ]
            player_name = cur_line[ cur_line.find(':')+2 : cur_line.find('(')-1 ]

            newPlayer = player.Player(player_name, seat_num, hands_played=1, preflop_calls=0, 
                                        preflop_bets_and_raises=0, postflop_bets_and_raises=0,
                                        postflop_calls_checks_and_folds=0)
            players[player_name] = newPlayer

            lines = lines[1:]

        return players, lines

    def __parse_preflop(self, game, players):
        player_actions = {}

        while game[0].startswith(tuple([ x for x in players.keys() ])):
            cur_line = game[0]

            # ignore disconnection messages
            if 'disconnected' in cur_line:
                game = game[1:]
                continue

            this_player = cur_line[: cur_line.find(':')]
            cur_line = cur_line[cur_line.find(':')+2 : ]

            words = cur_line.split(' ')
            action = words[0]

            # find dominant action for each player
            if not this_player in player_actions:
                player_actions[this_player] = action

            else:
                if action == "calls":
                    if player_actions[this_player] == "raises":
                        pass

                    else:
                        player_actions[this_player] = "calls"

                elif action == "raises":
                    player_actions[this_player] = "raises"

                elif action == "checks":
                    player_actions[this_player] = "checks"

                elif action == "folds":
                    pass

                else:
                    print(f"unexpected action: {words[0]}")

            game = game[1:]

        # update players dictionary with dominant action
        for aplayer, paction in player_actions.items():
            if paction == "raises":
                players[aplayer].preflop_bets_and_raises += 1

            elif paction == "calls":
                players[aplayer].preflop_calls += 1

            elif paction == "checks":
                pass

            elif paction == "folds":
                pass

            else:
                print(f"unexpected action: {action}, paction: {paction}, preflop, cur_line: {cur_line}, words: {words}, pactions: {player_actions}")

        return game

    def __parse_postflop(self, game, players):
        player_actions = {}

        while game[0].startswith(tuple([ x for x in players.keys() ])):
            cur_line = game[0]

            # ignore disconnection messages
            if 'disconnected' in cur_line:
                game = game[1:]
                continue

            this_player = cur_line[: cur_line.find(':')]
            cur_line = cur_line[cur_line.find(':')+2 : ]

            # parse action for player
            words = cur_line.split(' ')
            action = words[0]

            # find dominant action for each player
            if not this_player in player_actions:
                player_actions[this_player] = action

            else:
                if action == "calls":
                    if player_actions[this_player] == "bets" or player_actions[this_player] == "raises":
                        pass

                    else:
                        player_actions[this_player] = "calls"

                elif action == "checks":
                    player_actions[this_player] = "checks"

                elif action == "raises":
                    player_actions[this_player] = "raises"
                
                elif action == "bets":
                    player_actions[this_player] = "bets"

                elif action == "folds":
                    pass

                else:
                    print(f"unexpected action: {words[0]}")

            game = game[1:]

        # update players dictionary with dominant action
        for aplayer, paction in player_actions.items():
            if paction == "raises":
                players[aplayer].postflop_bets_and_raises += 1

            elif paction == "bets":
                players[aplayer].postflop_bets_and_raises += 1

            elif paction == "calls":
                players[aplayer].postflop_calls_checks_and_folds += 1

            elif paction == "folds":
                players[aplayer].postflop_calls_checks_and_folds += 1

            elif paction == "checks":
                players[aplayer].postflop_calls_checks_and_folds += 1

            else:
                print(f"unexpected action: {action}, paction: {paction}, postflop, cur_line: {cur_line}, words: {words}")

        return game

    def parse_game(self, game):
        """ parses a game of poker and builds a dict of Player """
        # players = {}

        # skip table info lines
        game = game[2:]

        # get seats & players
        players, game = self.__parse_players_and_seats(game)
        
        # skip sb/bb info
        game = game[2:]

        # skip hole cards info
        game = game[2:]

        # parse preflop
        game = self.__parse_preflop(game, players)

        # parse postflop
        if game[0].startswith("*** FLOP ***"):
            game = game[1:]
            game = self.__parse_postflop(game, players)

        # parse turn
        if game[0].startswith("*** TURN ***"):
            game = game[1:]
            game = self.__parse_postflop(game, players)

        # parse river
        if game[0].startswith("*** RIVER ***"):
            game = game[1:]
            game = self.__parse_postflop(game, players)

        return players
    

if __name__ == "__main__":

    import glob
    import os

    HAND_HISTORY_DIR_PATH = "/Users/charlesfiguero/Library/Application Support/PokerStarsUK/HandHistory/ToiletBaby"
    list_of_files = glob.glob(HAND_HISTORY_DIR_PATH + '/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)


    test_game = [
    "PokerStars Zoom Hand #225001835715:  Hold'em No Limit ($0.01/$0.02) - 2021/03/20 15:18:49 WET [2021/03/20 11:18:49 ET]",
    "Table 'Halley' 6-max Seat #1 is the button",
    "Seat 1: ziggyphillis ($2.40 in chips) ",
    "Seat 2: ToiletBaby ($2.95 in chips) ",
    "Seat 3: $ zalesovich ($2.11 in chips) ",
    "Seat 4: zoot62 ($2.03 in chips) ",
    "Seat 5: Orboeb ($2.12 in chips) ",
    "Seat 6: hymon96 ($4.19 in chips) ",
    "ToiletBaby: posts small blind $0.01",
    "$ zalesovich: posts big blind $0.02",
    "*** HOLE CARDS ***",
    "Dealt to ToiletBaby [6d 2c]",
    "zoot62: folds ",
    "Orboeb: folds ",
    "hymon96: raises $0.04 to $0.06",
    "ziggyphillis: calls $0.06",
    "ToiletBaby: folds ",
    "$ zalesovich: folds ",
    "*** FLOP *** [Td Ah As]",
    "hymon96: checks ",
    "ziggyphillis: bets $0.05",
    "hymon96: calls $0.05",
    "*** TURN *** [Td Ah As] [Qc]",
    "hymon96: checks ",
    "ziggyphillis: checks ",
    "*** RIVER *** [Td Ah As Qc] [8c]",
    "hymon96: bets $0.20",
    "ziggyphillis: calls $0.20",
    "*** SHOW DOWN ***",
    "hymon96: shows [Js Jh] (two pair, Aces and Jacks)",
    "ziggyphillis: shows [Qd 8d] (two pair, Aces and Queens)",
    "ziggyphillis collected $0.63 from pot",
    "*** SUMMARY ***",
    "Total pot $0.65 | Rake $0.02 ",
    "Board [Td Ah As Qc 8c]",
    "Seat 1: ziggyphillis (button) showed [Qd 8d] and won ($0.63) with two pair, Aces and Queens",
    "Seat 2: ToiletBaby (small blind) folded before Flop",
    "Seat 3: $ zalesovich (big blind) folded before Flop",
    "Seat 4: zoot62 folded before Flop (didn't bet)",
    "Seat 5: Orboeb folded before Flop (didn't bet)",
    "Seat 6: hymon96 showed [Js Jh] and lost with two pair, Aces and Jacks"
    ]

    parser = Parser()

    # parser.parse_game(test_game)
    hhfile = "/Users/charlesfiguero/Library/Application Support/PokerStarsUK/HandHistory/ToiletBaby/HH20210320 Halley - $0.01-$0.02 - USD No Limit Hold'em.txt"

    lines = parser.get_lines(hhfile)

    games = parser.get_games(lines)

    # for count, game in enumerate(games):
        # for line in games:
        #     print(line)
        # print(count)
        # players = parser.parse_game(game)
    # print(players)

    # for line in games[1]:
    #     print(line)

    # players = parser.parse_game(games[1])



