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

    @commands.Cog.listener()
    async def on_message_edit(self, before,after):
        channel = discord.utils.get(before.guild.channels, name='log')
        if before.author.id == 685307035142586380 or before.author.id == 325387620266016768 or before.author.id == 234395307759108106 or before.author.id == 235088799074484224 or before.author.id == 172002275412279296 or before.author.id == 359401025330741248:
            return
        if before.content == after.content:
            return
        else:
            edit_embed = discord.Embed(description=f'@{before.author.name} edited a message in #{before.channel}')
            edit_embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.avatar_url)
            edit_embed.set_footer(text=f"Author ID:{before.author.id} • Message ID: {before.id}")
            edit_embed.add_field(name='Before:', value=before.content, inline=False)
            edit_embed.add_field(name="After:", value=after.content, inline=False)
            edit_embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=edit_embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.client.get_channel(684130494023073865)
        if not message.author.id == 685307035142586380:
            delete_embed = discord.Embed(title="Message deletion", decription=f"Action by {message.author.name} in #{message.channel}.",
                            colour = message.author.colour, 
                            timestamp=datetime.datetime.utcnow())
            fields = [("Content",message.content, False)]
            for name, value, inline in fields:
                delete_embed.add_field(name=name, value=value,inline=inline)
            await log_channel.send(embed=delete_embed)
			


def setup(client):
    client.add_cog(Log(client))