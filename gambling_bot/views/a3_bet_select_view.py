import discord
from gambling_bot.models.table.table import Table
from gambling_bot.views import a4_table_view
from discord.ui import Button
from gambling_bot.casino import casino


async def display(interaction: discord.Interaction, table: Table):
    player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
    name = player_profile.profile_data['name']
    description = f"{player_profile.profile_data['chips']}$"
    color = int(player_profile.profile_data['color'])
    embed = discord.Embed(title=name, description=description, color=color)
    view = BetSelectView(table)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


def _create_button_callback(table: Table, bet: int):
    async def button_callback(interaction: discord.Interaction):
        player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
        table.add_bet_player(player_profile, bet)
        await a4_table_view.display(interaction, table)
    return button_callback

class BetSelectView(discord.ui.View):
    def __init__(self, table: Table):
        super().__init__()
        self.table = table
        for bet in table.table_data['bets']:
            bet_name = f"bet {bet}"
            bet_unq_id = f"{table.table_data.path[-1]}_{table.table_data.path[-2]}_{bet}"
            button = Button(
                label=bet_name,
                style=discord.ButtonStyle.blurple, custom_id=bet_unq_id
            )
            button.callback = _create_button_callback(table, int(bet))
            button.style = discord.ButtonStyle.gray
            self.add_item(button)

    @discord.ui.button(label="ready", style=discord.ButtonStyle.green, custom_id="ready")
    async def ready(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.table.ready(interaction.user.id)
        await a4_table_view.display(interaction, self.table)
