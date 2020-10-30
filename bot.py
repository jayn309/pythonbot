import os
import discord
import time
import asyncio
import asyncpg
import apscheduler

from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
from time import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '_',owner_id=359401025330741248,intents=intents) 


bot.load_extension(f'cogs.Administrator')
bot.load_extension(f'cogs.CommandEvents')
bot.load_extension(f'cogs.HelpCommands')
bot.load_extension(f'cogs.Usersinfo')
bot.load_extension(f'cogs.MiscCommands')
bot.load_extension(f'cogs.Roles')
bot.load_extension(f'cogs.Emotes')
bot.load_extension(f'cogs.Log')
bot.load_extension(f'cogs.Riddle')
bot.load_extension(f'cogs.Pun')
bot.load_extension(f'cogs.Covid')
bot.load_extension(f'cogs.Instagram')
bot.load_extension(f'cogs.WolframAlpha')
bot.load_extension(f'cogs.Weather')
bot.load_extension(f'cogs.Urban')
bot.load_extension(name='jishaku')
print("All cogs are loaded.")

#async def main():
    #con = await asyncpg.connect(os.environ['DATABASE_URL'])
    #print('Database connected.')
    #await con.execute('''
        #DROP TABLE mytab;
    #''')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(686446361419186199)
    await channel.send("Sonbae is now online!")
    bot.scheduler = AsyncIOScheduler()
    bot.scheduler.start()
    await bot.change_presence(activity=discord.Activity(type=2,name="Spotify"))

@bot.command(brief='load a cog (Admin only)')
@commands.has_guild_permissions(administrator=True)
@commands.guild_only()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}') #loads the extension in the "cogs" folder
    await ctx.send(f'loaded "{extension}"')
    print(f'loaded "{extension}"')
    return

@bot.command(brief='unload a cog (Admin only)')
@commands.has_guild_permissions(administrator=True)
@commands.guild_only()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}') #unloads the extension in the "cogs" folder
    await ctx.send(f'unloaded "{extension}"')
    print(f'unloaded "{extension}"')
    return

@bot.command(brief='bot ping (Admin only)')
@commands.guild_only()
async def ping(ctx):
    start = time()
    message = await ctx.send(f'Pong! Latency: {bot.latency*1000:,.0f} ms.')
    end = time()
    await message.edit(content=f'Pong! Latency: {bot.latency*1000:,.0f} ms. Response time:{(end-start)*1000:,.0f} ms.')
    
@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "\U0001F4CC":
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
            
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        channel = discord.utils.find(lambda c : c.id == channel_id, guild.channels)
        message = await channel.fetch_message(message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        if reaction.count >= 3:
            await message.pin()

#asyncio.get_event_loop().run_until_complete(main())
bot.run(os.environ['DISCORD_TOKEN'])

