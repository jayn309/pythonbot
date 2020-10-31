import discord
import DiscordUtils
import datetime

from discord.ext import commands

class Invites(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.tracker = DiscordUtils.InviteTracker(bot)

@commands.Cog.listener()
async def on_ready(self):
	await self.tracker.cache_invites()

@commands.Cog.listener()
async def on_invite_create(self,invite):
	await self.tracker.update_invite_cache(invite)

@commands.Cog.listener()
async def on_guild_join(self,guild):
	await self.tracker.update_guild_cache(guild)

@commands.Cog.listener()
async def on_invite_delete(self,invite):
	await self.tracker.remove_invite_cache(invite)

@commands.Cog.listener()
async def on_guild_remove(self,guild):
	await self.tracker.remove_guild_cache(guild)

@commands.Cog.listener()
async def on_member_join(self,member):
	guild = self.bot.get_guild(626016069873696791)
	if guild:
		inviter = await self.tracker.fetch_inviter(member) # inviter is the member who invited
		data = await self.bot.invites.find(inviter.id)
		if data is None:
			data = {"_id": inviter.id, "count": 0, "userInvited": []}

		data["count"] +=1
		data["userInvited"].append(member.id)
		await self.bot.invites.upsert(data)

		channel = self.bot.get_channel(731357775652847686)
		if not channel:
			print("Invitation log channel not found! Reconfigure bot!")
		else:
			embed = discord.Embed(title =f'{len(member.guild.members)}th member joined',description=f'Invited by: {inviter.mention}\nInvites: {data["count"]}', 
									colour=member.color,timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_author(name=member.name, icon_url=member.avatar_url)
			embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
			await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Invites(bot))