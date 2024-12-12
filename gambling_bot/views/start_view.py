import discord

from gambling_bot.views.menu_view import MenuView
from gambling_bot.views.view import View
from gambling_bot.data.json_manager import load_data

class StartView(View):
    def __init__(self, interaction, message):
        super().__init__(interaction, message)

    def create_buttons(self):
        # start button
        start_button = discord.ui.Button(
            label="start",
            style=discord.ButtonStyle.green,
            custom_id="start"
        )
        start_button.callback = self.start

        return [start_button]

    def create_embeds(self):
        embed = discord.Embed(
            title="Main view (default on spawn)",
            description=f"wersja: {load_data("app/info/version")}",
            color=discord.Color.orange()
        )
        return [embed]

    # --------- callbacks ---------

    async def start(self, interaction: discord.Interaction):
        view = MenuView(interaction, self.message)
        await view.send(ephemeral=True)
        