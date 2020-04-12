import discord
import time
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} got ban")
        except discord.Forbidden:
            return await ctx.send(f"{ctx.author.mention} got ban")
    @ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} got ban")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned the user.')
                return

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def kick(self,ctx, member : discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} got kicked")
        except discord.Forbidden:
            return await ctx.send(f"{ctx.author.mention} got kicked")
    @kick.error
    async def kick_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} got kicked")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def mute(self,ctx, member : discord.Member,*, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role: # checks if there is muted role
            try: # creates muted role 
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                    await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=True,
                                              read_messages=True)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role") # self-explainatory
            await member.add_roles(muted) # adds newly created muted role
            
        else:
            await member.add_roles(role)
        await ctx.send(f"{member.mention} was muted")
    @mute.error
    async def mute_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} was muted")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def unmute(self,ctx, member : discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} was unmuted")
    @unmute.error
    async def unmute_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} was unmuted")

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def purge(self,ctx, number:int=None ):
        if number is None:
            await ctx.send('You must input a number')
        else:
            await ctx.message.channel.purge(limit=number)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel, *, msg):
        channel_mentions = ctx.message.channel_mentions
        channel = discord.utils.get(channel_mentions, mention=channel)
        await ctx.message.delete()
        await channel.send(format(msg))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def edit(self,ctx,channel,message_id, *,content):
        try:
            channel_mentions = ctx.message.channel_mentions
            channel = discord.utils.get(channel_mentions, mention=channel)
            message = await channel.fetch_message(message_id)
            await message.edit(content=content)
        except discord.NotFound as e:
            await ctx.send("Could not find that message")
            raise e

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def role(self,ctx, role: discord.Role, user: discord.Member):
        if role is None and user is None:
            return await ctx.send("You haven't specified a role or a user! ")

        if role not in ctx.message.guild.roles or user not in ctx.message.guild.members:
            return await ctx.send("That role or user doesn't exist.")

        if  user != None and role not in user.roles:
            await user.add_roles(user, role)
            return await ctx.send(f"{role} role has been added to {user}.")

        if  user != None and role in user.roles:
            await user.remove_roles(user, role)
            return await ctx.send(f"{role} role has been removed from {user}.")

def setup(client):
    client.add_cog(Administrator(client))