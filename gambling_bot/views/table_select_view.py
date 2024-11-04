import discord
from gambling_bot.views.view import View
from gambling_bot.views.bet_select_view import BetSelectView

class TableSelectView(View):
    def __init__(self, tables):
        super().__init__()
        self.tables = tables

    def create_buttons(self):
        buttons = []
        for table in self.tables:
            button = discord.ui.Button(
                label=table.table_data['name'],
                style=discord.ButtonStyle.gray,
                custom_id=str(table.table_data.path)
            )
            button.callback = self.select_table(table)
            buttons.append(button)
        return buttons

    def create_embeds(self):
        embed = discord.Embed(
            title="Table Select",
            description="Choose a table",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    def select_table(self, table):
        async def button_callback(interaction: discord.Interaction):
            view = BetSelectView(table)
            await view.display(interaction.message)
        return button_callback
