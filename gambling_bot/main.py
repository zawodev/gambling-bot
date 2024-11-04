import discord

from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.main_view import MainView
from gambling_bot.casino import casino
from gambling_bot.admin_configuration import table_configuration
from gambling_bot.admin_configuration.profile_manager import (create_player_profile, create_dealer_profile,
                                                              remove_dealer_profile, create_default_dealers,
                                                              create_player_profiles_in_guild)


# both commands: bet
# blackjack commands: hit, stand, double, split, forfeit
# poker commands: check, call, raise, fold, all_in

async def setup(bot):
    # casino setup
    create_default_dealers()
    casino.setup(bot)

    @bot.tree.command(name="play", description="rozpocznij grę w kasynie")
    async def play(interaction: discord.Interaction):
        main_view = MainView(interaction) # noqa
        await main_view.send()

    # ------- ON INTERACTION -------

    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        create_player_profiles_in_guild(interaction.guild)

    # ------- ADMIN COMMANDS -------

    # add table command
    @bot.tree.command(name="add_table", description="dodaj stół do kasyna")
    async def add_table(interaction: discord.Interaction, table_type: TableType, table_name: str,
                        bets: str = "10 100 500"):
        bets_list = bets.split(" ")
        await table_configuration.add_table(interaction, table_type, table_name, bets_list)

    # remove table command
    @bot.tree.command(name="remove_table", description="usuń stół z kasyna")
    async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
        await table_configuration.remove_table(interaction, table_type, table_name)

    # add dealer command
    @bot.tree.command(name="add_dealer", description="dodaj dealera do kasyna")
    async def add_dealer(interaction: discord.Interaction, dealer_name: str):
        create_dealer_profile(dealer_name)

    # remove dealer command
    @bot.tree.command(name="remove_dealer", description="usuń dealera z kasyna")
    async def remove_dealer(interaction: discord.Interaction, dealer_name: str):
        remove_dealer_profile(dealer_name)
