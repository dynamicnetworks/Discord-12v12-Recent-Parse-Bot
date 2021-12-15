import json
import discord
import datetime
import requests
from discord.ext import commands


def get_embed():
    info = Info()
    board = info.get_recents()
    now = datetime.datetime.now()
    current_time = str(now.strftime("%I:%M:%S"))
    board.sort(reverse=True)
    timestamp_list = []
    recent_list = []

    for recent in board:
		
        date = datetime.datetime.fromtimestamp(recent[0])
        timestamp_list.append(date.strftime("%c"))
        recent_list.append(recent[1])

    embed = discord.Embed(
        color=0x7E1212,
        title="Recent Match Parse Searches (Last 20)\nhttps://dotaworkshop.com/match",
    )
    embed.add_field(name="Date", value="{}".format('\n'.join(timestamp_list)), inline=True)
    embed.add_field(name="Match ID / Stats Url", value="{}".format('\n' .join(str(recent) for recent in recent_list)), inline=True)
    embed.set_footer(text="Last updated at: " + current_time + " CST")
    embed.set_thumbnail(
        url="https://dotaworkshop.com/dist/images/logo.png")
    return embed
	


class Info:
    def __init__(self):
        self.url = "https://api.dotaworkshop.com/v3/MatchDetails/recent-parse/get"

    def get_list(self):
        return requests.request("GET", self.url).text

    def get_recents(self):
        recents = json.loads(self.get_list())[-20:]
        board = []
        for recent in recents:
            board.append([
                recent["timestamp"],
                recent["matchid"]
            ])
        return board


class MatchID(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def recent(self, ctx):
        message = await ctx.send(embed=get_embed())

        message_id = message.id
        channel_id = message.channel.id
        guild_id = message.guild.id

        with open('config.json') as f:
            config = json.load(f)
        config['message_id'] = message_id
        config['channel_id'] = channel_id
        config['server_id'] = guild_id

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)


def setup(client):
    client.add_cog(MatchID(client))
