import discord
from discord.ext import commands
from typing import List

FIELD_VALUE_LIMIT = 1024

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def showemoji(self,ctx, emoji: discord.Emoji =None):
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
        normal = [str(e) for e in emojis if not e.animated]
        animated = [str(e) for e in emojis if e.animated]
        embed = discord.Embed(title="Custom Emojis", color=discord.Color.blurple())
        if normal:
            emojis_str = "\n".join(normal)
            fields = split_message(emojis_str, FIELD_VALUE_LIMIT)
            for i, value in enumerate(fields):
                if i == 0:
                    name = f"Regular ({len(normal)})"
                else:
                    name = "\u200F"
                embed.add_field(name=name, value=value.replace("\n", ""))
        if animated:
            emojis_str = "\n".join(animated)
            fields = split_message(emojis_str, FIELD_VALUE_LIMIT)
            for i, value in enumerate(fields):
                if i == 0:
                    name = f"Animated (Nitro required) or ,emotename, to use in server ({len(animated)})"
                else:
                    name = "\u200F"
                embed.add_field(name=name, value=value.replace("\n", ""))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Emotes(client))