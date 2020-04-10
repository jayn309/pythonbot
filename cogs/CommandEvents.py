import discord
from discord.ext import commands
from discord.utils import get

commands_tally = {}
class CommandEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        channel = discord.utils.get(ctx.guild.chanels, name="bot-errors")
        await channel.send(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1
            print(commands_tally)

def setup(client):
    client.add_cog(CommandEvents(client))