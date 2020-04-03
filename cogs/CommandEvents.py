import discord
from discord.ext import commands

commands_tally = {}
class CommandEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1
            print(commands_tally)

    @commands.Cog.listener()
    async def on_message(self, message):
     if (message.content[0]==":" and message.content[-1]==":") or (message.content[0]=="," and message.content[-1]==","):
            if not " " in message.content:
                requestedemoji=message.content[1:-1]
                emotes=self.client.emojis
                for i in range(len(emotes)):
                    if emotes[i].name==requestedemoji:
                        await message.channel.send(emotes[i])
                        return
    
def setup(client):
    client.add_cog(CommandEvents(client))