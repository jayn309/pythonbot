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

    @commands.Cog.listener()
    async def on_user_update(self,before,after):
        channel = discord.utils.get(after.guild.channels, name='users-log')
        if before.name != after.name and after.name is not None:
            await channel.send(f'{before.name}, {after.name}')
        if before.avatar != after.avatar and after.avatar is not None:
            pass
        if before.discriminator != after.discriminator and after.discriminator is not None:
            await channel.send(f'{before.discriminator}, {after.discriminator}')

def setup(client):
    client.add_cog(Log(client))