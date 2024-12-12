from gambling_bot.data.json_manager import load_data, save_data
import discord

from gambling_bot.views.start_view import StartView


async def configure(interaction: discord.Interaction):
    casino_channel_id_list = load_data('app/config/casino_channel_id_list')
    if casino_channel_id_list == {} or casino_channel_id_list is None:
        casino_channel_id_list = []
    casino_channel_id_list.append(interaction.channel_id)
    save_data('app/config/casino_channel_id_list', casino_channel_id_list)
    await interaction.response.send_message("kanał został dodany do listy kanałów kasyna", ephemeral=True)


async def run(bot):
    casino_channel_id_list = load_data('app/config/casino_channel_id_list')
    if casino_channel_id_list is not {} and casino_channel_id_list is not None:
        for channel_id in casino_channel_id_list:
            channel = await bot.fetch_channel(channel_id)
            if channel is not None:
                view = StartView(None, None)
                await view.send_to_channel(channel)
