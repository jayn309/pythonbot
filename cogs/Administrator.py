import discord
import time
import datetime
import asyncio
import re
import typing

from discord.ext import commands 
from discord.ext.commands import Greedy
from discord.utils import get
from datetime import timedelta
from discord import Member, Embed, DMChannel
from asyncio import sleep
from psutil import Process, virtual_memory
from time import time


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict= {'h': 3600, 's': 1, 'm': 60 , 'd' : 86400}

class TimeConverter(commands.Converter):
	async def convert(self,ctx, argument):
		args = argument.lower()
		matches = re.findall(time_regex, args)
		time = 0
		for key, value in matches:
			try: 
				time += time_dict[value] *float(key)
			except KeyError:
				raise commands.BadArgument(f'{value} is an invalid time key! h|m|s|d are valid arguments.')
			except ValueError:
				raise commands.BadArgument(f'{key} is not a number!')
		return time

class Administrator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief='ban a member')
	@commands.has_guild_permissions(ban_members=True, kick_members=True)
	@commands.guild_only()
	async def ban(self, ctx, member : discord.Member, *, reason: typing.Optional[str]):
		channel = discord.utils.get(member.guild.text_channels, name='mod-log')
		try:
			await member.ban(reason=reason)
			await ctx.send(f"{member.mention} got ban")
			if channel:
				ban_embed = discord.Embed(title='Moderation Ban',colour=member.color,timestamp=datetime.datetime.utcnow())
				ban_embed.add_field(name="Punished by", value=ctx.author,inline=False)
				ban_embed.add_field(name="Punished User", value=member.name,inline=False)
				ban_embed.add_field(name="Reason", value=reason,inline=False)
				ban_embed.set_thumbnail(url=member.avatar_url)
				ban_embed.set_author(name=member.name, icon_url=member.avatar_url)
				ban_embed.set_footer(text=f"Member ID:{member.id}")
				await channel.send(embed=ban_embed)
		except discord.Forbidden:
			return await ctx.send(f"{ctx.author.mention} got ban")
		
	@ban.error
	async def ban_error(self,ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send(f"{ctx.author.mention} got ban")

	@commands.command(brief='unban a member')
	@commands.has_guild_permissions(ban_members=True, kick_members=True)
	@commands.guild_only()
	async def unban(self,ctx, member, *, reason: typing.Optional[str]):
		member = await self.bot.fetch_user(int(member))
		await ctx.guild.unban(member, reason=reason)
		await ctx.send(f'Unbanned the user.')
		channel = self.bot.get_channel(706728600874909712)
		if channel:
				unban_embed = discord.Embed(title='Moderation Unban',colour=member.color,timestamp=datetime.datetime.utcnow())
				unban_embed.add_field(name="Unbanned by", value=ctx.author,inline=False)
				unban_embed.add_field(name="User", value=member.name,inline=False)
				unban_embed.add_field(name="Reason", value=reason,inline=False)
				unban_embed.set_thumbnail(url=member.avatar_url)
				unban_embed.set_author(name=member.name, icon_url=member.avatar_url)
				unban_embed.set_footer(text=f"Member ID:{member.id}")
				await channel.send(embed=unban_embed)


	@commands.command(brief='kick a member')
	@commands.has_guild_permissions(ban_members=True, kick_members=True)
	@commands.guild_only()
	async def kick(self,ctx, member : discord.Member, *,reason: typing.Optional[str]):
		channel = discord.utils.get(member.guild.text_channels, name='mod-log')
		try:
			await member.kick(reason=reason)
			await ctx.send(f"{member.mention} got kicked")
			if channel:
				kick_embed = discord.Embed(title='Moderation Kick',colour=member.color,timestamp=datetime.datetime.utcnow())
				kick_embed.add_field(name="Punished by", value=ctx.author,inline=False)
				kick_embed.add_field(name="Punished User", value=member.name,inline=False)
				kick_embed.add_field(name="Reason", value=reason,inline=False)
				kick_embed.set_thumbnail(url=member.avatar_url)
				kick_embed.set_author(name=member.name, icon_url=member.avatar_url)
				kick_embed.set_footer(text=f"Member ID:{member.id}")
				await channel.send(embed=kick_embed)
		except discord.Forbidden:
			return await ctx.send(f"{ctx.author.mention} got kicked")
	@kick.error
	async def kick_error(self,ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send(f"{ctx.author.mention} got kicked")

	async def mute_member(self, message, member, time, reason):
		role = discord.utils.get(message.guild.roles, name="Muted")
		privaterole = discord.utils.get(message.guild.roles, name="betunamluv")
		privaterole1 = discord.utils.get(message.guild.roles, name="Indomie")
		channel = discord.utils.get(member.guild.text_channels, name='mod-log')
		channel1 = message.channel
		if not role: # checks if there is muted role
			try: # creates muted role 
				muted = await message.guild.create_role(name="Muted", reason="To use for muting")
				for channel in message.guild.channels: # removes permission to view and send in the channels 
					await channel.set_permissions(muted, send_messages=False,
													read_message_history=True,
													read_messages=True)
			except discord.Forbidden:
				return await channel1.send("I have no permissions to make a muted role") # self-explainatory
			await member.add_roles(muted) # adds newly created muted role
			if privaterole:
				await member.remove_roles(privaterole)
			if privaterole1:
				await member.remove_roles(privaterole1)
		else:
			await member.add_roles(role)
			if privaterole:
				await member.remove_roles(privaterole)
			if privaterole1:
				await member.remove_roles(privaterole1)
						
		if channel:
				mute_embed = discord.Embed(title='Moderation Mute',colour=member.color,timestamp=datetime.datetime.utcnow())
				mute_embed.add_field(name="Punished by", value=message.author,inline=False)
				mute_embed.add_field(name="Punished User", value=member.name,inline=False)
				mute_embed.add_field(name="Reason", value=reason,inline=False)
				mute_embed.add_field(name="Duration", value=time,inline=False)
				mute_embed.set_thumbnail(url=member.avatar_url)
				mute_embed.set_author(name=member.name, icon_url=member.avatar_url)
				mute_embed.set_footer(text=f"Member ID:{member.id}")
				await channel.send(embed=mute_embed)
		else:
			pass

		if time:
			await asyncio.sleep(time)

			if role in member.roles:
				await member.remove_roles(role)

			if channel:
				unmute_embed = discord.Embed(title='Moderation Unmute',colour=member.color,timestamp=datetime.datetime.utcnow())
				unmute_embed.add_field(name="Unmuted by", value=message.author,inline=False)
				unmute_embed.add_field(name="User", value=member.name,inline=False)
				unmute_embed.add_field(name="Reason", value=reason,inline=False)
				unmute_embed.set_thumbnail(url=member.avatar_url)
				unmute_embed.set_author(name=member.name, icon_url=member.avatar_url)
				unmute_embed.set_footer(text=f"Member ID:{member.id}")
				await channel.send(embed=unmute_embed)
			else:
				return
		
	@commands.command(brief='mute a member')
	@commands.has_guild_permissions(ban_members=True, kick_members=True)
	@commands.guild_only()
	async def mute(self,ctx, member : discord.Member,time:TimeConverter=None,*,reason: typing.Optional[str]):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if role in member.roles:
			await ctx.send(f"{member.mention} is already muted.")
		else:
			await self.mute_member(ctx.message, member,time,reason)
			await ctx.send(f"{member.mention} was muted for {time}s." if time else f"{member.mention} was muted.")
			if time:
				await asyncio.sleep(time)
				await ctx.send(f"{member.mention} was unmuted")

	async def mute_error(self,ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send(f"{ctx.author.mention} was muted")

	async def unmute_member(self, message, member,reason):
		role = discord.utils.get(message.guild.roles, name="Muted")
		channel = discord.utils.get(member.guild.text_channels, name='mod-log')
		await member.remove_roles(role)   
		if channel:
				unmute_embed = discord.Embed(title='Moderation Unmute',colour=member.color,timestamp=datetime.datetime.utcnow())
				unmute_embed.add_field(name="Unmuted by", value=message.author,inline=False)
				unmute_embed.add_field(name="User", value=member.name,inline=False)
				unmute_embed.add_field(name="Reason", value=reason,inline=False)
				unmute_embed.set_thumbnail(url=member.avatar_url)
				unmute_embed.set_author(name=member.name, icon_url=member.avatar_url)
				unmute_embed.set_footer(text=f"Member ID:{member.id}")
				await channel.send(embed=unmute_embed)
		else:
			return

	@commands.command(brief='unmute a member',description='Unmute a member.')
	@commands.has_guild_permissions(ban_members=True, kick_members=True)
	@commands.guild_only()
	async def unmute(self,ctx, member : discord.Member,reason: typing.Optional[str]):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if role not in member.roles:
			await ctx.send(f"{member.mention} is not muted.")
		else:
			await self.unmute_member(ctx.message, member,reason)
			await ctx.send(f"{member.mention} was unmuted")

		
	@unmute.error
	async def unmute_error(self,ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send(f"{ctx.author.mention} was unmuted")

	@commands.command(brief = 'clear an amount of messages (of members if mentioned)',description='mention members to delete their messages\ncount messages from others also, but the bot will only delete messages from mentioned member\ncount up to the message you want to delete')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def purge(self,ctx, members: Greedy[Member], number:int=None):
		def _check(message):
			return not len(members) or message.author in members
		if number is None:
			await ctx.send('You must input a number')
		else:
			await ctx.message.delete()
			deleted = await ctx.channel.purge(limit=number,check=_check)
			await ctx.send(f'Deleted {len(deleted):,} messages.', delete_after=5)

	@commands.command(brief='make the bot say something in a channel',description='_say #channel message')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def say(self, ctx, channel, *, msg):
		channel_mentions = ctx.message.channel_mentions
		channel = discord.utils.get(channel_mentions, mention=channel)
		await ctx.message.delete()
		await channel.send(format(msg))

	@commands.command(brief='edit a bot message in a channel',description='_edit #channel message_id content')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def edit(self,ctx,channel,message_id, *,content):
		try:
			channel_mentions = ctx.message.channel_mentions
			channel = discord.utils.get(channel_mentions, mention=channel)
			message = await channel.fetch_message(message_id)
			await message.edit(content=content)
		except discord.NotFound as e:
			await ctx.send("Could not find that message")
			raise e

	@commands.command(brief='remove a role from a member',description='_removerole rolename @member')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def removerole(self,ctx,role: discord.Role, *, member : discord.Member):
		await member.remove_roles(role)
		await ctx.send(f"Remove role from {member.mention}")

	@commands.command(brief='add a role to a member',description='_addrole rolename @member')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def addrole(self,ctx,role: discord.Role, *, member : discord.Member):
		await member.add_roles(role)
		await ctx.send(f"Add role to {member.mention}")

	@commands.command(aliases=['aar'],brief='add a role to all members (Admin only)',description='_aar rolename')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
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

	@commands.command(aliases=['arr'],brief='remove a role from all members',description='_arr rolename')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
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

	@commands.command(brief='number of members have that role',description='_countr rolename')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def countr(self,ctx, *,role: discord.Role):
		def ccheck(m):
			try:
				return int(m.content) and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
			except ValueError:
				return False
		counter = 0
		for member in ctx.guild.members:
			if role in member.roles:
				counter =len(role.members)
		await ctx.send(f'{counter} members have {role} role.')
		if counter != 0:
			await ctx.send('Do you want a list of those members? If yes type 1, if no just go.')
			try:
				msg_countr = await self.bot.wait_for('message',timeout=10.0,check=ccheck)
				if msg_countr.content == '1':
					await ctx.send("This will take awhile.")
					while counter != 0:
						for member in ctx.guild.members:
							if role in member.roles:
								await ctx.send(f'{member.name}#{member.discriminator} - ID: {member.id}')
								counter -= 1
					else:
						counter == 0
						await ctx.send('Done.')
			except asyncio.TimeoutError:
				await ctx.send("Less work for me then.")

	@commands.command(brief='move member to another voice chat or disconnect from voicechat',description='Mention voice chat channel by <#channelID>. \n _move @members without channel will disconnect members from vchat.\n _move #channel without members will move everyone to another voice chat channel.')
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
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
	
	@commands.command(aliases=[ 'slm'],brief='set slowmode for channel', description='Slowmode by number of seconds for a channel. \n Put 0  to disable slowmode.') 
	@commands.guild_only()
	async def slowmode(self,ctx,channel:discord.TextChannel,seconds:int):
		if seconds is None:
			await ctx.send("Please put a number or 0 to disable")
		else:
			await channel.edit(slowmode_delay=seconds)

	@commands.command(aliases=['lm'],brief='set limit for number of users in a voice chat channel',description='Limit the number of users in a voice chat channel. \n Put 0  to set no limit. \n Mention channel by <#channelID>.')
	@commands.guild_only()
	async def limit(self,ctx,channel:discord.VoiceChannel,numbers:int):
		if numbers is None:
			await ctx.send("Please put a number of users or 0 to set no limit")
		else:
			await channel.edit(user_limit=numbers)
		
	@commands.Cog.listener()
	async def on_message(self, message):
		modlog_channel = self.bot.get_channel(731357775652847686)
		if not modlog_channel:
			print("Mail channel not found! Reconfigure bot!")
		if not message.author.id == 685307035142586380:
			if isinstance(message.channel, DMChannel):
				guild = self.bot.get_guild(626016069873696791)
				member = guild.get_member(message.author.id)
				member_role = guild.get_role(687823988831027203)
				muted_member = guild.get_role(690770300002107442)
				if muted_member in member.roles:
					await message.channel.send("Muted members cannot use modmail.")
				else:
					if member_role in member.roles and not muted_member in member.roles:
						if len(message.content) < 50 and not message.content[0]=="_":
							await message.channel.send("Your message should be at least 50 characters in length.")
						elif message.content[0]=="_":
							await message.channel.send("Get lost!")
						else:
							embed = Embed(title="Modmail",
											colour=member.colour,
											timestamp=datetime.datetime.utcnow())
							embed.set_thumbnail(url=member.avatar_url)
							embed.add_field(name="Member",value= member.display_name,inline= False)
							embed.add_field(name="Message",value= message.content, inline=False)    
							if message.attachments:
								embed.add_field(name="Attachments", value=", ".join([i.url for i in message.attachments])) 
							await modlog_channel.send(embed=embed)
							await message.channel.send("Message relayed to moderators.")
					else:
							await message.channel.send("Only members can use modmail.")
			else:
				pass

		def _check(m):
			return (m.author == message.author
					and len(m.mentions)
					and (datetime.datetime.utcnow()-m.created_at).seconds < 10)

		if not message.author.bot:
			if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:
				await message.channel.send("Don't spam mentions!", delete_after=10)
				unmutes = await self.mute_member(message, message.author, 60, reason="Mention spam")

				if unmutes:
					await sleep(60)
					await self.unmute_member(message.guild, message.author, reason="Mute time expired") 

	@commands.command(name="stats",brief="show bot stats")
	async def show_bot_stats(self, ctx):
		embed = Embed(title="Bot stats",
					  colour=ctx.author.colour,
					  thumbnail=self.bot.user.avatar_url,
					  timestamp=datetime.datetime.utcnow())

		proc = Process()
		with proc.oneshot():
			uptime = timedelta(seconds=time()-proc.create_time())
			mem_total = virtual_memory().total / (1024**2)
			mem_of_total = proc.memory_percent()
			mem_usage = mem_total * (mem_of_total / 100)

		channels = map(lambda m: len(m.channels), self.bot.guilds)

		fields = [
			("Uptime", uptime, True),
			("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
			("__*Discord Stats*__",
			 "All Guilds: {}"
			 "\nAll Channels: {}"
			 "\nAll Emojis: {}"
			 "\nAll Commands: {}"
			 "\nAll Users: {:,}".format(len(self.bot.guilds), sum(list(channels)), len(self.bot.emojis),
									len(self.bot.commands),
									len(self.bot.users)), True),
		]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)   

	@commands.command(name="prefix",aliases=["changeprefix", "setprefix"],description="Change your guilds prefix!",usage="[prefix]")
	@commands.has_guild_permissions(manage_guild=True)
	async def prefix(self, ctx, *, prefix="_"):
		await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
		await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")

	@commands.command(
	name='deleteprefix',
	aliases=['dp'],
	description="Delete your guilds prefix!"
	)
	@commands.guild_only()
	@commands.has_guild_permissions(administrator=True)
	async def deleteprefix(self, ctx):
		await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
		await ctx.send("This guilds prefix has been set back to the default")

def setup(bot):
	bot.add_cog(Administrator(bot))