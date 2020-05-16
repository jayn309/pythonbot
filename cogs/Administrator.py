import discord
import time
import datetime
import asyncio

from discord.ext import commands
from discord.utils import get


class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        channel = discord.utils.get(member.guild.text_channels, name='mod-log')
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
        channel = self.client.get_channel(706728600874909712)
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
        channel = discord.utils.get(member.guild.text_channels, name='mod-log')
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
        channel = discord.utils.get(member.guild.text_channels, name='mod-log')
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
        privaterole = discord.utils.get(ctx.guild.roles, name="betunamluv")
        privaterole1 = discord.utils.get(ctx.guild.roles, name="Test Subject")
        privaterole2 = discord.utils.get(ctx.guild.roles, name="Solitary Confinement")
        privaterole3 = discord.utils.get(ctx.guild.roles, name="YadongYaseol")
        channel = discord.utils.get(member.guild.text_channels, name='mod-log')
        privaterole_channel = discord.utils.get(member.guild.text_channels, name='bot-config')
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

        await privaterole_channel.send("Does this member need roles for private channels? If yes how many? If none type 0")
        def check(m):
                try:
                    return m.channel.id == 680233386648141860
                except ValueError:
                    return False
        msg = await self.client.wait_for('message',check=check)
        number_of_roles = int(msg.content)
        if number_of_roles != 0:
            await privaterole_channel.send("Please type the roles name below.")
            while number_of_roles != 0:
                msg_channel_name = await self.client.wait_for('message',check=check)
                if msg_channel_name.content.lower () == 'betunamluv':
                    await member.add_roles(privaterole)
                    number_of_roles -= 1
                    await privaterole_channel.send("Role was added to this member. Type next role below or leave me alone if you're done.")
                if msg_channel_name.content.lower () == 'test':
                    await member.add_roles(privaterole1)
                    number_of_roles -= 1
                    await privaterole_channel.send("Role was added to this member. Type next role below or leave me alone if you're done.")
                if msg_channel_name.content.lower () == 'yadongyaseol' or msg_channel_name.content.lower () == 'yy':
                    await member.add_roles(privaterole3)
                    number_of_roles -= 1
                    await privaterole_channel.send("Role was added to this member. Type next role below or leave me alone if you're done.")
                if msg_channel_name.content.lower () == 'solitary' or msg_channel_name.content.lower () == 'sc':
                    await member.add_roles(privaterole2)
                    number_of_roles -= 1
                    await privaterole_channel.send("Role was added to this member. Type next role below or leave me alone if you're done." )
                if number_of_roles == 0:
                    await privaterole_channel.send("All roles are added.")
                    break
        else:
            await privaterole_channel.send("No private role need to be added to this member")

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
    async def removerole(self,ctx,role: discord.Role, *, member : discord.Member):
        await member.remove_roles(role)
        await ctx.send(f"Remove role from {member.mention}")

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def addrole(self,ctx,role: discord.Role, *, member : discord.Member):
        await member.add_roles(role)
        await ctx.send(f"Add role to {member.mention}")

    @commands.command(aliases=['aar'])
    @commands.has_guild_permissions(administrator=True)
    async def alladdrole(self,ctx, *,role: discord.Role):
        num_members = len(ctx.guild.members)
        await ctx.send("This will take awhile.")
        while num_members != 0:
            for member in ctx.guild.members:
                await member.add_roles(role)
                num_members -= 1
        else:
            num_members == 0
            await ctx.send(f"Added role to all members.")

    @commands.command(aliases=['arr'])
    @commands.has_guild_permissions(administrator=True)
    async def allremoverole(self,ctx, *,role: discord.Role):
        num_members = len(role.members)
        await ctx.send("This will take awhile.")
        while num_members != 0:
            for member in ctx.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
                    num_members -= 1
        else:
            num_members == 0
            await ctx.send(f"Remove role from all members.")

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def countr(self,ctx, *,role: discord.Role):
        counter = 0
        for member in ctx.guild.members:
            if role in member.roles:
                counter =len(role.members)
        await ctx.send(f'{counter} members have {role} role.')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def move(self,ctx,members: commands.Greedy[discord.Member] = None, channel: discord.VoiceChannel = None):
        if ctx.author.voice:
            members = members or ctx.author.voice.channel.members
        else:
            if members is None:
                return await ctx.send('Please specify users or join a voice channel')
        total = len(members)
        success = 0
        for member in members:
            try:
                await member.move_to(channel)
            except discord.HTTPException as e:
                await ctx.send(f'Unable to move {member} - `{e}`', delete_after=7)
            else:
                success += 1
                await ctx.message.add_reaction('\U00002705')  # React with checkmark
        await ctx.send(f'Moved {success}/{total} users', delete_after=10)


def setup(client):
    client.add_cog(Administrator(client))