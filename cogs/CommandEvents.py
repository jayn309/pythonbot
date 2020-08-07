import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import CommandNotFound

commands_tally = {}
class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        else:
            await ctx.send(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1
            print(commands_tally)


def setup(bot):
    bot.add_cog(CommandEvents(bot))