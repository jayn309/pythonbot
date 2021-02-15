import datetime
import discord

from random import choice
from discord.ext import commands
from discord.utils import get
from typing import Any, List, Union, Optional

class Log(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
			
	@commands.Cog.listener()
	async def on_member_join(self, member):
		guild = self.bot.get_guild(626016069873696791)
		channel = self.bot.get_channel(706728600874909712)
		welcome_channel = self.bot.get_channel(626016070624346113)
		if guild:
			if channel:
				embed = discord.Embed(description=f'{len(member.guild.members)}th member joined', 
									colour=member.color,timestamp=datetime.datetime.utcnow())
				embed.set_thumbnail(url=member.avatar_url)
				embed.set_author(name=member.name, icon_url=member.avatar_url)
				embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
				await channel.send(embed=embed)
			if welcome_channel:
				await welcome_channel.send(f'Welcome to WenRene Discord, {member.mention}! Pick a role tag in <#681672202822877207>. Enjoy your stay!')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel =  self.bot.get_channel(706728600874909712)
		if channel:
			embed = discord.Embed(description='Goodbye', colour=member.color,timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_author(name=member.name, icon_url=member.avatar_url)
			embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
			await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_user_update(self,before,after):
		log_channel = self.bot.get_channel(700137514572185662)
		if before.name != after.name:
			embed = discord.Embed(title="Username change",
							colour=after.colour,
							timestamp=datetime.datetime.utcnow())

			embed.set_author(name=f'{before.name}#{before.discriminator}', icon_url=before.avatar_url)
			embed.set_footer(text=f"Author ID:{before.id}")

			fields = [("Before", before.name, False),
						("After", after.name, False)]

			for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				
			await log_channel.send(embed=embed)

		if before.discriminator != after.discriminator:
			embed = discord.Embed(title="Discriminator change",
							colour=after.colour,
							timestamp=datetime.datetime.utcnow())

			embed.set_author(name=f'{before.name}#{before.discriminator}', icon_url=before.avatar_url)
			embed.set_footer(text=f"Author ID:{before.id}")

			fields = [("Before", before.discriminator, False),
						("After", after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await log_channel.send(embed=embed)

		if before.avatar_url != after.avatar_url:
			embed = discord.Embed(title="Avatar change",
							description="New image is below, old to the right.",
							colour=after.colour,
							timestamp=datetime.datetime.utcnow())

			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)
			embed.set_author(name=f'{before.name}#{before.discriminator}', icon_url=before.avatar_url)
			embed.set_footer(text=f"Author ID:{before.id}")

			await log_channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		log_channel = self.bot.get_channel(700137514572185662)
		rolelog_channel = self.bot.get_channel(700120282140246026)
		if before.guild.id != 626016069873696791:
			return
		else:    
			if before.display_name != after.display_name:
				embed = discord.Embed(title="Nickname change",
								colour=after.colour,
								timestamp=datetime.datetime.utcnow())

				embed.set_author(name=f'{before.name}#{before.discriminator}', icon_url=before.avatar_url)
				embed.set_footer(text=f"Author ID:{before.id}")
				fields = [("Before", before.display_name, False),
							("After", after.display_name, False)]

				for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)

				await log_channel.send(embed=embed)

			elif before.roles != after.roles:
				embed = discord.Embed(title="Role updates",
								colour=after.colour,
								timestamp=datetime.datetime.utcnow())

				embed.set_author(name=f'{before.name}#{before.discriminator}', icon_url=before.avatar_url)
				embed.set_footer(text=f"Author ID:{before.id}")      

				fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
							("After", ", ".join([r.mention for r in after.roles]), False)]

				for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
				await rolelog_channel.send(embed=embed)
			else:
				return

	@commands.Cog.listener()
	async def on_message_edit(self, before,after):
		try:
			if before.author.id == 685307035142586380 or before.author.id == 325387620266016768 or before.author.id == 234395307759108106 or before.author.id == 235088799074484224 or before.author.id == 172002275412279296 or before.author.id == 359401025330741248 or before.author.id == 408785106942164992:
				return
			if before.content == after.content:
				return
			else:
				edit_embed = discord.Embed(title="Message edited",description=f'{before.author.name} edited a message in {before.channel.mention}', 
												colour = before.author.colour,
												timestamp=datetime.datetime.utcnow())
				edit_embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.avatar_url)
				edit_embed.set_footer(text=f"Author ID:{before.author.id} • Message ID: {before.id}")
				edit_embed.add_field(name='Before:', value=before.content, inline=False)
				edit_embed.add_field(name="After:", value=after.content, inline=False)
				for channel in before.guild.channels:
					if channel.id == 684130494023073865:
						await channel.send(embed=edit_embed)
		except AttributeError:
			return

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.guild.id  != 626016069873696791:
			return
		if not message.author.id == 685307035142586380:
			delete_embed = discord.Embed(title="Message deleted", description=f"Action by {message.author.name} in {message.channel.mention}.",
							colour = message.author.colour, 
							timestamp=datetime.datetime.utcnow())
			delete_embed.set_footer(text=f"Author ID:{message.author.id} • Message ID: {message.id}")
			delete_embed.set_author(name=f'{message.author.name}#{message.author.discriminator}', icon_url=message.author.avatar_url)
			fields = [("Content",message.content, False)]
			for name, value, inline in fields:
				delete_embed.add_field(name=name, value=value,inline=inline)
			for channel in message.guild.channels:
					if channel.id == 684130494023073865:
						await channel.send(embed=delete_embed)

	@commands.Cog.listener()
	async def on_bulk_message_delete(self, messages):
		for message in messages:
			if message.guild.id  != 626016069873696791:
				return
			if not message.author.id == 685307035142586380:
				delete_embed = discord.Embed(title="Message deleted", description=f"Action by {message.author.name} in {message.channel.mention}.",
								colour = message.author.colour, 
								timestamp=datetime.datetime.utcnow())
				delete_embed.set_footer(text=f"Author ID:{message.author.id} • Message ID: {message.id}")
				delete_embed.set_author(name=f'{message.author.name}#{message.author.discriminator}', icon_url= message.author.avatar_url)
				fields = [("Content",message.content, False)]
				for name, value, inline in fields:
					delete_embed.add_field(name=name, value=value,inline=inline)
				for channel in message.guild.channels:
					if channel.id == 684130494023073865:
						await channel.send(embed=delete_embed)
		

def setup(bot):
	bot.add_cog(Log(bot))