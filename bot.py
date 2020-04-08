import os
import discord
import time
import asyncio

from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get

client = commands.Bot(command_prefix = '_')

client.remove_command('help')

client.load_extension(f'cogs.Administrator')
client.load_extension(f'cogs.CommandEvents')
client.load_extension(f'cogs.HelpCommands')
client.load_extension(f'cogs.Usersinfo')
client.load_extension(f'cogs.MiscCommands')
client.load_extension(f'cogs.Roles')
client.load_extension(f'cogs.Emotes')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=2,name="Spotify"))

@client.command()
@commands.has_guild_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}') #loads the extension in the "cogs" folder
    await ctx.send(f'loaded "{extension}"')
    print(f'loaded "{extension}"')
    return

@client.command()
@commands.has_guild_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}') #unloads the extension in the "cogs" folder
    await ctx.send(f'unloaded "{extension}"')
    print(f'unloaded "{extension}"')
    return

gmOptionEnabled = False

@client.command()
async def morninggreet(ctx, onOrOff):
    global gmOptionEnabled
    if str.lower(onOrOff) == "on" and gmOptionEnabled == False:
        gmOptionEnabled = True
        await ctx.send("sonofthebae will now greet people when they say good morning")
    elif str.lower(onOrOff) == "off" and gmOptionEnabled == True:
        gmOptionEnabled = False
        await ctx.send("sonofthebae will no longer greet people when they say good morning")

@client.event
async def on_message(message):
    global gmOptionEnabled
    if gmOptionEnabled == True:
        author = message.author
        if str.lower(str(message.content)) == 'good morning' or str.lower(str(message.content)) == 'gmorning':
            await message.channel.send(f'Good morning, {author.mention} <a:wenrenewaveb:687193351589855265><a:wenrenewavea:687193349513674762>' )
    await client.process_commands(message)

client.run(os.environ['DISCORD_TOKEN'])
