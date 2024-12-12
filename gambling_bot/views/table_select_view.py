import discord

from gambling_bot.admin.not_implemented_error import game_in_progress_error
from gambling_bot.models.table.table_status import TableStatus
from gambling_bot.views.view import View
from gambling_bot.views.bet_select_view import BetSelectView

class TableSelectView(View):
    def __init__(self, interaction, message, tables):
        self.tables = tables
        super().__init__(interaction, message)

    def create_buttons(self):
        buttons = []
        for table in self.tables:
            #button green if table game not started, grey if started
            button = discord.ui.Button(
                label=table.table_data['name'],
                style=discord.ButtonStyle.green
                if table.table_status == TableStatus.WAITING_FOR_PLAYERS else
                discord.ButtonStyle.grey,
                custom_id=str(table.table_data.path)
            )
            button.callback = self.select_table(table)
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
        # print every table in new line as description
        embed = discord.Embed(
            title="Table Select",
            description="\n".join([table.__str__() for table in self.tables]),
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    def select_table(self, table):
        async def button_callback(interaction: discord.Interaction):
            if table.table_status == TableStatus.IN_PROGRESS:
                await game_in_progress_error(interaction)
            else:
                view = BetSelectView(interaction, self.message, table)
                await view.edit(interaction)
        return button_callback

    async def back(self, interaction: discord.Interaction):
        from gambling_bot.views.game_select_view import GameSelectView
        view = GameSelectView(self.interaction, self.message)
        await view.edit(interaction)
