# enum for the different game modes
from enum import Enum

class Game(Enum):
    BLACKJACK = 0
    POKER = 1
    ROULETTE = 2
    YAZY = 3
    
class GameMode(Enum):
    CASH_GAME = 0
    TOURNAMENT = 1
    RANKED = 2
    SPIN_AND_PLAY = 3
    GAMBLING_BATTLES = 4
