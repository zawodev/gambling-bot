import discord

from gambling_bot.admin.not_implemented_error import not_implemented_error
from gambling_bot.data.json_manager import load_data
from gambling_bot.views.view import View
from gambling_bot.casino import casino

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
        embed = discord.Embed(
            title="Claim Reward",
            description="You have a reward to claim",
            color=discord.Color.green()
        )
        # print reward claimed if profile.has_claimed_free_chips else print reward to claim and when it can be claimed
        return [embed]

    # --------- callbacks ---------

    async def claim(self, interaction: discord.Interaction):
        self.profile.claim_free_chips(load_data("app/data/free_chips"))
        await self.edit(interaction)

    async def back(self, interaction: discord.Interaction):
        await self.back_view.edit(interaction)
