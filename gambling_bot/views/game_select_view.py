import discord
from gambling_bot.views.view import View
from gambling_bot.views.table_select_view import TableSelectView
from gambling_bot.casino import casino

class GameSelectView(View):
    def __init__(self):
        super().__init__()

    def create_buttons(self):
        # blackjack button
        blackjack_button = discord.ui.Button(
            label="blackjack",
            style=discord.ButtonStyle.green,
            custom_id="blackjack"
        )

        # poker button
        poker_button = discord.ui.Button(
            label="poker",
            style=discord.ButtonStyle.green,
            custom_id="poker"
        )

        # roulette button
        roulette_button = discord.ui.Button(
            label="roulette",
            style=discord.ButtonStyle.green,
            custom_id="roulette"
        )

        # slots button
        slots_button = discord.ui.Button(
            label="slots",
            style=discord.ButtonStyle.green,
            custom_id="slots"
        )

        return [blackjack_button, poker_button, roulette_button, slots_button]

    def create_embeds(self):
        embed = discord.Embed(
            title="Game Select",
            description="Choose a game",
            color=discord.Color.pink()
        )
        return [embed]

    # --------- callbacks ---------

    async def blackjack(self, interaction: discord.Interaction, button: discord.ui.Button):
        tables = casino.blackjack_tables
        view = TableSelectView(tables)
        await view.display(interaction.message)

    async def poker(self, interaction: discord.Interaction, button: discord.ui.Button):
        raise NotImplementedError

    async def roulette(self, interaction: discord.Interaction, button: discord.ui.Button):
        raise NotImplementedError

    async def slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        raise NotImplementedError
