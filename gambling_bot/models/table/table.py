import discord
from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.table.table_data import TableData
from gambling_bot.models.hand import Hand

class Table:
    def __init__(self, dealer, data, path):
        self.table_data = TableData(data, path)

        self.players = []
        self.dealer = dealer

        self.is_game_started = False
        self.is_game_finished = False

    def add_bet_player(self, player_profile: Profile, bet: int):
        if self.is_game_finished:
            self.reset_game()

        if not self.is_game_started:
            player_id = player_profile.profile_data.path.split('/')[-1]
            player: Player = self.get_player(player_id)
            if player is None:
                player = Player(player_profile)
                self.players.append(player)

            if not player.is_ready and player_profile.has_chips(bet) and bet > 0:
                player_profile.transfer_chips(self.dealer.profile, bet)
                player.add_bet(bet)

    # ============ GAME ACTIONS ============

    def do_checks(self):
        self.check_all_ready()
        self.check_all_stands()

    def check_all_ready(self):
        if self.all_ready():
            self.dealer.hand.is_ready = True
            self.start_game()

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
            self.finish_game()

    # ============ GETTERS ============

    def get_player(self, player_id):
        for player in self.players:
            if player.profile.profile_data.path.split('/')[-1] == str(player_id):
                return player
        return None

    # ============ GAME ============

    def start_game(self):
        self.is_game_started = True

    def reset_game(self):
        self.is_game_started = False
        self.is_game_finished = False
        self.players = []
        self.dealer.init()

    def finish_game(self):
        self.is_game_finished = True

    # ============ CHECKS ============

    def all_stands(self):
        return all(player.all_hands_stand() for player in self.players) and len(self.players) > 0

    def all_ready(self):
        return all(player.is_ready for player in self.players) and len(self.players) > 0

    def get_all_bets(self):
        return sum(player.get_all_bets() for player in self.players)

    def __str__(self):
        # print <table name>: [players / ready players]
        ready_players_len = len([player for player in self.players if player.is_ready])
        return f"{self.table_data['name']}: [{len(self.players)}/{ready_players_len}] players"
