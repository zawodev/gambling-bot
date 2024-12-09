
from gambling_bot.models.table.table import Table


class RouletteTable(Table):
    def __init__(self, dealer, data, path):
        super().__init__(dealer, data, path)
