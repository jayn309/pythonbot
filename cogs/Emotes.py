import discord
import re
import operator
from discord.ext import commands, menus
from typing import List

class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=10)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == 685307035142586380:
            return
        #if message is empty
        if len(message.content)==0:
            return
        if (message.content[0]==":" and message.content[-1]==":") or (message.content[0]=="," and message.content[-1]==","):

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

    @commands.command(aliases=[ 'shem'],brief='show all emotes of server in a channel',description='Mention a channel to show all emote there\n _shem #channel')
    @commands.has_guild_permissions(administrator=True)
    async def showemotes(self,ctx,channel,emoji: discord.Emoji =None):
        channel_mentions = ctx.message.channel_mentions
        channel = discord.utils.get(channel_mentions, mention=channel)

        """Displays all available custom emoji in this server"""
        emojis: List[discord.Emoji] = ctx.guild.emojis
        if not emojis:
            return await ctx.send("This server has no custom emojis.")
        normal = [str(e) for e in emojis if not e.animated]
        animated = [str(e) for e in emojis if e.animated]
        if normal:
            for i in range(0,len(normal),10):
                emojis_str = "".join(normal[i:i+10]) 
                await channel.send(emojis_str)
        if animated:
             for i in range(0,len(animated),10):
                emojis_str = "".join(animated[i:i+10])
                await channel.send(emojis_str)
        await channel.send(f"```For non nitro user, you can do ,emotename, or :emotename: to use available animated emotes in this server.```")

    @commands.command(aliases=[ 'emst'],brief='show stat of server emotes')
    @commands.has_guild_permissions(administrator=True)
    async def emojistat(self, ctx, channel : discord.TextChannel=None):
        channel = discord.TextChannel if not channel else channel
        allemojis = [str(e) for e in ctx.guild.emojis]
        dict = {}
        async with ctx.typing():
            async for message1 in ctx.channel.history(limit = 5000, oldest_first = False):
                if message1.content in allemojis:
                    if message1.content in dict.keys():
                        dict[f"{message1.content}"] += 1
                    else:
                        dict[f"{message1.content}"] = 1
        sorted_d = (sorted(dict.items(), key=operator.itemgetter(1),reverse=True))
        pages = menus.MenuPages(source=MySource(list(sorted_d)), clear_reactions_after=True,timeout=300.0, delete_message_after=True)
        await pages.start(ctx)

def setup(client):
    client.add_cog(Emotes(client))