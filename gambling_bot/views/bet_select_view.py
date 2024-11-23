import discord

from gambling_bot.admin.not_implemented_error import not_implemented_error
from gambling_bot.models.table.table_type import TableType
from gambling_bot.views.view import View
from gambling_bot.views.blackjack_table_view import BlackjackTableView
from gambling_bot.casino import casino

class BetSelectView(View):
    def __init__(self, interaction, table, table_type):
        self.table = table
        self.table_type = table_type
        self.bet = 0
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
        player_profile = casino.get_player_profile_with_id(str(self.interaction.user.id))
        embed = discord.Embed(
            title=f"{self.table.table_data['name']}",
            description=f"{player_profile.profile_data['name']}:\n"
                        f"chips: {player_profile.profile_data['chips']}\n"
                        f"bet: {self.bet}\n",
            color=discord.Color.red()
        )
        return [embed]

    # --------- callbacks ---------

    def increment_bet(self, add_bet: int):
        async def button_callback(interaction: discord.Interaction):
            player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
            available_chips = player_profile.profile_data['chips']
            max_bet = self.table.table_data['max_bet']
            min_bet = self.table.table_data['min_bet']

            self.bet += max(min_bet, add_bet)

            if self.bet > available_chips:
                self.bet = available_chips

            if self.bet > max_bet:
                self.bet = max_bet

            await self.edit(interaction)
        return button_callback

    async def ready(self, interaction: discord.Interaction):
        if self.bet > 0:
            player_profile = casino.get_player_profile_with_id(str(interaction.user.id))
            self.table.add_bet_player(player_profile, self.bet)
            match self.table_type:
                case TableType.BLACKJACK:
                    view = BlackjackTableView(interaction, self.table, self)
                    await view.send()
                    await self.destroy()
                case TableType.POKER:
                    await not_implemented_error(interaction)
                case TableType.ROULETTE:
                    await not_implemented_error(interaction)
                case TableType.SLOTS:
                    await not_implemented_error(interaction)
                case _:
                    await not_implemented_error(interaction)
        else:
            await self.edit(interaction)
