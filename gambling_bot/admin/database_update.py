import discord
import os

from gambling_bot.admin.operation_type import OperationType
from gambling_bot.data.json_manager import load_data_raw, save_data_raw
from gambling_bot.models.casino import casino

async def db(interaction: discord.Interaction, operation: OperationType, path: str = "", data: str = ""):
    if operation == OperationType.SAVE:
        save_data_raw(path, data)
        await interaction.response.send_message(f"saved data: {data}, to {path}", ephemeral=True)
    elif operation == OperationType.LOAD:
        data = f"```{load_data_raw(path)}```"
        if len(data) < 2000:
            await interaction.response.send_message(content=data, ephemeral=True)
        else:
            with open("temp.txt", "w") as file:
                file.write(data)
            await interaction.response.send_message(file=discord.File("temp.txt"), ephemeral=True)
            os.remove("temp.txt")
    else:
        await interaction.response.send_message(f"operation not found", ephemeral=True)

    # save new data to casino
    casino.load_data()
