import os
import discord
import time
import asyncio
import asyncpg
import apscheduler
import motor.motor_asyncio

from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
from time import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.mongo import Document

#async def main():
    #con = await asyncpg.connect(os.environ['DATABASE_URL'])
    #print('Database connected.')
    #await con.execute('''
        #DROP TABLE mytab;
    #''')

async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("_")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("_")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("_")(bot, message)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = get_prefix,owner_id=359401025330741248,intents=intents) 
bot.connection_url = os.environ["mongodb_url"]

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


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: _\n-----")
    channel = bot.get_channel(686446361419186199)
    await channel.send("Sonbae is now online!")

    bot.scheduler = AsyncIOScheduler()
    bot.scheduler.start()
    await bot.change_presence(activity=discord.Activity(type=2,name="Spotify"))

    if bot.connection_url:
        bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
        bot.db = bot.mongo["sonofthebae"]
        bot.config = Document(bot.db, "config")
        bot.invites = Document(bot.db, "invites")
        print("Initialized Database\n-----")
        for document in await bot.config.get_all():
            print(document)
    else:
        print("ERROR: Database not set")
        return


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

@bot.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.bot:
        return

    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@!{bot.user.id}>") and \
        len(message.content) == len(f"<@!{bot.user.id}>"
    ):
        data = await bot.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = "_"
        else:
            prefix = data["prefix"]
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

    await bot.process_commands(message)

#asyncio.get_event_loop().run_until_complete(main())
bot.run(os.environ['DISCORD_TOKEN'])

