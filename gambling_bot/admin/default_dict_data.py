import discord

from gambling_bot.data.json_manager import load_data, save_data, save_data_raw
from gambling_bot.models.profile.profile import Profile


# ---------------- PLAYER ----------------

def get_player_profile_with_id(casino, player_profile_id):
    for profile in casino.player_profiles:
        if profile.profile_data.path[-1] == player_profile_id:
            return profile
    return None

def create_default_player_profiles_in_guild(casino, guild: discord.Guild):
    for member in guild.members:
        create_player_profile(casino, str(member.id), member.display_name)

def create_player_profile(casino, user_id: str, user_name: str):
    path = f'profiles/players/{user_id}'
    if path not in casino.player_profiles:
        player_profile = Profile({'name': user_name}, path)
        casino.player_profiles.append(player_profile)

# ---------------- DEALER ----------------

def create_default_dealers():
    dealer_data = load_data('profiles/dealers')
    names = ['Marek', 'Romper', 'Extreme', 'Gambler', 'WYGRAŁEM',
             'NIE', 'Fenomenalnie', 'Jogurt', 'Dealer', 'Krupier',
             'Wojtek', 'Pięcia', 'Nice Cnie', 'Jakub', 'Janek',
             'Obsrany', 'Jaja', 'Degenerat', 'Denaturat']
    for name in names:
        if name not in dealer_data:
            dealer_data[name] = {'name': name}
    save_data('profiles/dealers', dealer_data)

# ---------------- TABLE ----------------

def create_default_tables():
    blackjack_data = load_data('tables/blackjack')
    blackjack_default_data = [('BIG WIN', [100, 500]), ('SMALL WIN', [10, 50])]
    for name, bets in blackjack_default_data:
        if name not in blackjack_data:
            blackjack_data[name] = {'name': name, 'bets': bets, 'type': 'blackjack'}
    save_data('tables/blackjack', blackjack_data)

    poker_data = load_data('tables/poker')
    poker_default_data = [('BIG WIN', [100]), ('SMALL WIN', [10])]
    for name, bets in poker_default_data:
        if name not in poker_data:
            poker_data[name] = {'name': name, 'bets': bets, 'type': 'poker'}
    save_data('tables/poker', poker_data)

# ---------------- OTHER ----------------

def create_default_app_data():
    version = "0.64.1"
    author = "zawodev"
    freechips = 100
    save_data_raw("app/info/version", f'"{version}"')
    save_data_raw("app/info/author", f'"{author}"')
    save_data_raw("app/data/freechips", f"{freechips}")
