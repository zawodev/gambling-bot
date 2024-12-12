import discord

from gambling_bot.views.menu_view import MenuView
from gambling_bot.views.view import View
from gambling_bot.models.casino import casino

class StatsView(View):
    def __init__(self, interaction, message):
        super().__init__(interaction, message)
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
            description=f"{self.profile.profile_data.__str__()}",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    async def back(self, interaction: discord.Interaction):
        view = MenuView(self.interaction, self.message)
        await view.edit(interaction)
