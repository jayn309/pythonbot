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
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")

    
    async def help (self,ctx):
        author = ctx.message.author

        embed = discord.Embed(description='Here is the list of commands! \n For more info on a specific command, use _help {command}',
                    colour = discord.Colour.blurple())

        embed.set_author(name="Commands list", icon_url=self.client.avatar_url)
        embed.add_field(name=r'\U+1F451 Admin', value="kick ban unban mute unmute purge say edit showemotes addrole removerole move alladdrole allremoverole countr"
            ,inline=False)

        embed.set_author(name="Commands list", icon_url=self.client.avatar_url)
        embed.add_field(name=r'U+1F389 Fun', value="8ball coinflip f choose hug rate hot slot tableflip unflip add subtract multiply divide avatar usersinfo numgame rps riddle pun google youtube"
            ,inline=False)
        await ctx.send(author.mention, embed=embed)

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                            description=syntax(command),
                            colour=ctx.author.colour)
        embed.add_field(name="Command description", value=command.description or command.brief)              
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
         #Shows this message
        if (command := get(self.client.commands, name=cmd)):
            await self.cmd_help(ctx, command)

        else:
            await ctx.send("That command does not exist.")

def setup(client):
    client.add_cog(HelpCommands(client))
