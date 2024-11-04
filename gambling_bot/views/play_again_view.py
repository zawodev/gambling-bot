import discord
from gambling_bot.views.view import View

class PlayAgainView(View):
    def __init__(self, table):
        super().__init__()
        self.table = table

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
        embed = discord.Embed(
            title=self.table.table_data['name'],
            description=f"maybe some player data here?\n"
                        f"minbet - maxbet: [{self.table.table_data['min_bet']}$ - {self.table.table_data['max_bet']}]$",
            color=discord.Color.purple()
        )
        return [embed]

    # --------- callbacks ---------

    async def play_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.play_again(interaction.user.id)
        await self.table.display(interaction)

    async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.quit(interaction.user.id)
        await self.table.display(interaction)
