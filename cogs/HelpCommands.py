import discord
from discord.ext import commands

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

def setup(client):
    client.add_cog(HelpCommands(client))
