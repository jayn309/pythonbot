import discord
from discord.ext import commands
from typing import List

FIELD_VALUE_LIMIT = 1024

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def showemoji(self,ctx,channel,emoji: discord.Emoji =None):
        channel_mentions = ctx.message.channel_mentions
        channel = discord.utils.get(channel_mentions, mention=channel)
        def split_message(message: str, limit: int = 2000):
            """Splits a message into a list of messages if it exceeds limit.
            Messages are only split at new lines.
            Discord message limits:
            Normal message: 2000
            Embed description: 2048
            Embed field name: 256
            Embed field value: 1024"""

            if len(message) <= limit:
                return [message]
            else:
                lines = message.splitlines()
                new_message = ""
                message_list = []
                for line in lines:
                    if len(new_message+line+"\n") <= limit:
                        new_message += line+"\n"
                    else:
                        message_list.append(new_message)
                        new_message = ""
                if new_message:
                    message_list.append(new_message)
                return message_list

        """Displays all available custom emoji in this server"""
        emojis: List[discord.Emoji] = ctx.guild.emojis
        if not emojis:
            return await ctx.send("This server has no custom emojis.")
        for e in emojis:
            if not e.animated:
                normal = e
        for e in emojis:
            if e.animated:
                animated = e
        if normal:
            emojis_str = "\n".join(normal)
            fields = split_message(emojis_str, FIELD_VALUE_LIMIT)
            await channel.send(normal)
        if animated:
            emojis_str = "\n".join(animated)
            fields = split_message(emojis_str, FIELD_VALUE_LIMIT)
            await channel.send(animated)

def setup(client):
    client.add_cog(Emotes(client))