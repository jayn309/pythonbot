import os
import discord
import time
import asyncio

from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get

client = commands.Bot(command_prefix = '_')

client.remove_command('help')

startup_extensions = ["Administrator","CommandEvents","HelpCommands","MiscCommands","Roles", "Usersinfo"]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=2,name="Spotify"))

@client.command()
async def load(ctx, startup_extensions):
    client.load_extension(startup_extensions)
    await ctx.send(f'loaded "{startup_extensions}"')
    print(f'loaded "{startup_extensions}"')
    return

@client.command()
async def mload(ctx, extension):
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
