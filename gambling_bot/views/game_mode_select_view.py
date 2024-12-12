import discord

from gambling_bot.admin.not_implemented_error import not_implemented_error
from gambling_bot.views.main_menu_view import MainMenuView
from gambling_bot.views.view import View

class GameModeSelectView(View):
    def __init__(self, interaction, message):
        super().__init__(interaction, message)

    def create_buttons(self):
        # cash game button
        cash_game_button = discord.ui.Button(
            label="cash game",
            style=discord.ButtonStyle.green,
            custom_id="cash_game"
        )
        cash_game_button.callback = self.cash_game
        
        # tournament button
        tournament_button = discord.ui.Button(
            label="tournament",
            style=discord.ButtonStyle.gray,
            custom_id="tournament"
        )
        tournament_button.callback = self.tournament
        
        # back button
        back_button = discord.ui.Button(
            label="back",
            style=discord.ButtonStyle.red,
            custom_id="back"
        )
        back_button.callback = self.back
        
        return [cash_game_button, tournament_button, back_button]

    def create_embeds(self):
        embed = discord.Embed(
            title="Game Mode Select",
            description="Choose a game mode",
            color=discord.Color.purple()
        )
        return [embed]

    # --------- callbacks ---------

    async def cash_game(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def tournament(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)

    async def back(self, interaction: discord.Interaction):
        view = MainMenuView(self.interaction, self.message)
        await view.edit(interaction)
