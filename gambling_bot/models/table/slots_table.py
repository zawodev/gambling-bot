
from gambling_bot.models.table.table import Table
from gambling_bot.models.player import Player

class SlotsTable(Table):
    def __init__(self, dealer, data, path):
        super().__init__(dealer, data, path)
