import discord
from gambling_bot.views.view import View

class BetSelectView(View):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.bet = 0

    def create_buttons(self):
        # 1 button for each bet and a ready button when ready
        buttons = []
        for bet in self.table.table_data['bets']:
            button = discord.ui.Button(
                label=str(bet),
                style=discord.ButtonStyle.green,
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
        embed = discord.Embed(
            title="Bet Select",
            description="Choose a bet",
            color=discord.Color.green()
        )
        return [embed]

    # --------- callbacks ---------

    async def increment_bet(self, _bet: int):
        async def button_callback(interaction: discord.Interaction):
            self.bet += _bet
            await self.display(interaction.message)
        return button_callback

    async def ready(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
