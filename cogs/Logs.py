import discord
import datetime

from discord.utils import get
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = discord.utils.get(self.client.get_channels, name='log')
        em = discord.Embed(title=f"Message deleted in :"
                                         f" {str(message.channel.name)}",
                                   colour=discord.Color.purple)
        em.add_field(name=f"{str(message.author)} "
                                  f"*`({str(message.author.id)})`* "
                                  f"deleted :", value=str(message.content))
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)

def setup(client):
    client.add_cog(Logs(client))