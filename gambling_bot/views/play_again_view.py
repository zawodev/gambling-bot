import discord

from gambling_bot.core.hand_values import HandValue
from gambling_bot.models.player.player import Player

from gambling_bot.views.menu_view import MenuView
from gambling_bot.views.view import View

class PlayAgainView(View):
    def __init__(self, interaction, message, table):
        self.table = table
        super().__init__(interaction, message)

    def create_buttons(self):
        # play again button
        play_again_button = discord.ui.Button(
            label="play again",
            style=discord.ButtonStyle.green,
            custom_id="play_again"
        )
        play_again_button.callback = self.play_again

        # quit button
        quit_button = discord.ui.Button(
            label="quit",
            style=discord.ButtonStyle.red,
            custom_id="quit"
        )
        quit_button.callback = self.quit

        return [play_again_button, quit_button]

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

    async def play_again(self, interaction: discord.Interaction):
        #view = BetSelectView(self.interaction, self.message)
        #await view.edit(interaction)
        from gambling_bot.views.bet_select_view import BetSelectView
        view = BetSelectView(interaction, self.message, self.table)
        await view.send(ephemeral=True)

    async def quit(self, interaction: discord.Interaction):
        view = MenuView(interaction, self.message)
        await view.send(ephemeral=True)

