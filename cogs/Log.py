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
        channel = discord.utils.get(member.guild.text_channels, name='mod-log')
        welcome_channel = discord.utils.get(member.guild.text_channels, name='lounge')
        if channel:
            embed = discord.Embed(description=f'{len(member.guild.members)}th member joined', colour=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)
        
        if welcome_channel:
            await welcome_channel.send(f'Welcome to WenRene Discord, {member.mention}! Pick a role tag in <#681672202822877207>. Enjoy your stay!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='mod-log')
        if channel:
            embed = discord.Embed(description='Goodbye', colour=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self,before,after):
        log_channel = self.client.get_channel(700137514572185662)
        if log_channel:
            user_embed = discord.Embed(title='User updates')
            user_embed.add_field(name="Name before:", value=before.name,inline=False)
            user_embed.add_field(name="Name after:", value=after.name,inline=False)
            user_embed.add_field(name="Avatar before", value=before.avatar_url,inline=False)
            user_embed.add_field(name="Avatar after", value=after.avatar_url,inline=False)
            user_embed.add_field(name="Discriminator before", value=before.discriminator,inline=False)
            user_embed.add_field(name="Discriminator after", value=after.discriminator,inline=False)
            user_embed.timestamp = datetime.datetime.utcnow()
            await log_channel.send(embed=user_embed)


def setup(client):
    client.add_cog(Log(client))