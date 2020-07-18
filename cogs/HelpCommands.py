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

    @commands.group(name="help", invoke_without_command=True)
    async def helpcommand(self ,ctx):
        await ctx.channel.send("Base help command. Subcommands: Admin, Fun")

    @helpcommand.command(name='Admin', aliases=['admin'])
    async def admin_subcommand(self,ctx):
        author = ctx.message.author

        embed = discord.Embed(description='Here is the list of commands! \n For more info on a specific command, use _help {command}',
                colour = discord.Colour.blurple()
            )

        embed.set_author(name="Administrator commands list", icon_url=self.client.avatar_url)
        embed.add_field(name=r'\U+1F451 Admin', value="kick ban unban mute unmute purge say edit showemotes addrole removerole move alladdrole allremoverole countr"
        ,inline=False)
        await ctx.send(author.mention, embed=embed)

    @helpcommand.command(name='Fun',aliases=['fun'])
    async def fun_subcommand(self,ctx):
        author = ctx.message.author

        embed = discord.Embed(
                colour = discord.Colour.blurple()
            )
        embed.add_field(name="_8ball [question]", value="get random answer",inline=False)
        embed.add_field(name="_coinflip", value="flip a coin",inline=False)
        embed.add_field(name="_f", value="pay your respect",inline=False)
        embed.add_field(name="_choose [choices]", value="choose between choices .Use , between your choices.",inline=False)
        embed.add_field(name="_hug", value="give a hug to a member",inline=False)
        embed.add_field(name="_rate", value="rate something",inline=False)
        embed.add_field(name="_hot", value="how hot someone is",inline=False)
        embed.add_field(name="_slot", value="play slot machine",inline=False)
        embed.add_field(name="_tableflip _unflip", value="flip/unflip a table",inline=False)
        embed.add_field(name="_add _subtract _multiply _divide [2 numbers]", value="do basic maths",inline=False)
        embed.add_field(name="_avatar", value="get avatar of a user",inline=False)
        embed.add_field(name="_usersinfo", value="get info of a user",inline=False)
        embed.add_field(name="_numgame", value="guess a number",inline=False)
        embed.add_field(name="_rps [rock, paper, scissors]", value="play rps",inline=False)
        embed.add_field(name="_riddle", value="guess a word from riddles",inline=False)
        embed.add_field(name="_pun", value="guess a word from puns",inline=False)
        embed.add_field(name="_google", value="google search",inline=False)
        embed.add_field(name="_youtube", value="youtube search",inline=False)


        await ctx.send(author.mention, embed=embed)

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
						description=syntax(command),
						colour=ctx.author.colour)
        embed.add_field(name="Command description", value=command.description or command.brief)              
        await ctx.send(embed=embed)

    @command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows this message."""
        if (command := get(self.client.commands, name=cmd)):
            await self.cmd_help(ctx, command)

        else:
            await ctx.send("That command does not exist.")


def setup(client):
    client.add_cog(HelpCommands(client))
