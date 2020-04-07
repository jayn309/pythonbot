import discord
from discord.ext import commands
from typing import List


class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def showemoji(self,ctx,channel,emoji: discord.Emoji =None):
        channel_mentions = ctx.message.channel_mentions
        channel = discord.utils.get(channel_mentions, mention=channel)

        """Displays all available custom emoji in this server"""
        emojis: List[discord.Emoji] = ctx.guild.emojis
        if not emojis:
            return await ctx.send("This server has no custom emojis.")
        normal = [str(e) for e in emojis if not e.animated]
        animated = [str(e) for e in emojis if e.animated]
        if normal:
            emojis_str = "".join(normal)
            await channel.send(emojis_str)
        if animated:
            emojis_str = "".join(animated)
            await channel.send(emojis_str)

def setup(client):
    client.add_cog(Emotes(client))