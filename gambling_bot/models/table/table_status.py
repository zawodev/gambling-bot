from enum import Enum

class TableStatus(Enum):
    WAITING_FOR_PLAYERS = "waiting_for_players"
    WAITING_FOR_START = "waiting_for_start"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    DISABLED = "disabled"
    UNKNOWN = "unknown"
