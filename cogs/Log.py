import discord
import datetime
from random import choice
from discord.ext import commands
from discord.utils import get
from typing import Any, List, Union, Optional

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def send_log_message(self,ctx, guild: discord.Guild, content=None, *, embed: discord.Embed = None):
        channel = discord.utils.get(guild.text_channels, name="log")
        try:
            await channel.send(content=content, embed=embed)
            return True
        except discord.HTTPException as e:
            print(e)
        if not channel:
            try:
                overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            guild.me: discord.PermissionOverwrite(read_messages=True)}
                channel = await guild.create_text_channel('log', overwrites=overwrites)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to create a channel")
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(description=f'{len(member.guild.members)}th member joined', color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        self.client.send_log_message(member.guild,embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(description='Goodbye', color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        if self.client.guild_permissions.view_audit_log:
            entry = await self.get_audit_entry(member.guild, discord.AuditLogAction.kick, member)
            if entry:
                embed.description = "Kicked"
                embed.set_footer(text=f"{entry.user.name}#{entry.user.discriminator}",
                                    icon_url=member.avatar_url(entry.user))
                embed.colour = member.color
                if entry.reason:
                    embed.description += f"\n**Reason:** {entry.reason}"
                await self.client.send_log_message(member.guild, embed=embed)
                return
            embed.description = "Left the server"
            await self.client.send_log_message(member.guild, embed=embed)
            return
            # Otherwise, we are not certain
        await self.client.send_log_message(member.guild, embed=embed)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: List[discord.Emoji],
                                     after: List[discord.Emoji]):
        """Called every time an emoji is created, deleted or updated."""
        def emoji_repr(_emoji: discord.Emoji):
            fix = ":" if _emoji.require_colons else ""
            return f"{fix}{_emoji.name}{fix}"
        embed = discord.Embed(colour=discord.Colour.blurple())
        emoji: discord.Emoji = None
        # Emoji deleted
        if len(before) > len(after):
            emoji = discord.utils.find(lambda e: e not in after, before)
            if emoji is None:
                return
            embed.set_author(name=f"{emoji_repr(emoji)} (ID: {emoji.id})", icon_url=emoji.url)
            embed.description = f"Emoji deleted."
            action = discord.AuditLogAction.emoji_delete
        # Emoji added
        elif len(after) > len(before):
            emoji = discord.utils.find(lambda e: e not in before, after)
            if emoji is None:
                return
            embed.set_author(name=f"{emoji_repr(emoji)} (ID: {emoji.id})", icon_url=emoji.url)
            embed.description = f"Emoji added."
            action = discord.AuditLogAction.emoji_create
        else:
            old_name = ""
            for new_emoji in after:
                for old_emoji in before:
                    if new_emoji == old_emoji and new_emoji.name != old_emoji.name:
                        old_name = old_emoji.name
                        emoji = new_emoji
                        break
            if emoji is None:
                return
            embed.set_author(name=f"{emoji_repr(emoji)} (ID: {emoji.id})", icon_url=emoji.url)
            embed.description = f"Emoji renamed from `{old_name}` to `{emoji.name}`"
            action = discord.AuditLogAction.emoji_update
        if emoji:
            entry = await self.get_audit_entry(guild, action, emoji)
            if entry:
                embed.set_footer(text="{0.name}#{0.discriminator}".format(entry.user))
            await self.client.send_log_message(guild, embed=embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        def get_region_string(region: discord.VoiceRegion) -> str:
            """Returns a formatted string for a given :class:`VoiceRegion`
            :param region: The voice region to convert.
            :return: The string representing the region."""
            regions = {"us-west": "🇺🇸US West",
                    "us-east": "🇺🇸US East",
                    "us-central": "🇺🇸US Central",
                    "us-south": "🇺🇸US South",
                    "eu-west": "🇪🇺West Europe",
                    "eu-central": "🇪🇺Central Europe",
                    "singapore": "🇸🇬Singapore",
                    "london": "🇬🇧London",
                    "sydney": "🇦🇺Sydney",
                    "amsterdam": "🇳🇱Amsterdam",
                    "frankfurt": "🇩🇪Frankfurt",
                    "brazil": "🇧🇷Brazil",
                    "japan": "🇯🇵Japan",
                    "hongkong": "🇭🇰Hong Kong",
                    "russia": "🇷🇺Russia",
                    "vip-us-east": "🇺🇸US East (VIP)",
                    "vip-us-west": "🇺🇸US West (VIP)",
                    "vip-amsterdam": "🇳🇱Amsterdam (VIP)",
                    }
            return regions.get(str(region), str(region))

        def get_user_avatar(user: Union[discord.User, discord.Member]) -> str:
            """Gets the user's avatar url
            If they don't have an avatar set, the default avatar is returned.
            :param user: The user to get the avatar of
            :return: The avatar's url."""
            return user.avatar_url if user.avatar_url is not None else user.default_avatar_url

        """Called every time a guild is updated"""
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=after.name, icon_url=after.icon_url)

        changes = True
        if before.name != after.name:
            embed.description = f"Name changed from **{before.name}** to **{after.name}**"
        elif before.region != after.region:
            embed.description = "Region changed from **{0}** to **{1}**".format(get_region_string(before.region),
                                                                                get_region_string(after.region))
        elif before.icon_url != after.icon_url:
            embed.description = "Icon changed"
            embed.set_thumbnail(url=after.icon_url)
        elif before.owner_id != after.owner_id:
            embed.description = f"Ownership transferred to {after.owner.mention}"
        else:
            changes = False
        if changes:
            entry = await self.get_audit_entry(after, discord.AuditLogAction.guild_update)
            if entry:
                icon_url = get_user_avatar(entry.user)
                embed.set_footer(text=f"{entry.user.name}#{entry.user.discriminator}", icon_url=icon_url)
            await self.client.send_log_message(after, embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        """Called when a member is banned from a guild."""
        embed = discord.Embed(description="Banned", colour=member.color)
        embed.set_author(name="{0.name}#{0.discriminator}".format(member), icon_url=member.avatar_url(member))

        # If bot can see audit log, we can get more details of the ban
        entry = await self.get_audit_entry(guild, discord.AuditLogAction.ban, member)
        if entry:
            embed.set_footer(text="{0.name}#{0.discriminator}".format(entry.user),
                             icon_url=member.avatar_url(entry.user))
            if entry.reason:
                embed.description += f"\n**Reason:** {entry.reason}"
            await self.client.send_log_message(guild, embed=embed)
    
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Called every time a member is updated"""
        member = discord.Member
        def get_user_avatar(user: Union[discord.User, discord.Member]) -> str:
            """Gets the user's avatar url
            If they don't have an avatar set, the default avatar is returned.
            :param user: The user to get the avatar of
            :return: The avatar's url."""
            return user.avatar_url if user.avatar_url is not None else user.default_avatar_url
        if before.nick != after.nick:
            embed = discord.Embed(description=f"{after.mention}: ", color=member.color)
            embed.set_author(name=f"{after.name}#{after.discriminator} (ID: {after.id})",
                             icon_url=get_user_avatar(after))
            if before.nick is None:
                embed.description += f"Nickname set to **{after.nick}**"
            elif after.nick is None:
                embed.description += f"Nickname **{before.nick}** deleted"
            else:
                embed.description += f"Nickname changed from **{before.nick}** to **{after.nick}**"
            entry = await self.get_audit_entry(after.guild, discord.AuditLogAction.member_update, after)
            if entry and entry.user.id != after.id:
                icon_url = get_user_avatar(entry.user)
                embed.set_footer(text=f"{entry.user.name}#{entry.user.discriminator}", icon_url=icon_url)
            await self.client.send_log_message(after.guild, embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, member: discord.Member):
        """Called when a member is unbanned from a guild"""
        embed = discord.Embed(description="Unbanned", color=member.color)
        embed.set_author(name="{0.name}#{0.discriminator} (ID {0.id})".format(member), icon_url=member.avatar_url(member))

        entry = await self.get_audit_entry(guild, discord.AuditLogAction.unban, member)
        if entry:
            embed.set_footer(text="{0.name}#{0.discriminator}".format(entry.user),
                             icon_url=member.avatar_url(entry.user))
        await self.client.send_log_message(guild, embed=embed)

    @staticmethod
    async def get_audit_entry(guild: discord.Guild, action: discord.AuditLogAction,
                              target: Any = None) -> Optional[discord.AuditLogEntry]:
        """Gets an audit log entry of the specified action type.
        The type of the action depends on the action.
        :param guild: The guild where the audit log will be checked.
        :param action: The action to filter.
        :param target: The target to filter.
        :return: The first matching audit log entry if found.
        """
        if not guild.me.guild_permissions.view_audit_log:
            return
        now = datetime.datetime.utcnow()
        after = now - datetime.timedelta(0, 5)
        async for entry in guild.audit_logs(limit=10, oldest_first=False, action=action, after=after):
            if abs((entry.created_at - now)) >= datetime.timedelta(seconds=5):
                break
            if target is not None and entry.target.id == target.id:
                return entry

def setup(client):
    client.add_cog(Log(client))