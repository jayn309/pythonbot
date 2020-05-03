import discord
import time
import datetime

from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        channel = discord.utils.get(member.guild.text_channels, name='log')
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} got ban")
            if channel:
                ban_embed = discord.Embed(title='Moderation Ban',colour=member.color)
                ban_embed.add_field(name="Punished by", value=ctx.author,inline=False)
                ban_embed.add_field(name="Punished User", value=member.name,inline=False)
                ban_embed.set_thumbnail(url=member.avatar_url)
                ban_embed.set_author(name=member.name, icon_url=member.avatar_url)
                ban_embed.set_footer(text=f"Member ID:{member.id}")
                ban_embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=ban_embed)
        except discord.Forbidden:
            return await ctx.send(f"{ctx.author.mention} got ban")
        
    @ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} got ban")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def unban(self,ctx, member, *, reason=None):
        member = await self.client.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f'Unbanned the user.')
        channel = discord.utils.get(member.guild.text_channels, name='log')
        if channel:
                unban_embed = discord.Embed(title='Moderation Unban',colour=member.color)
                unban_embed.add_field(name="Unbanned by", value=ctx.author,inline=False)
                unban_embed.add_field(name="User", value=member.name,inline=False)
                unban_embed.set_thumbnail(url=member.avatar_url)
                unban_embed.set_author(name=member.name, icon_url=member.avatar_url)
                unban_embed.set_footer(text=f"Member ID:{member.id}")
                unban_embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=unban_embed)


    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def kick(self,ctx, member : discord.Member, *, reason=None):
        channel = discord.utils.get(member.guild.text_channels, name='log')
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} got kicked")
            if channel:
                kick_embed = discord.Embed(title='Moderation Kick',colour=member.color)
                kick_embed.add_field(name="Punished by", value=ctx.author,inline=False)
                kick_embed.add_field(name="Punished User", value=member.name,inline=False)
                kick_embed.set_thumbnail(url=member.avatar_url)
                kick_embed.set_author(name=member.name, icon_url=member.avatar_url)
                kick_embed.set_footer(text=f"Member ID:{member.id}")
                kick_embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=kick_embed)
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
        privaterole = discord.utils.get(ctx.guild.roles, name="betunamluv")
        privaterole1 = discord.utils.get(ctx.guild.roles, name="Test Subject")
        privaterole2 = discord.utils.get(ctx.guild.roles, name="Solitary Confinement")
        channel = discord.utils.get(member.guild.text_channels, name='log')
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
            if privaterole:
                await member.remove_roles(privaterole)
            if privaterole1:
                await member.remove_roles(privaterole1)
            if privaterole2:
                await member.remove_roles(privaterole2)
        else:
            await member.add_roles(role)
            if privaterole:
                await member.remove_roles(privaterole)
            if privaterole1:
                await member.remove_roles(privaterole1)
            if privaterole2:
                await member.remove_roles(privaterole2)
                
        await ctx.send(f"{member.mention} was muted")
        if channel:
                mute_embed = discord.Embed(title='Moderation Mute',colour=member.color)
                mute_embed.add_field(name="Punished by", value=ctx.author,inline=False)
                mute_embed.add_field(name="Punished User", value=member.name,inline=False)
                mute_embed.set_thumbnail(url=member.avatar_url)
                mute_embed.set_author(name=member.name, icon_url=member.avatar_url)
                mute_embed.set_footer(text=f"Member ID:{member.id}")
                mute_embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=mute_embed)
    @mute.error
    async def mute_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} was muted")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def unmute(self,ctx, member : discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        channel = discord.utils.get(member.guild.text_channels, name='log')
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} was unmuted")
        if channel:
                unmute_embed = discord.Embed(title='Moderation Unmute',colour=member.color)
                unmute_embed.add_field(name="Unmuted by", value=ctx.author,inline=False)
                unmute_embed.add_field(name="User", value=member.name,inline=False)
                unmute_embed.set_thumbnail(url=member.avatar_url)
                unmute_embed.set_author(name=member.name, icon_url=member.avatar_url)
                unmute_embed.set_footer(text=f"Member ID:{member.id}")
                unmute_embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=unmute_embed)
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
    async def removerole(self,ctx,user: discord.Member,*role: discord.Role):
        await user.remove_roles(*role)
        await ctx.send(f"Remove role from {user.mention}")

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def addrole(self,ctx,user: discord.Member,*role: discord.Role):
        await user.add_roles(*role)
        await ctx.send(f"Add role to {user.mention}")


def setup(client):
    client.add_cog(Administrator(client))