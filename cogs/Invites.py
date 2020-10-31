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
		print(inviter)
	else:
		pass

def setup(bot):
	bot.add_cog(Invites(bot))