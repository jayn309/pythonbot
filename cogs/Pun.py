import discord
import random
import asyncio

from discord.ext import commands
from random import choice as randchoice
from random import randint, sample

class Pun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='guess a word from puns',description='_pun to start')
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def pun(self,ctx):
        Questions =['What bird can write?',
        'What clothing does a house wear?',
        'What day does an Easter egg hate the most?',
        'What did the cab driver wear to the ball?',
        'What do you call a fish with no eye?',
        'What is an astronaut’s favorite meal?',
        'What tea do hockey players drink?',
        'Where does Santa put his suit after Christmas?',
        'What do you call bears with no ears?',
        'What do you call an alligator in a vest?',
        'Where all the fish go on vacation?',
        'What do you call a pile of cats?',
        'What do you call a monkey that loves Doritos?',
        'What do you call a cow in an earthquake?',
        'What do you call a sad cup of coffee?',
        'What do you call an elephant that doesnt matter?',
        'What do you call a computer that sings?',
        'What do you call a witch who lives at the beach?',
        'What do you call a tiny mother?',
        'What do you call a factory that sells OK products',
        'What do you call a sleeping wolf?',
        'Which martial art are carrots best suited for?',
        'Where do cows go for a night out?',
        'Where do Russians get their milk?',
        'How does a farmer count a herd of cows?',
        'What do you call a grumpy cow?',
        'What happens if a cow laughs too hard?',
        'What do you call a happy penguin?',
        'Which Disney princess is a cows favorite?',
        'What do you call several men waiting in line for a haircut?',
        'Where do automobiles go for a dip?',
        'What is a vampires favorite fruit?',
        'What is a bakers favorite kind of tree?',
        'What is small, furry, and smells like bacon?',
        'Which fish only swims at night?',
        'What do duck like to watch on TV?',
        'Where did the duck go when he was sick?',
        'Which kind of melon can change colors at will?',
        'Which type of cucumber comes from the rainforest?',
        'What do a monkey wear while cooking?',
        'What do you call two witches who live together?',
        'What time does a tennis player get up?',
        'What kind of car does the sheep drive?',
        'What does a dog say when he sits down on a piece of sandpaper?',
        'What kind of shoes does a ninja wear?',
        'What is a lifeguards favorite game?',
        'What do you call an animal you keep in your car?',
        'What does a clam do on his birthday?',
        'What kind of birthday cake do you get for a coffee lover?',
        'How many tickles does it take to make a squid laugh?',
        'What is a bee from us called?']
                
        Answers =['penguin','address','fryday','taxido','fsh','launch','penaltea','clauset','b','investigator','finland',
        'meowntain','chipmonk','milkshake','depresso','irrelephant','adell','sandwitch','minimum','satisfactory','unawarewolf',
        'carrotee','moovie','moscows','cowculator','moody','cowlapse','pengrin','moolan','barbercue','carpool','necktarines',
        'pastree','hamster','starfish','duckumentaries','ducktor','chemelon','tropickle','aperon','broomates','tenish','subahhru','ruff','sneaker',
        'pool','carpet','shellabrates','chocolatte','tentickles','usbee']

        def check(m):
                try:
                    return str(m.content) and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                except ValueError:
                    return False
                    
        i = random.choice(range(len(Questions)))
        await asyncio.sleep(1)
        await ctx.send(Questions[i],delete_after=30)
        await asyncio.sleep(1)
        await ctx.send('Type your answer(1 word) below. You have 30 seconds and only 1 chance.',delete_after=30)
                
        try:     
            msg = await self.bot.wait_for('message',check=check,timeout=30.0)
            await ctx.channel.purge(limit=3) 
            if msg.content.lower() != Answers[i]:
                await asyncio.sleep(1)
                await ctx.send(f'Incorrect. Game over. Dumb Dumb! <:wendyyikes:682673361725554785>')
            elif msg.content.lower() == Answers[i]:
                await asyncio.sleep(1)
                await ctx.send('You got it <:wensun:699102648229691402> ')
        except asyncio.TimeoutError:
            await ctx.send('Oops! Nobody solved it.')
            await asyncio.sleep(1)
            return  await ctx.channel.purge(limit=1)


def setup(bot):
    bot.add_cog(Pun(bot)) 