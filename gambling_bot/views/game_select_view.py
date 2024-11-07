import discord

from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.view import View
from gambling_bot.views.table_select_view import TableSelectView
from gambling_bot.casino import casino

class GameSelectView(View):
    def __init__(self, interaction, back_view):
        super().__init__(interaction)
        self.back_view = back_view

    def create_buttons(self):
        # blackjack button
        blackjack_button = discord.ui.Button(
            label="blackjack",
            style=discord.ButtonStyle.green,
            custom_id="blackjack"
        )
        blackjack_button.callback = self.blackjack

        # poker button
        poker_button = discord.ui.Button(
            label="poker",
            style=discord.ButtonStyle.green,
            custom_id="poker"
        )
        poker_button.callback = self.poker

        # roulette button
        roulette_button = discord.ui.Button(
            label="roulette",
            style=discord.ButtonStyle.green,
            custom_id="roulette"
        )
        roulette_button.callback = self.roulette

        # slots button
        slots_button = discord.ui.Button(
            label="slots",
            style=discord.ButtonStyle.green,
            custom_id="slots"
        )
        slots_button.callback = self.slots

        # back button
        back_button = discord.ui.Button(
            label="back",
            style=discord.ButtonStyle.red,
            custom_id="back"
        )
        back_button.callback = self.back

        return [blackjack_button, poker_button, roulette_button, slots_button, back_button]

    def create_embeds(self):
        embed = discord.Embed(
            title="Game Select",
            description="Choose a game",
            color=discord.Color.pink()
        )
        return [embed]

    # --------- callbacks ---------

    async def blackjack(self, interaction: discord.Interaction):
        tables = casino.blackjack_tables
        view = TableSelectView(self.interaction, tables, TableType.BLACKJACK, self)
        await view.edit(interaction)

    async def poker(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def roulette(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def slots(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def back(self, interaction: discord.Interaction):
        await self.back_view.edit(interaction)
