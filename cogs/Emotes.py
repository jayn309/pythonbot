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
        normal = [e for e in emojis if not e.animated]
        animated = [str(e) for e in emojis if e.animated]
        if normal:
                emojis_str = "\n".join(["".join(normal[i:i+10]) for i in range(0,len(normal),10)])
                await channel.send(emojis_str)
        if animated:
                emojis_str = "\n".join(["".join(animated[i:i+10]) for i in range(0,len(animated),10)])
                await channel.send(emojis_str)

def setup(client):
    client.add_cog(Emotes(client))