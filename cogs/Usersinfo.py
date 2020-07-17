import discord
import datetime
from discord.ext import commands

class usersinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[ 'ui'],brief='get info of a user')
    async def usersinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
    
        roles = [role for role in member.roles]
    
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)
    
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)
    
        embed.add_field(name="Bot?", value=member.bot)
    
        await ctx.send(embed=embed)

    @commands.command(aliases=[ 'pfp'],brief='get avatar of a user or yours')
    @commands.guild_only()
    async def avatar(self, ctx, *, member: discord.Member = None):
        """ Get the avatar of you or someone else """
        member = member or ctx.author
        await ctx.send(f"Avatar of {member.display_name}")

def setup(client):
    client.add_cog(usersinfo(client))
