from enum import Enum

class OperationType(Enum):
    SAVE = "save"
    LOAD = "load"
    REMOVE = "remove"
    MOVE = "move"

    def __str__(self):
        return self.name.lower()
