import discord

from gambling_bot.models.player.player import Player
from gambling_bot.models.profile.profile import Profile
from gambling_bot.models.dict_data.table_data import TableData
from gambling_bot.models.hand.hand import Hand
from gambling_bot.models.table.table_status import TableStatus

import asyncio
from datetime import datetime, timedelta

from gambling_bot.models.table.table_type import TableType


class Table:
    def __init__(self, dealer, data, path):
        self.table_data = TableData(data, path)
        match self.table_data['type']:
            case "blackjack": self.type = TableType.BLACKJACK
            case "poker": self.type = TableType.POKER
            case "roulette": self.type = TableType.ROULETTE
            case "none": self.type = TableType.NONE
            case _: self.type = TableType.NONE

        self.players = []
        self.dealer = dealer

        self.table_status = TableStatus.WAITING_FOR_PLAYERS

        self.last_activity_time = datetime.now()
        asyncio.create_task(self.monitor_activity())

    def add_bet_player(self, player_profile: Profile, bet: int):
        if self.table_status == TableStatus.WAITING_FOR_PLAYERS:
            player_id = player_profile.profile_data.path.split('/')[-1]
            player: Player = self.get_player(player_id)
            if player is None:
                player = Player(player_profile)
                self.players.append(player)

            if not player.is_ready and player_profile.has_chips(bet) and bet > 0:
                player_profile.transfer_chips(self.dealer.profile, bet)
                player.add_bet(bet)
                self.update_activity()

    # ============ PLAYER ACTIONS ============

    def update_activity(self):
        self.last_activity_time = datetime.now()

    async def monitor_activity(self):
        while True:
            await asyncio.sleep(10)
            is_time = datetime.now() - self.last_activity_time > timedelta(minutes=5)
            if len(self.players) > 0 and not self.table_status == TableStatus.FINISHED and is_time:
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
        self.table_status = TableStatus.IN_PROGRESS

    def reset_game(self):
        self.table_status = TableStatus.WAITING_FOR_PLAYERS
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

        self.table_status = TableStatus.FINISHED

    # ============ CHECKS ============

    def all_stands(self):
        return all(player.all_hands_stand() for player in self.players) and len(self.players) > 0

    def all_ready(self):
        return all(player.is_ready for player in self.players) and len(self.players) > 0

    def get_all_bets(self):
        return sum(player.get_all_bets() for player in self.players)

    def can_join(self):
        return self.table_status == TableStatus.WAITING_FOR_PLAYERS or self.table_status == TableStatus.FINISHED

    def __str__(self):
        if self.can_join():
            emoji = "✅"
        else:
            emoji = "❌"
        return f"{emoji}{self.table_data['name']}: {', '.join([player.profile.profile_data['name'] for player in self.players])}"
