import os
import discord
import time
import asyncio

from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get

client = commands.Bot(command_prefix = '_')
status = cycle(['Happiness',
                'Ice Cream Cake','Automatic','Somethin Kinda Crazy','Stupid Cupid','Take It Slow',
                'Candy','Be Natural','Dumb Dumb','Huff n Puff','Campfire','Red Dress',
                'Oh Boy','Lady’s Room','Time Slip','Don’t U Wait No More','Day 1',
                'Cool World','Wish Tree','One Of These Nights','Cool Hot Sweet Love',
                'Light Me Up','First Time','Rose Scent Breeze','One Of These Nights(De-Capo Ver.)',
                'One Of These Nights (7월 7일) (Joe Millionaire Ver.)',
                'One Of These Nights (7월 7일) (Piano Ver.)','Russian Roulette','Lucky Girl',
                'Bad Dracula','Sunny Afternoon','Fool','Some Love','My Dear','Rookie',
                'Little Little', 'Happily Ever After','Talk To Me','Body Talk','Last Love',
                'Would U','Red Flavor','You Better Know','Zoo','Mojito','Hear The Sea',
                'Rebirth','Peek-A-Boo','Look','I Just','Kingdom Come','My Second Date','Attaboy',
                'Perfect 10','About Love','Moonlight Melody','Bad Boy','All Right','#Cookie Jar','Aitai-tai','Cause it’s you',
                'Power Up','With You','Mr. EMosquito','Hit That Drum','Blue Lemonade','Bad Boy (English Ver.)',
                'RBB','Butterflies','So Good','Sassy Me','Taste','RBB (English Ver.)','Sappy','Swimming Pool',
                'Sayonara','Peek-a-Boo (Japanese Ver.)','Rookie (Japanese Ver.)','Power Up (Japanese Ver.)',
                'Psycho','In & Out','Remember Forever','Eyes Locked, Hands Locked','Ladies Night','Jumpin','Love Is The Way',
                'Carpool','Umpah Umpah','LP','Parade','Bing Bing','Milkshake','Sunny Side Up','Zimzalabim','La Rouge'])

client.remove_command('help')

@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} has connected to Discord!')

@tasks.loop(minutes=1440)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=2,name=(next(status))))

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
