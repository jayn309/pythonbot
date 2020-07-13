import discord
import asyncio
import datetime
from discord.ext import commands
from discord.utils import get

role ="Unvelvified"

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() 
    async def on_member_join(self, member):
            role = get(member.guild.roles, name = "Unvelvified") 
            await member.add_roles(role)
            print(f"{member} just joined.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        message_id = payload.message_id
        channel_id = payload.channel_id
        if  message_id == 684015060888453148:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            
            if payload.emoji.name == 'wendysip':
                role = discord.utils.get(guild.roles, name='Admiral')
            if payload.emoji.name == 'wendyimpressed':
                role = discord.utils.get(guild.roles, name='Commander')
            if payload.emoji.name == 'irenepokerface':
                role = discord.utils.get(guild.roles, name='Captain')
            if payload.emoji.name == 'irenejudge':
                role = discord.utils.get(guild.roles, name='Lieutenant Commander')
            if payload.emoji.name == 'wendyhide':
                role = discord.utils.get(guild.roles, name='Ensign')
            if payload.emoji.name == 'irenemunch':
                role = discord.utils.get(guild.roles, name='Camping House')
            if payload.emoji.name == 'ireneevilsmile':
                role = discord.utils.get(guild.roles, name='Yadong Yaseol')

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)
                msg = await channel.fetch_message(payload.message_id)
                if member is not None:
                    if role in member.roles:
                        await member.remove_roles(role)
                        await channel.send(f'Role was removed.')
                        await asyncio.sleep(2)
                        await channel.purge(limit=1)
                    else:
                        await member.add_roles(role)
                        await channel.send(f'Role was added.')
                        await asyncio.sleep(2)
                        await channel.purge(limit=1)
                    await msg.remove_reaction(discord.Emoji,member)
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

        if message_id == 683696135793279127:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            if payload.emoji.name == 'wendyfist':
                role = discord.utils.get(guild.roles, name='Velvified')
                role1 = discord.utils.get(guild.roles, name='Unvelvified')
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)
                log_channel = discord.utils.get(member.guild.text_channels, name='role-log')
                if member is not None:
                    await member.add_roles(role)
                    await channel.send(f'Have fun. Pick a role tag in <#681672202822877207>.')
                    await asyncio.sleep(2)
                    await channel.purge(limit=1)
                    await member.remove_roles(role1)
                    if log_channel:
                        addrole_embed = discord.Embed(title='Role Add',colour=member.color)
                        addrole_embed.add_field(name="Member", value=member.name,inline=False)
                        addrole_embed.add_field(name="Role", value=role,inline=False)
                        addrole_embed.set_thumbnail(url=member.avatar_url)
                        addrole_embed.timestamp = datetime.datetime.utcnow()
                        await log_channel.send(embed=addrole_embed)
                    
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        message_id = payload.message_id
        channel_id = payload.channel_id
        if message_id == 684015060888453148:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)

            if payload.emoji.name == 'wendysip':
                role = discord.utils.get(guild.roles, name='Admiral')
            if payload.emoji.name == 'wendyimpressed':
                role = discord.utils.get(guild.roles, name='Commander')
            if payload.emoji.name == 'irenepokerface':
                role = discord.utils.get(guild.roles, name='Captain')
            if payload.emoji.name == 'irenejudge':
                role = discord.utils.get(guild.roles, name='Lieutenant Commander')
            if payload.emoji.name == 'wendyhide':
                role = discord.utils.get(guild.roles, name='Ensign')
            if payload.emoji.name == 'irenemunch':
                role = discord.utils.get(guild.roles, name='Camping House')
            if payload.emoji.name == 'ireneevilsmile':
                role = discord.utils.get(guild.roles, name='Yadong Yaseol')

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                log_channel = discord.utils.get(member.guild.text_channels, name='role-log')
                if member is not None:
                    await member.remove_roles(role)
                    await channel.send(f'Role was removed.')
                    await asyncio.sleep(2)
                    await channel.purge(limit=1)
                    if log_channel:
                        removerole_embed = discord.Embed(title='Role Remove',colour=member.color)
                        removerole_embed.add_field(name="Member", value=member.name,inline=False)
                        removerole_embed.add_field(name="Role", value=role,inline=False)
                        removerole_embed.set_thumbnail(url=member.avatar_url)
                        removerole_embed.timestamp = datetime.datetime.utcnow()
                        await log_channel.send(embed=removerole_embed)
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

        if message_id == 683696135793279127:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)           
            channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)

            if payload.emoji.name == 'wendyfist':
                role = discord.utils.get(guild.roles, name='Velvified')
            
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                log_channel = discord.utils.get(member.guild.text_channels, name='role-log')
                if member is not None:
                    await member.remove_roles(role)
                    if log_channel:
                        removerole_embed = discord.Embed(title='Role Remove',colour=member.color)
                        removerole_embed.add_field(name="Member", value=member.name,inline=False)
                        removerole_embed.add_field(name="Role", value=role,inline=False)
                        removerole_embed.set_thumbnail(url=member.avatar_url)
                        removerole_embed.timestamp = datetime.datetime.utcnow()
                        await log_channel.send(embed=removerole_embed)
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

def setup(client):
    client.add_cog(Roles(client))
