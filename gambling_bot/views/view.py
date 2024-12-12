import discord
from discord.ext import tasks
from discord import InteractionResponse


class View(discord.ui.View):
    def __init__(self, interaction, message):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.message = message
        self.embeds = None
        self.refresh_task.start()

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
        await self.message.edit(content="", embeds=self.embeds, view=self)
        await new_interaction.response.defer()

    async def send(self, ephemeral=False):
        self.refresh()
        await self.interaction.response.send_message(embeds=self.embeds, view=self, ephemeral=ephemeral)
        self.message = await self.interaction.original_response()

    async def send_to_channel(self, channel: discord.TextChannel):
        self.refresh()
        self.message = await channel.send(embeds=self.embeds, view=self)

    async def destroy(self):
        msg = await self.interaction.original_response()
        await msg.delete()

    @tasks.loop(minutes=10)
    async def refresh_task(self):
        self.refresh()
