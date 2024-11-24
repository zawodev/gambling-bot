import discord

from gambling_bot.models.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.dict_data.table_data import TableData
from gambling_bot.models.hand import Hand

import asyncio
from datetime import datetime, timedelta


class Table:
    def __init__(self, dealer, data, path):
        self.table_data = TableData(data, path)

        self.players = []
        self.dealer = dealer

        self.is_game_started = False
        self.is_game_finished = False

        # from gambling_bot.models.dict_data.table_status import TableStatus
        #self.table_status = None #instead of is_game_started and is_game_finished

        self.last_activity_time = datetime.now()
        asyncio.create_task(self.monitor_activity())

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
                self.update_activity()

    def update_activity(self):
        self.last_activity_time = datetime.now()

    async def monitor_activity(self):
        while True:
            await asyncio.sleep(10)
            is_time = datetime.now() - self.last_activity_time > timedelta(minutes=5)
            if len(self.players) > 0 and not self.is_game_finished and is_time:
                await self.notify_players()
                self.reset_game()

    async def notify_players(self):
        for player in self.players:
            player: Player
            from gambling_bot.setup import bot_ref as bot
            user = await bot.fetch_user(int(player.profile.profile_data.get_key()))
            user: discord.User
            message = (f"stół {self.table_data['name']} został zresetowany z uwagi na brak aktywności, "
                       f"twój zakład o wysokości {player.get_all_bets()}$ poszedł się jebać")
            try:
                await user.send(message)
            except discord.Forbidden:
                print(f"cant send message to {user} (forbidden)")

    # ============ GAME ACTIONS ============

    def do_checks(self):
        self.check_all_ready()
        self.check_all_stands()

    def check_all_ready(self):
        if self.all_ready():
            self.start_game()

    def check_all_stands(self):
        if self.all_stands():
            self.finish_game()

    # ============ GETTERS ============

    def get_player(self, player_id):
        for player in self.players:
            if player.profile.profile_data.path.split('/')[-1] == str(player_id):
                return player
        return None

    # ============ GAME ============

    def start_game(self):
        self.dealer.hand.is_ready = True
        self.is_game_started = True

    def reset_game(self):
        self.is_game_started = False
        self.is_game_finished = False
        self.players = []
        self.dealer.init()
        self.update_activity()

    def finish_game(self):
        self.dealer.hand.is_hidden = False
        self.dealer.hand.is_ready = True
        self.dealer.hand.is_finished = True

        for player in self.players:
            player: Player
            date_key = datetime.now().strftime("%Y-%m-%d %H:00")
            player.profile.profile_data.increment(f'games_played_by_date/{date_key}/{self.table_data['type']}')
            # give players winnings
            for hand in player.hands:
                hand: Hand
                winnings = int(hand.calculate_winnings(player.profile, self.dealer.hand))
                self.dealer.profile.transfer_chips(player.profile, winnings)

        self.is_game_finished = True

    # ============ CHECKS ============

    def all_stands(self):
        return all(player.all_hands_stand() for player in self.players) and len(self.players) > 0

    def all_ready(self):
        return all(player.is_ready for player in self.players) and len(self.players) > 0

    def get_all_bets(self):
        return sum(player.get_all_bets() for player in self.players)

    def __str__(self):
        # emoji = "✅" if self.is_game_started else "❌"
        return f"{self.table_data['name']}: {', '.join([player.profile.profile_data['name'] for player in self.players])}"
