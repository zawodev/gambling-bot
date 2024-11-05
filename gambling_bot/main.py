import discord

from gambling_bot.admin.operation_type import OperationType
from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.main_view import MainView
from gambling_bot.casino import casino
from gambling_bot.admin import database_update
from gambling_bot.admin.default_dict_data import create_default_player_profiles_in_guild


# both commands: bet
# blackjack commands: hit, stand, double, split, forfeit
# poker commands: check, call, raise, fold, all_in

async def setup(bot):
    # casino setup
    casino.setup(bot)

    # ------- ON INTERACTION -------

    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        create_default_player_profiles_in_guild(interaction.guild)

    # ------- PLAYER COMMANDS -------

    @bot.tree.command(name="play", description="rozpocznij grę w kasynie")
    async def play(interaction: discord.Interaction):
        main_view = MainView(interaction) # noqa
        await main_view.send()

    @bot.tree.command(name="bet", description="postaw zakład")
    async def bet(interaction: discord.Interaction, table_type: TableType, table_name: str, bet_: int):
        await casino.bet(interaction, table_type, table_name, bet_)

    # ------- ADMIN COMMANDS -------
    # commands for adding, removing and modyfing data in database from given path
    @bot.tree.command(name="db", description="zarządzaj bazą danych")
    async def db(interaction: discord.Interaction, operation: OperationType, path: str = None, data: str = None):
        await database_update.db(interaction, operation, path, data)
