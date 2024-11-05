import discord
from gambling_bot.casino import casino
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.poker_table import PokerTable
from gambling_bot.models.table.table_type import TableType


# ---------------- PLAYER ----------------

def create_player_profile(user_id: str, user_name: str):
    if user_id not in casino.player_profiles:
        player_profile = Profile({'name': user_name}, 'profiles', 'players', user_id)
        casino.player_profiles.append(player_profile)

def get_player_profile_with_id(player_profile_id):
    for profile in casino.player_profiles:
        if profile.profile_data.path[-1] == player_profile_id:
            return profile
    return None

def create_default_player_profiles_in_guild(guild: discord.Guild):
    for member in guild.members:
        create_player_profile(str(member.id), member.display_name)

# ---------------- DEALER ----------------

def create_dealer_profile(name: str):
    if name not in casino.dealer_profiles:
        dealer_profile = Profile({'name': name}, 'profiles', 'dealers', name)
        casino.dealer_profiles.append(dealer_profile)

def create_default_dealers():
    names = ['Marek', 'Romper', 'Extreme', 'Gambler', 'WYGRAŁEM',
             'NIE', 'Fenomenalnie', 'Jogurt', 'Dealer', 'Krupier',
             'Wojtek', 'Pięcia', 'Nice Cnie', 'Jakub', 'Janek',
             'Obsrany', 'Jaja', 'Degenerat', 'Denaturat']
    for name in names:
        create_dealer_profile(f"Dealer {name}")

# ---------------- TABLE ----------------

def create_default_tables():
    pass


"""
    bets = ['10', '100', '500']
    blackjack_table = casino.add_table('blackjack', 'blackjack_table', bets)
    poker_table = casino.add_table('poker', 'poker_table', bets)

    blackjack_table.dealer = casino.get_random_dealer()
    poker_table.dealer = casino.get_random_dealer()
    blackjack_table.save()
    poker_table.save()
    

async def add_table(interaction: discord.Interaction, table_type: TableType, table_name: str, bets: list):
    # można się pozbyć tego ifa jeśli zrównasz klasy oraz dasz type jako argument zamiast ręcznie
    if table_type.value[0] == TableType.BLACKJACK.value[0]:
        blackjack_table = BlackJackTable(casino.get_random_dealer(), {'bets': bets}, 'tables', 'blackjack', table_name)
        casino.blackjack_tables.append(blackjack_table)
    elif table_type.value[0] == TableType.POKER.value[0]:
        poker_table = PokerTable(casino.get_random_dealer(), {'bets': bets}, 'tables', 'poker', table_name)
        casino.spin_and_play_tables.append(poker_table)
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message(f"added table {table_type}", ephemeral=True)


async def remove_table(interaction: discord.Interaction, table_type: str, table_name: str):
    if table_type == "blackjack":
        for table in casino.blackjack_tables:
            if table.table_data.path[-1] == table_name:
                table.table_data.delete()
                casino.blackjack_tables.remove(table)
                break
    elif table_type == "poker":
        for table in casino.poker_tables:
            if table.table_data.path[-1] == table_name:
                table.table_data.delete()
                casino.poker_tables.remove(table)
                break
    else:
        await interaction.response.send_message(f"table type not found", ephemeral=True)
        return
    await interaction.response.send_message("removed table", ephemeral=True)
"""
