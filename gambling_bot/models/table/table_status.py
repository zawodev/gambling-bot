from enum import Enum

class TableStatus(Enum):
    DISABLED = 0
    WAITING_FOR_PLAYERS = 1
    IN_PROGRESS = 2
    FINISHED = 3
