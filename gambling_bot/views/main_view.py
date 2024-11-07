import discord

from gambling_bot.views.stats_view import StatsView
from gambling_bot.views.view import View
from gambling_bot.views.game_select_view import GameSelectView

class MainView(View):
    def __init__(self, interaction):
        super().__init__(interaction)

    def create_buttons(self):
        # play again button
        play_button = discord.ui.Button(
            label="play",
            style=discord.ButtonStyle.green,
            custom_id="play"
        )
        play_button.callback = self.play

        # stats button
        stats_button = discord.ui.Button(
            label="stats",
            style=discord.ButtonStyle.blurple,
            custom_id="stats"
        )
        stats_button.callback = self.stats

        # ranking button
        ranking_button = discord.ui.Button(
            label="ranking",
            style=discord.ButtonStyle.red,
            custom_id="ranking"
        )
        ranking_button.callback = self.ranking

        return [play_button, stats_button, ranking_button]

    def create_embeds(self):
        embed = discord.Embed(
            title="Casino Bot",
            description=f"wersja: 0.53 alpha - experimental",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    async def play(self, interaction: discord.Interaction):
        view = GameSelectView(self.interaction, self)
        await view.edit(interaction)

    async def stats(self, interaction: discord.Interaction):
        view = StatsView(self.interaction, self)
        await view.edit(interaction)

    async def ranking(self, interaction: discord.Interaction):
        raise NotImplementedError
        #interaction.response.defer()
