import discord
from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.table_data import TableData
from gambling_bot.models.hand import Hand

class Table:
    def __init__(self, dealer, data, path):
        self.table_data = TableData(data, path)
        self.active_game_message = None
        self.players = []
        self.dealer = dealer
        self.is_game_started = False

    def add_bet_player(self, player_profile: Profile, bet: int):
        player_id = player_profile.profile_data.path[-1]
        player: Player = self.get_player(player_id)
        if player is None:
            player = Player(player_profile)
            self.players.append(player)

        bet = min(bet, player_profile.profile_data['chips'])
        bet = min(bet, self.table_data['max_bet'] - player.get_bet())
        bet = max(bet, self.table_data['min_bet'] - player.get_bet())

        if not player.is_ready and player.has_chips(bet):
            player_profile.transfer_chips(self.dealer.profile, bet)
            player.add_bet(bet)

    def check_end_game(self):
        if self.all_stands():
            self.end_game()

    def check_all_stands(self):
        if self.all_stands():
            self.dealer.hand.is_hidden = False
            self.dealer.hand.is_ready = True
            self.dealer.hand.is_finished = True

            for player in self.players:
                player: Player
                # give players winnings
                for hand in player.hands:
                    hand: Hand
                    winnings = int(hand.calculate_winnings(self.dealer.hand))
                    self.dealer.profile.transfer_chips(player.profile, winnings)


    def check_all_ready(self):
        if self.all_ready():
            self.dealer.hand.is_ready = True
            self.is_game_started = True


    def get_player(self, player_id):
        for player in self.players:
            if player.profile.profile_data.path.split('/')[-1] == str(player_id):
                return player
        return None

    # ============ GAME ============

    def start_game(self, game_message):
        self.active_game_message = game_message

    def end_game(self):
        self.active_game_message = None
        self.players = []
        self.dealer.init()
        #self.table_data.save()

    # ============ CHECKS ============

    def all_stands(self):
        return all(player.all_hands_stand() for player in self.players) and len(self.players) > 0

    def all_ready(self):
        return all(player.is_ready for player in self.players) and len(self.players) > 0

    def get_all_bets(self):
        return sum(player.get_all_bets() for player in self.players)
