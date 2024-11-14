import discord
from discord import InteractionResponse


class View(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.interaction = interaction
        self.embeds = None

    def create_buttons(self):
        raise NotImplementedError

    def create_embeds(self):
        raise NotImplementedError

    def refresh(self):
        # refresh embeds
        self.embeds = self.create_embeds()

        # refresh buttons
        self.clear_items()
        for button in self.create_buttons():
            self.add_item(button)

    async def edit(self, new_interaction: discord.Interaction):
        self.refresh()
        message = await self.interaction.original_response()
        await message.edit(content="", embeds=self.embeds, view=self)
        await new_interaction.response.defer()

    async def send(self, ephemeral=False):
        self.refresh()
        await self.interaction.response.send_message(embeds=self.embeds, view=self, ephemeral=ephemeral)

    async def destroy(self):
        msg = await self.interaction.original_response()
        await msg.delete()
