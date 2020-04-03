import discord
from discord.ext import commands

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def showemoji(self,ctx, message,*args):
        """Displays all available custom emoji in this server"""
        guild = message.guild
        if len(args) > 0:
            try:
                guild = client.get_guild(args[0])
                if not (isowner(message.author) or guild.get_member(message.author.id)):
                    guild = message.guild
                emojis = ' '.join(['<:{0.name}:{0.id}>'.format(emoji) if guild == message.guild else '<:{0.name}:{0.id}> `<:{0.name}:{0.id}>`\n'.format(emoji) for emoji in guild.emojis])
            except:
                await ctx.send(message.channel,message.author.mention + ' You provided an invalid server ID.')
                return

        if not 'emojis' in locals():
            emojis = ' '.join(['<:{0.name}:{0.id}>'.format(emoji) if guild == message.guild else '`<:{0.name}:{0.id}>`'.format(emoji) for emoji in guild.emojis])
            
        await ctx.send(message.channel,emojis)

def setup(client):
    client.add_cog(Emotes(client))