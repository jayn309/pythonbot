import discord
from discord.ext import commands
from discord.utils import get

commands_tally = {}
class CommandEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        channel = discord.utils.get(ctx.guild.channels, name="testing")
        await channel.send(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1
            print(commands_tally)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.emoji.name == "\U0001F4CC":
            message_id = payload.message_id
            channel_id = payload.channel_id
            guild_id = payload.guild_id
            
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)
            message = await channel.fetch_message(message_id)
            await message.pin(message)

def setup(client):
    client.add_cog(CommandEvents(client))