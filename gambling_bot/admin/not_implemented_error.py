import discord

async def not_implemented_error(interaction: discord.Interaction):
    await interaction.response.send_message("not implemented!", ephemeral=True)

async def game_started_error(interaction: discord.Interaction):
    await interaction.response.send_message("game already started!", ephemeral=True)
