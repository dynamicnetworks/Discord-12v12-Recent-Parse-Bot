import json
import asyncio
from discord.ext import commands
from cogs.command_recent import get_embed

config = json.load(open('config.json'))

client = commands.Bot(command_prefix=config['prefix'])


@client.event
async def on_ready():
    while True:
        ids = json.load(open('config.json'))
        while ids['message_id'] == -1:
            ids = json.load(open('config.json'))
            print("Please set a channel with the 'recent' command.")
            await asyncio.sleep(5)
        try:
            msg = await \
                client.get_guild(ids['server_id']).get_channel(ids['channel_id']).fetch_message(ids['message_id'])
            await msg.edit(embed=get_embed())
        except:
            pass
        await asyncio.sleep(5)


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    client.unload_extension('cogs.command_recent')
    client.load_extension('cogs.command_recent')
    await ctx.send("Reloaded.")
    print("Reloaded recent cog.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

client.load_extension('cogs.command_recent')
client.run(config['token'])
