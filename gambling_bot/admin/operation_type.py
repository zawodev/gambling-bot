from enum import Enum

class OperationType(Enum):
    SAVE = "save"
    LOAD = "load"

    def __str__(self):
        return self.name.lower()
