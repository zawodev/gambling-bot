from enum import Enum

class TableType(Enum):
    BLACKJACK = ("blackjack", "epicki opis blackjacka")
    POKER = ("poker", "epicki opis pokera")
    ROULETTE = ("roulette", "epicki opis ruletki")
    SLOTS = ("slots", "epicki opis slotów")

    # gamemodes
    #SPIN_AND_PLAY = "spin_and_play"
    #TEXAS_HOLDEM = "texas_holdem"
    #WAR = "war"
    #WHEEL_OF_FORTUNE = "wheel_of_fortune"
    #YAHTZEE = "yahtzee"
    #ZILCH = "zilch"
