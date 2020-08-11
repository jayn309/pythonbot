import discord
from discord.ext import commands

from typing import Optional
from discord import Embed
from discord.utils import get
from discord.ext.commands import command

def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

	params = " ".join(params)

	return f"`{cmd_and_aliases} {params}`"

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                            description=syntax(command),
                            colour=ctx.author.colour)
        embed.add_field(name="Command description", value=command.description or command.brief)              
        await ctx.send(embed=embed)

    @commands.command(name="help")
    @commands.guild_only()
    async def show_help(self, ctx, cmd: Optional[str]):
        #Shows this message
        if cmd is None:
            embed = discord.Embed(description='Here is the list of commands! \nFor more info on a specific command use _help {command}',
                        colour = discord.Colour.blurple())
            embed.set_author(name="Command list")
            embed.add_field(name='👑 **Admin**', value="`ping`  `kick`  `ban`  `unban` `mute`  `unmute`  `purge`  `say`  `edit`  `showemotes`  `addrole`  `removerole`  `move`  `alladdrole`  `allremoverole`  `countr`  `showemotes`  `slowmode`  `limit`  `emojistat`"
                ,inline=False)
            embed.add_field(name='🎉 **Fun**', value="`eightb`  `coinflip`  `f`  `choose`  `hug`  `rate`  `hot`  `slot`  `tableflip`  `unflip`  `calc`  `numgame`  `rps`  `riddle`  `pun`"
                ,inline=False)
            embed.add_field(name='🔧 **Utility**', value="`avatar`  `usersinfo`  `serverinfo`  `google`  `youtube`  `spotify`  `translate`  `covid`  `enlarge`  `vote`  `poll`  `instagram`  `wolframalpha`  `weather`  `urban`")
            await ctx.send(embed=embed)
        
        else:

            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("That command does not exist.")

def setup(bot):
    bot.add_cog(HelpCommands(bot))
