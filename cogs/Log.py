import discord
import datetime

from random import choice
from discord.ext import commands
from discord.utils import get
from typing import Any, List, Union, Optional

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='log')
        if channel:
            embed = discord.Embed(description=f'{len(member.guild.members)}th member joined', colour=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='log')
        if channel:
            embed = discord.Embed(description='Goodbye', colour=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Log(client))