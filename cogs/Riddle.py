import discord
import random
import asyncio

from discord.ext import commands
from random import choice as randchoice
from random import randint, sample

class Riddle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=[ 'rd'],brief='guess a word from riddles',description='_rd to start')
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def riddle(self,ctx):
        Questions =['What has to be broken before you can use it?', 
                'I’m tall when I’m young, and I’m short when I’m old. What am I?',
                'What month of the year has 28 days?', 
                'The more of this there is, the less you see. What is it?',
                'What has many keys but can’t open a single lock?', 
                'Where does today come before yesterday?', 
                'What invention lets you look right through a wall?',
                'If you’ve got me, you want to share me; if you share me, you haven’t kept me. What am I?',
                'It belongs to you, but other people use it more than you do. What is it?',
                'There are 30 cows in a field, and 28 chickens. How many didnt?',
                'If life gets tough, what do you have that you can always count on?',
                'What is one thing that all wise men, regardless of their politics or religion, agree is between heaven and earth?',
                'What is easy to get into, but hard to get out of?',
                'A seven letter word containing thousands of letters',
                'A kind of tree can you carry in your hand?',
                'I can fly but have no wings. I can cry but I have no eyes. Wherever I go, darkness follows me. What am I?',
                'Feed me and I live, yet give me a drink and I die',
                'What 4-letter word can be written forward, backward or upside down, and can still be read from left to right?',
                'What flies without wings?',
                'What begins with T, ends with T and has T in it?',
                'What can you catch but not throw?',
                'What can travel around the world while staying in a corner?',
                'What is as big as you are and yet does not weigh anything?',
                'Take off my skin - I wont cry, but you will! What am I?',
                'What has four legs, but cant walk?',
                'You are my brother, but I am not your brother. Who am I?',
                'Whats orange and sounds like a parrot?',
                'Where do fish keep their money?',
                'I am always in front and never behind. What am I?',
                'Which word contains 26 letters but only three syllables?',
                'What has four eyes but cant see?',
                'What never asks questions but is always answered. What am I?',
                'What has cities, but no houses; forests, but no trees; and water, but no fish?',
                'What is harder to catch the faster you run?',
                'Which vehicle is spelled the same forwards and backwards?',
                'What type of dress can never be worn?',
                'What loses its head in the morning but gets it back at night?',
                'What tastes better than it smells?',
                'What is the saddest fruit?',
                'A barrel of water weighs 20 pounds. What must you add to it to make it weigh 12 pounds?',
                'I turn around once. What is out will not get in. I turn around again. What is in will not get out. What am I?',
                'What goes through a door but never goes in and never comes out?',
                'What disappears the moment you say its name?',
                'This company makes billions of dollars selling Windows.',
                'What is it something that you always have but you always leave behind?',
                'I am flat when I am new. I am fat when you use me. I release my gas when something sharp touches me. What am I?',
                'Look at me. I can bring a smile to your face, a tear to your eye, or even a thought to your mind. But, I cant be seen. What am I?',
                'What does December have that other months dont have?',
                'What goes through towns and over hills but never moves?',
                'What can be seen in the middle of March and April that cannot be seen at the beginning or end of either month?',
                'I make two people out of one. What am I?',
                'What has six faces, but does not wear makeup, has twenty-one eyes, but cannot see? What is it?',
                'I am white when I am dirty, and black when I am clean. What am I?',
                'They have not flesh, nor feathers, nor scales, nor bone. Yet they have fingers and thumbs of their own. What are they?',
                'Poor people have it. Rich people need it. If you eat it you die. what is it?',
                'Always in you, Sometimes on you; If I surround you, I can kill you.What am I?',
                'I have no feet, no hands, no wings, but I climb to the sky. What am I?',
                'What 5 letter word typed in all capital letters can be read the same upside down?',
                'What English word has three consecutive double letters?',
                'What has a head and a tail but no body?']
                
        Answers =['egg','candle','all','darkness','piano','dictionary','window','secret','name','ten','fingers','and','trouble','mailbox',
        'palm','clouds','fire','noon','time','teapot','cold','stamp','shadow','onion','table','sister','carrot','riverbank','future','alphabet',
        'mississippi','doorbell','map','breath','racecar','address','pillow','tongue','blueberry','holes','key','keyhole','silence',
        'microsoft','fingerprint','balloon','memories','d','road','r','mirror','dice','blackboard','gloves','nothing','water','smoke',
        'swims','bookkeeper','coin']

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
                return await ctx.channel.purge(limit=1)

def setup(bot):
    bot.add_cog(Riddle(bot))        