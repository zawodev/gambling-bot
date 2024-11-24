import discord

from gambling_bot.data.json_manager import load_data
from gambling_bot.views.view import View
from gambling_bot.models.casino import casino
from datetime import datetime

class ClaimRewardView(View):
    def __init__(self, interaction, back_view):
        super().__init__(interaction)
        self.back_view = back_view
        self.profile = casino.get_player_profile_with_id(str(interaction.user.id))

    def create_buttons(self):
        # claim button
        claim_button = discord.ui.Button(
            label="claim",
            style=discord.ButtonStyle.green,
            custom_id="claim"
        )
        claim_button.callback = self.claim

        # back button
        back_button = discord.ui.Button(
            label="back",
            style=discord.ButtonStyle.red,
            custom_id="back"
        )
        back_button.callback = self.back

        return [claim_button, back_button]

    def create_embeds(self):
        if self.profile.has_claimed_free_chips():
            return [discord.Embed(
                title="Reward Claimed",
                description=f"Next reward ({load_data("app/data/freechips")}$) in: {60 - datetime.now().minute} minutes",
                color=discord.Color.red()
            )]
        else:
            return [discord.Embed(
                title=f"Claim Hourly Reward ({load_data("app/data/freechips")}$)",
                description="You can claim your reward now",
                color=discord.Color.green()
            )]

    # --------- callbacks ---------

    async def claim(self, interaction: discord.Interaction):
        self.profile.claim_free_chips(load_data("app/data/freechips"))
        await self.edit(interaction)

    async def back(self, interaction: discord.Interaction):
        await self.back_view.edit(interaction)
