
from gambling_bot.models.table.table import Table


class SlotsTable(Table):
    def __init__(self, dealer, data, path):
        super().__init__(dealer, data, path)
