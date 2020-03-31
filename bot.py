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

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=2,name="Spotify"))

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}') #loads the extension in the "cogs" folder
    await ctx.send(f'loaded "{extension}"')
    print(f'loaded "{extension}"')
    return

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}') #unloads the extension in the "cogs" folder
    await ctx.send(f'unloaded "{extension}"')
    print(f'unoaded "{extension}"')
    return

client.run(os.environ['DISCORD_TOKEN'])
