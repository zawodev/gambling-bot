
from gambling_bot.models.table.table import Table
from gambling_bot.models.player.player import Player

class BlackJackTable(Table):
    def __init__(self, dealer, data, path):
        super().__init__(dealer, data, path)

    def deal(self, player):
        if not player.is_ready:
            player.deal(self.dealer.deck.draw(), self.dealer.deck.draw())
        self.do_checks()

    def hit(self, player):
        if player.is_ready and not player.all_hands_stand():
            player.hit(self.dealer.deck.draw())
        self.do_checks()

    def stand(self, player):
        if player.is_ready and not player.all_hands_stand():
            player.stand()
        self.do_checks()

    def double(self, player):
        if player.is_ready and not player.all_hands_stand() and player.profile.has_chips(player.hands[0].bet):
            player.profile.transfer_chips(self.dealer.profile, player.hands[0].bet)
            player.double(self.dealer.deck.draw())
        self.do_checks()

    def split(self, player):
        if player.is_ready and not player.all_hands_stand() and player.profile.has_chips(player.hands[0].bet) and not player.split_used:
            player.profile.transfer_chips(self.dealer.profile, player.hands[0].bet)
            player.split(self.dealer.deck.draw(), self.dealer.deck.draw())
        self.do_checks()

    def forfeit(self, player):
        if player.is_ready and not player.all_hands_stand():
            player.forfeit()
        self.do_checks()
