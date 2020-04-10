import discord
import datetime
from random import choice
from discord.ext import commands
from discord.utils import get

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="log")
        if channel:
            embed = discord.Embed(description=f'{len(member.guild.members)}th member joined', color=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="log")
        if channel:
            embed = discord.Embed(description='Goodbye', color=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.client.get_channel(684130494023073865)
        if channel:
            embed = discord.Embed(
                timestamp=after.created_at,
                description = f"<@!{before.author.id}>**'s message was edited in** <#{before.channel.id}>.",
                colour = discord.Colour.blurple) 
            embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.avatar_url)
            embed.set_footer(text=f"Author ID:{before.author.id} • Message ID: {before.id}")
            embed.add_field(name='Before:', value=before.content, inline=False)
            embed.add_field(name="After:", value=after.content, inline=False)
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Log(client))