from enum import Enum

class OperationType(Enum):
    ADD = 1
    REMOVE = 2
    MODIFY = 3

    def __str__(self):
        return self.name.lower()
