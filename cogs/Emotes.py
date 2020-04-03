import discord
from discord.ext import commands

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def showemoji(self, message,*args):
        """Displays all available custom emoji in this server"""
        guild = message.guild
        if len(args) > 0:
            try:
                server = client.get_server(args[0])
                if not (isowner(message.author) or server.get_member(message.author.id)):
                    server = message.server
                emojis = ' '.join(['<:{0.name}:{0.id}>'.format(emoji) if server==message.server else '<:{0.name}:{0.id}> `<:{0.name}:{0.id}>`\n'.format(emoji) for emoji in server.emojis])
            except:
                await self.client.send_message(message.channel,message.author.mention + ' You provided an invalid server ID.')
                return

        if not 'emojis' in locals():
            emojis = ' '.join(['<:{0.name}:{0.id}>'.format(emoji) if server==message.server else '`<:{0.name}:{0.id}>`'.format(emoji) for emoji in server.emojis])
            
        await self.client.send_message(message.channel,'Emoji in __{}__\n'.format(server.name) + emojis)

def setup(client):
    client.add_cog(Emotes(client))