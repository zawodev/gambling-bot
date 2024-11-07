import discord
from gambling_bot.views.view import View
from gambling_bot.views.bet_select_view import BetSelectView

class TableSelectView(View):
    def __init__(self, interaction, tables, table_type, back_view):
        self.tables = tables
        self.table_type = table_type
        self.back_view = back_view
        super().__init__(interaction)

    def create_buttons(self):
        buttons = []
        for table in self.tables:
            button = discord.ui.Button(
                label=table.table_data['name'],
                style=discord.ButtonStyle.gray,
                custom_id=str(table.table_data.path)
            )
            button.callback = self.select_table(table, self.table_type)
            buttons.append(button)

        back_button = discord.ui.Button(
            label="back",
            style=discord.ButtonStyle.red,
            custom_id="back"
        )
        back_button.callback = self.back
        buttons.append(back_button)

        return buttons

    def create_embeds(self):
        embed = discord.Embed(
            title="Table Select",
            description="Choose a table",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    def select_table(self, table, table_type):
        async def button_callback(interaction: discord.Interaction):
            view = BetSelectView(self.interaction, table, table_type, self)
            await view.edit(interaction)
        return button_callback

    async def back(self, interaction: discord.Interaction):
        await self.back_view.edit(interaction)
