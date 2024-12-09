import discord

from gambling_bot.core.hand_values import HandValue
from gambling_bot.models.player import Player
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.play_again_view import PlayAgainView
from gambling_bot.views.view import View

class BlackjackTableView(View):
    def __init__(self, interaction, table: BlackJackTable, bet_select_view):
        self.table = table
        self.bet_select_view = bet_select_view
        super().__init__(interaction)

    def create_buttons(self):

        # draw button
        deal_button = discord.ui.Button(
            label="deal",
            style=discord.ButtonStyle.gray,
            custom_id="deal"
        )
        deal_button.callback = self.deal

        # hit button
        hit_button = discord.ui.Button(
            label="hit",
            style=discord.ButtonStyle.gray,
            custom_id="hit"
        )
        hit_button.callback = self.hit

        # stand button
        stand_button = discord.ui.Button(
            label="stand",
            style=discord.ButtonStyle.gray,
            custom_id="stand"
        )
        stand_button.callback = self.stand

        # double button
        double_button = discord.ui.Button(
            label="double",
            style=discord.ButtonStyle.gray,
            custom_id="double"
        )
        double_button.callback = self.double

        # split button
        split_button = discord.ui.Button(
            label="split",
            style=discord.ButtonStyle.gray,
            custom_id="split"
        )
        split_button.callback = self.split

        # forfeit button
        forfeit_button = discord.ui.Button(
            label="forfeit",
            style=discord.ButtonStyle.gray,
            custom_id="forfeit"
        )
        forfeit_button.callback = self.forfeit

        return [deal_button, hit_button, stand_button, double_button, split_button, forfeit_button]

    def create_embeds(self):
        embeds = []

        # create embed for table type
        embed = discord.Embed(
            title=self.table.table_data['name'],
            description=self.table.table_data['description'],
            color=0xffaff0
        )
        embeds.append(embed)

        for player in self.table.players:
            player: Player
            player_color = int(player.profile.profile_data['color'])

            for hand in player.hands:
                hand_value = hand.value()
                embed = discord.Embed(
                    title=player,
                    description=hand,
                    color=player_color
                )
                embed.set_thumbnail(url=HandValue.from_int(hand_value))
                embeds.append(embed)

        dealer_hand = self.table.dealer.hand
        dealer_embed = discord.Embed(
            title=self.table.dealer,
            description=dealer_hand,
            color=0xFFFF00
        )
        dealer_embed.set_thumbnail(url=HandValue.from_int(dealer_hand.value()))
        embeds.append(dealer_embed)

        return embeds

    # --------- callbacks ---------

    async def deal(self, interaction: discord.Interaction):
        self.table.deal(interaction.user.id)
        await self._check_game_finished(interaction)

    async def hit(self, interaction: discord.Interaction):
        self.table.hit(interaction.user.id)
        await self._check_game_finished(interaction)

    async def stand(self, interaction: discord.Interaction):
        self.table.stand(interaction.user.id)
        await self._check_game_finished(interaction)

    async def double(self, interaction: discord.Interaction):
        self.table.double(interaction.user.id)
        await self._check_game_finished(interaction)

    async def split(self, interaction: discord.Interaction):
        self.table.split(interaction.user.id)
        await self._check_game_finished(interaction)

    async def forfeit(self, interaction: discord.Interaction):
        self.table.forfeit(interaction.user.id)
        await self._check_game_finished(interaction)

    # --------- helpers ---------

    async def _check_game_finished(self, interaction: discord.Interaction):
        if self.table.is_game_finished:
            view = PlayAgainView(self.interaction, self.table, self.bet_select_view)
            await view.edit(interaction)
        else:
            await self.edit(interaction)
