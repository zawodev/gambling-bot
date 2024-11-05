import discord

from gambling_bot.admin.operation_type import OperationType
from gambling_bot.data.json_manager import load_data, save_data, delete_data

async def db(interaction: discord.Interaction, operation: OperationType, path: str, data: str = None):
    path = path.split('/')
    if operation == OperationType.ADD:
        db_add(data, *path)
        await interaction.response.send_message(f"added data to {path}", ephemeral=True)
    elif operation == OperationType.REMOVE:
        db_remove(*path)
        await interaction.response.send_message(f"removed data from {path}", ephemeral=True)
    elif operation == OperationType.MODIFY:
        db_modify(data, *path)
        await interaction.response.send_message(f"modified data in {path}", ephemeral=True)
    else:
        await interaction.response.send_message(f"operation not found", ephemeral=True)

def db_add(data, *path):
    save_data(data, *path)

def db_remove(*path):
    delete_data(*path)

# wszystko w bazie dac jako string imo i zamieniac przy odczycie
def db_modify(new_data, *path):
    #for path = "profiles/players/1234" and new_data = "5678" it will change "1234" to "5678"
    data = load_data(*path)
    data = new_data
    save_data(data, *path)
