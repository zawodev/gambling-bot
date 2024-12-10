import discord

from gambling_bot.admin.operation_type import OperationType
from gambling_bot.data.json_manager import load_data
from gambling_bot.views.main_view import MainView
from gambling_bot.models.casino import casino
from gambling_bot.admin import database_update
from gambling_bot.admin.default_dict_data import create_default_player_profiles_in_guild


# both commands: bet
# blackjack commands: hit, stand, double, split, forfeit
# poker commands: check, call, raise, fold, all_in
bot_ref = None

async def setup(bot):
    # casino setup
    global bot_ref
    bot_ref = bot

    casino.load_data()
    await bot.change_presence(activity=discord.Game(name=f"in casino /play /watch v{load_data("app/info/version")}"))

    # ------- ON INTERACTION -------

    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        create_default_player_profiles_in_guild(casino, interaction.guild)

    # ------- PLAYER COMMANDS -------

    @bot.tree.command(name="play", description="rozpocznij grę w kasynie")
    async def play(interaction: discord.Interaction):
        main_view = MainView(interaction) # noqa
        await main_view.send()

    @bot.tree.command(name="watch", description="oglądaj grę w kasynie")
    async def watch(interaction: discord.Interaction):
        pass

    # ------- ADMIN COMMANDS -------
    # commands for adding, removing and modifying data in database from given path
    @bot.tree.command(name="db", description="zarządzaj bazą danych")
    async def db(interaction: discord.Interaction, operation: OperationType, path: str = "", data: str = ""):
        if interaction.user.id in (336921078138011650, 380820820466991116):
            await database_update.db(interaction, operation, path, data)
        else:
            await interaction.response.send_message("nie masz uprawnień do użycia tej komendy", ephemeral=True)
