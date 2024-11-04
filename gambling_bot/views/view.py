import discord

class View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.embeds = self.create_embeds()
        for button in self.create_buttons():
            self.add_item(button)

    def create_buttons(self):
        raise NotImplementedError

    def create_embeds(self):
        raise NotImplementedError

    async def display(self, message: discord.Message):
        await message.edit(embeds=self.embeds, view=self)
