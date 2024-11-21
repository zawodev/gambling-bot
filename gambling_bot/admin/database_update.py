import discord

from gambling_bot.admin.operation_type import OperationType
from gambling_bot.data.json_manager import load_data, save_data_raw

async def db(interaction: discord.Interaction, operation: OperationType, path: str = "", data: str = ""):
    if operation == OperationType.SAVE:
        save_data_raw(path, data)
        await interaction.response.send_message(f"saved data: {data}, to {path}", ephemeral=True)
    elif operation == OperationType.LOAD:
        data = load_data(path)
        await interaction.response.send_message(content=data, ephemeral=True)
    else:
        await interaction.response.send_message(f"operation not found", ephemeral=True)

    # save new data to casino
    #casino.load_data()
