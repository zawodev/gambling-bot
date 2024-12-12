import discord

from gambling_bot.admin.not_implemented_error import not_implemented_error
from gambling_bot.core.hand_values import HandValue
from gambling_bot.models.table.poker_table import PokerTable
from gambling_bot.views.view import View

class PokerTableView(View):
    def __init__(self, interaction, message, table: PokerTable):
        self.table = table
        super().__init__(interaction, message)

    def create_buttons(self):
        # deal button
        deal_button = discord.ui.Button(
            label="deal",
            style=discord.ButtonStyle.gray,
            custom_id="deal"
        )
        deal_button.callback = self.deal

        # check button
        check_button = discord.ui.Button(
            label="check",
            style=discord.ButtonStyle.gray,
            custom_id="check"
        )
        check_button.callback = self.check

        # call button
        call_button = discord.ui.Button(
            label="call",
            style=discord.ButtonStyle.gray,
            custom_id="call"
        )
        call_button.callback = self.call

        # raise button
        raise_button = discord.ui.Button(
            label="raise",
            style=discord.ButtonStyle.gray,
            custom_id="raise"
        )
        raise_button.callback = self.raise_

        # fold button
        fold_button = discord.ui.Button(
            label="fold",
            style=discord.ButtonStyle.gray,
            custom_id="fold"
        )
        fold_button.callback = self.fold

        # all in button
        all_in_button = discord.ui.Button(
            label="all in",
            style=discord.ButtonStyle.gray,
            custom_id="all_in"
        )
        all_in_button.callback = self.all_in

        return [deal_button, check_button, call_button, raise_button, fold_button, all_in_button]


    def create_embeds(self):
        embeds = []

        embed = discord.Embed(
            title="Poker Table",
            description="Choose an action",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Community Cards",
            value=" ".join([card.emoji for card in self.table.community_cards]),
            inline=False
        )

        for player in self.table.players:
            embed.add_field(
                name=player.name,
                value=f"Chips: {player.chips}\nHand: {' '.join([card.emoji for card in player.hand])}\nHand Value: {HandValue(player.hand).value}",
                inline=False
            )

        embeds.append(embed)

        return embed

    # --------- callbacks ---------

    async def deal(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def check(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def call(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def raise_(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def fold(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def all_in(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)
