import discord
from gambling_bot.views.view import View
from gambling_bot.casino import casino

class StatsView(View):
    def __init__(self, interaction, back_view):
        super().__init__(interaction)
        self.back_view = back_view
        self.profile = casino.get_player_profile_with_id(str(interaction.user.id))

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
        embed = discord.Embed(
            title=f"{self.profile.profile_data['name']} stats",
            description=f"chips: {self.profile.profile_data['chips']}$\n"
                        f"freechips: {self.profile.profile_data['freechips']}$",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    async def back(self, interaction: discord.Interaction):
        await self.back_view.edit(interaction)
