import discord

from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.view import View
from gambling_bot.views.blackjack_table_view import BlackjackTableView
from gambling_bot.casino import casino

class BetSelectView(View):
    def __init__(self, interaction, table, table_type):
        self.table = table
        self.table_type = table_type
        self.bet = 0
        self.player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
        super().__init__(interaction)

    def create_buttons(self):
        # 1 button for each bet and a ready button when ready
        buttons = []
        for bet in self.table.table_data['bets']:
            button = discord.ui.Button(
                label=str(bet),
                style=discord.ButtonStyle.gray,
                custom_id=str(bet)
            )
            button.callback = self.increment_bet(int(bet))
            buttons.append(button)

        ready_button = discord.ui.Button(
            label="ready",
            style=discord.ButtonStyle.green,
            custom_id="ready"
        )
        ready_button.callback = self.ready
        buttons.append(ready_button)

        return buttons

    def create_embeds(self):
        # wyświetl gracza, nazwę stołu, ilość chipsów gracza oraz bet gracza
        embed = discord.Embed(
            title=f"{self.table.table_data['name']}",
            description=f"{self.player_profile.profile_data['name']}:\n"
                        f"chips: {self.player_profile.profile_data['chips']}\n"
                        f"bet: {self.bet}\n",
            color=discord.Color.red()
        )
        return [embed]

    # --------- callbacks ---------

    def increment_bet(self, add_bet: int):
        async def button_callback(interaction: discord.Interaction):
            available_chips = self.player_profile.profile_data['chips']
            max_bet = self.table.table_data['max_bet']
            min_bet = self.table.table_data['min_bet']

            new_bet = self.bet + add_bet
            new_bet = min(new_bet, available_chips)
            self.bet = max(min_bet, min(new_bet, max_bet))

            await self.edit(interaction)
        return button_callback

    async def ready(self, interaction: discord.Interaction):
        self.table.add_bet_player(self.player_profile, self.bet)
        match self.table_type:
            case TableType.BLACKJACK:
                view = BlackjackTableView(self.interaction, self.table)
                await view.edit(interaction)
            case TableType.POKER:
                raise NotImplementedError
            case TableType.ROULETTE:
                raise NotImplementedError
            case TableType.SLOTS:
                raise NotImplementedError
            case _:
                raise NotImplementedError
