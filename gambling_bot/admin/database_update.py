import discord

from gambling_bot.admin.operation_type import OperationType
from gambling_bot.data.json_manager import load_data, save_data, remove_data, move_data
from gambling_bot.casino import casino

async def db(interaction: discord.Interaction, operation: OperationType, path: str = "", data: str = ""):
    if data is not None and data.isdigit():
        data = int(data)
    if operation == OperationType.REMOVE:
        remove_data(path)
        await interaction.response.send_message(f"removed data from {path}", ephemeral=True)
    elif operation == OperationType.SAVE:
        save_data(path, data)
        await interaction.response.send_message(f"saved data: {data}, to {path}", ephemeral=True)
    elif operation == OperationType.MOVE:
        move_data(path, data)
        await interaction.response.send_message(f"moved data from {path} to {data}", ephemeral=True)
    elif operation == OperationType.LOAD:
        data = load_data(path)
        await interaction.response.send_message(content=data, ephemeral=True)
    else:
        await interaction.response.send_message(f"operation not found", ephemeral=True)

    # save new data to casino
    casino.load_data()
