import os
import discord
import time
import asyncio
import asyncpg

from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
from time import time

client = commands.Bot(command_prefix = '_')

client.load_extension(f'cogs.Administrator')
client.load_extension(f'cogs.CommandEvents')
client.load_extension(f'cogs.HelpCommands')
client.load_extension(f'cogs.Usersinfo')
client.load_extension(f'cogs.MiscCommands')
client.load_extension(f'cogs.Roles')
client.load_extension(f'cogs.Emotes')
client.load_extension(f'cogs.Log')
client.load_extension(f'cogs.Riddle')
client.load_extension(f'cogs.Pun')
client.load_extension(f'cogs.Covid')

async def main():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    print('Database connected.')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(686446361419186199)
    await channel.send("Sonbae is now online!")
    await client.change_presence(activity=discord.Activity(type=2,name="Spotify"))

@client.command(brief='load a cog (Admin only)')
@commands.has_guild_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}') #loads the extension in the "cogs" folder
    await ctx.send(f'loaded "{extension}"')
    print(f'loaded "{extension}"')
    return

@client.command(brief='unload a cog (Admin only)')
@commands.has_guild_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}') #unloads the extension in the "cogs" folder
    await ctx.send(f'unloaded "{extension}"')
    print(f'unloaded "{extension}"')
    return

@client.command(brief='bot ping (Admin only)')
async def ping(ctx):
    start = time()
    message = await ctx.send(f'Pong! Latency: {client.latency*1000:,.0f} ms.')
    end = time()
    await message.edit(content=f'Pong! Latency: {client.latency*1000:,.0f} ms. Response time:{(end-start)*1000:,.0f} ms.')
    
@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "\U0001F4CC":
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
            
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)
        message = await channel.fetch_message(message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        if reaction.count >= 3:
            await message.pin()

asyncio.get_event_loop().run_until_complete(main())
client.run(os.environ['DISCORD_TOKEN'])

