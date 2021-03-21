class Player():

    def __init__(self, name, seat, hands_played, preflop_calls, preflop_bets_and_raises, 
                    postflop_bets_and_raises, postflop_calls_checks_and_folds):

        self.name = name
        self.seat = seat
        self.hands_played = hands_played
        self.preflop_calls = preflop_calls
        self.preflop_bets_and_raises = preflop_bets_and_raises
        self.postflop_bets_and_raises = postflop_bets_and_raises
        self.postflop_calls_checks_and_folds = postflop_calls_checks_and_folds

    def __repr__(self):
        return (f"< name:{self.name}, "
                f"seat:{self.seat}, "
                f"hands_played:{self.hands_played}, "
                f"preflop_calls:{self.preflop_calls}, "
                f"preflop_bets_and_raises:{self.preflop_bets_and_raises}, "
                f"postflop_bets_and_raises:{self.postflop_bets_and_raises}, "
                f"postflop_calls_checks_and_folds:{self.postflop_calls_checks_and_folds} > \n")

    def __add__(self, o):
        if not self.name == o.name:
            raise ValueError()

        else:
            newPlayer = Player(self.name, 
            self.seat, 
            self.hands_played + o.hands_played,
            self.preflop_calls + o.preflop_calls,
            self.preflop_bets_and_raises + o.preflop_bets_and_raises,
            self.postflop_bets_and_raises + o.postflop_bets_and_raises,
            self.postflop_calls_checks_and_folds + o.postflop_calls_checks_and_folds)

            return newPlayer

    def print_stats(self):
        print()
        VPIP = self.calculate_VPIP()
        PFR = self.calculate_PFR()
        AFq = self.calculate_AFq()

        if self.is_shark(VPIP, PFR) == "shark":
            print("🦈 ")
        else:
            print("🐟 ")

        print(f"Player: {self.name}")
        print(f"Hands analysed: {self.hands_played}")
        print(f"VPIP: {VPIP}")
        print(f"PFR: {PFR}")
        print(f"AFq: {AFq}")

    def is_shark(self, VPIP, PFR):
        if VPIP < 30 and VPIP > 15 and VPIP - PFR < 5:
            return "shark"
        else:
            return "fish"

    def calculate_VPIP(self):
        if self.hands_played == 0:
            return 0

        else:
            VPIP = (self.preflop_calls + self.preflop_bets_and_raises) * 100 / self.hands_played
            return VPIP

    def calculate_PFR(self):
        if self.hands_played == 0:
            return 0

        else:
            PFR = (self.preflop_bets_and_raises / self.hands_played) * 100
            return PFR
    
    def calculate_AFq(self):
        if self.postflop_bets_and_raises + self.postflop_calls_checks_and_folds == 0:
            return 0

        else:
            AFq = (self.postflop_bets_and_raises / (self.postflop_bets_and_raises + self.postflop_calls_checks_and_folds)) * 100
            return AFq

if __name__ == "__main__":

    testFish = Player("fish", 2, 100, 45, 15, 10, 50)
    print(testFish)
    print(f"VPIP: {testFish.calculate_VPIP()}")
    print(f"PFR: {testFish.calculate_PFR()}")
    print(f"AF: {testFish.calculate_AFq()}")
    print()

    testShark = Player("shark", 1, 100, 2, 18, 10, 10)
    print(testShark)
    print(f"VPIP: {testShark.calculate_VPIP()}")
    print(f"PFR: {testShark.calculate_PFR()}")
    print(f"AF: {testShark.calculate_AFq()}")
