import discord

from gambling_bot.views.menu_view import MenuView
from gambling_bot.views.view import View
from gambling_bot.models.casino import casino

class RankingView(View):
    def __init__(self, interaction, message):
        super().__init__(interaction, message)

    def create_buttons(self):
        # back button
        back_button = discord.ui.Button(
            label="back",
            style=discord.ButtonStyle.red,
            custom_id="back"
        )
        back_button.callback = self.back

        return [back_button]

    def create_embeds(self):
        # weekly ranking, monthly ranking, all time ranking
        # weekly ranking - to be implemented
        # monthly ranking - to be implemented
        # all time ranking
        profiles = casino.player_profiles
        profiles.sort(key=lambda profile: profile.get_elo_points(), reverse=True)
        embed = discord.Embed(
            title=f"Ranking",
            description=f"{'\n'.join([
                f"{profile.profile_data['name']}: {profile.get_elo_points()} elo ({profile.get_elo_title()})" 
                for profile in profiles])}",
            color=discord.Color.blurple()
        )
        return [embed]

    # --------- callbacks ---------

    async def back(self, interaction: discord.Interaction):
        view = MenuView(self.interaction, self.message)
        await view.edit(interaction)
