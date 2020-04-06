import discord
import re
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
    async def on_message(self,message):
        if (message.content[0]==":" and message.content[-1]==":") or (message.content[0]=="," and message.content[-1]==",") and not message.guild==None:

           #regex for finding emote matches
            pattern = re.compile(r"\s*[:,][\w]+[:,]\s*")
            matches = pattern.findall(message.content)

            matchlength = 0
            #if emotes found
            if not matches == None:
                #check if message has anything other than emotes and spaces
                for x in matches:
                    matchlength += len(x)

                #if it doesn't then put together list of emotes to send
                if matchlength == len(message.content):

                    #print(f"message has nothing but emotes. {len(message.content)}={matchlength}")
                    emotes = self.client.emojis
                    finalmsg=""
                    for x in matches:
                        requestedemoji = x.strip()[1:-1]
                        for i in range(len(emotes)):
                            if emotes[i].name == requestedemoji:
                                finalmsg+=((str)(emotes[i]))
                                break
                    #if finalmsg isn't empty then send
                    if len(finalmsg)>0:
                        await message.channel.send(finalmsg)
                    return
                else:
                    pass
                    #print(f"message has things other than emotes. {len(message.content)}!={matchlength}")
def setup(client):
    client.add_cog(CommandEvents(client))