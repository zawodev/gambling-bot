from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.dealer.dealer import Dealer
from gambling_bot.models.table.blackjack_table import BlackJackTable
from gambling_bot.models.table.poker_table import PokerTable
from gambling_bot.data.json_manager import load_data
import random

class Casino:
    def __init__(self):
        self.bot = None
        self.player_profiles = []
        self.dealer_profiles = []
        self.available_dealers = []
        self.blackjack_tables = []
        self.poker_tables = []

    def load_data(self):
        self.player_profiles = [Profile(player_data, f'profiles/players/{player_key}')
                                for player_key, player_data in load_data('profiles/players').items()]
        self.dealer_profiles = [Profile(dealer_data, f'profiles/dealers/{dealer_key}')
                                for dealer_key, dealer_data in load_data('profiles/dealers').items()]

        print(self.player_profiles)

        self.available_dealers = [Dealer(profile) for profile in self.dealer_profiles]
        random.shuffle(self.available_dealers)

        self.blackjack_tables = [BlackJackTable(self.get_random_dealer(), table_data, f'tables/blackjack/{table_key}')
                                 for table_key, table_data in load_data('tables/blackjack').items()]
        self.poker_tables = [PokerTable(self.get_random_dealer(), table_data, f'tables/poker/{table_key}')
                             for table_key, table_data in load_data('tables/poker').items()]

    def setup_bot(self, bot):
        self.bot = bot

    def get_random_dealer(self):
        dealer = self.available_dealers.pop()
        self.available_dealers.insert(0, dealer)
        return dealer

    def get_player_profile_with_id(self, player_profile_id):
        for profile in self.player_profiles:
            if profile.profile_data.path.split('/')[-1] == player_profile_id:
                return profile
        return None

# uzyskanie instancji casino
casino = Casino()
