import discord
from discord.ext import commands
from typing import List


class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def showemotes(self,ctx,channel,emoji: discord.Emoji =None):
        channel_mentions = ctx.message.channel_mentions
        channel = discord.utils.get(channel_mentions, mention=channel)

        """Displays all available custom emoji in this server"""
        emojis: List[discord.Emoji] = ctx.guild.emojis
        if not emojis:
            return await ctx.send("This server has no custom emojis.")
        normal = [str(e) for e in emojis if not e.animated]
        animated = [str(e) for e in emojis if e.animated]
        if normal:
            for i in range(0,len(normal),10):
                emojis_str = "".join(normal[i:i+10]) 
                await channel.send(emojis_str)
        if animated:
             for i in range(0,len(animated),10):
                emojis_str = "".join(animated[i:i+10])
                await channel.send(emojis_str)

def setup(client):
    client.add_cog(Emotes(client))