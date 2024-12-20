import discord

from gambling_bot.admin.not_implemented_error import not_implemented_error
from gambling_bot.views.view import View
from gambling_bot.data.json_manager import load_data

class MenuView(View):
    def __init__(self, interaction, message):
        super().__init__(interaction, message)

    def create_buttons(self):
        # play again button
        play_button = discord.ui.Button(
            label="play",
            style=discord.ButtonStyle.green,
            custom_id="play"
        )
        play_button.callback = self.play

        # claim button
        claim_button = discord.ui.Button(
            label="claim",
            style=discord.ButtonStyle.gray,
            custom_id="claim"
        )
        claim_button.callback = self.claim

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

        return [play_button, claim_button, stats_button, ranking_button]

    def create_embeds(self):
        embed = discord.Embed(
            title="Casino Bot",
            description=f"wersja: {load_data("app/info/version")}",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    async def play(self, interaction: discord.Interaction):
        from gambling_bot.views.game_select_view import GameSelectView
        view = GameSelectView(self.interaction, self.message)
        await view.edit(interaction)

    async def claim(self, interaction: discord.Interaction):
        from gambling_bot.views.claim_reward_view import ClaimRewardView
        view = ClaimRewardView(self.interaction, self.message)
        await view.edit(interaction)

    async def stats(self, interaction: discord.Interaction):
        from gambling_bot.views.stats_view import StatsView
        view = StatsView(self.interaction, self.message)
        await view.edit(interaction)

    async def ranking(self, interaction: discord.Interaction):
        await not_implemented_error(interaction)
        return
        
        from gambling_bot.views.ranking_view import RankingView
        view = RankingView(self.interaction, self.message)
        await view.edit(interaction)
