import discord
import random
import asyncio

from discord.ext import commands
from random import choice as randchoice
from random import randint, sample

class Riddle(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
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
                'What can be seen in the middle of March and April that cannot be seen at the beginning or end of either month?']
                
        Answers =['egg','candle','all','darkness','piano','dictionary','window','secret','name','ten','fingers','and','trouble','mailbox',
        'palm','clouds','fire','noon','time','teapot','cold','stamp','shadow','onion','table','sister','carrot','riverbank','future','alphabet',
        'mississippi','doorbell','map','breath','racecar','address','pillow','tongue','blueberry','holes','key','keyhole','silence',
        'microsoft','fingerprint','balloon','memories','d','road','r']
        if ctx.channel.id == 680233219303800893:
            i = random.choice(range(len(Questions)))
            await asyncio.sleep(1)
            await ctx.send(Questions[i])
            await asyncio.sleep(1)
            await ctx.send('Type your answer(1 word) below. You have 30 seconds and only 1 chance.')
            def check(m):
                try:
                    return str(m.content) and m.channel.id == 680233219303800893
                except ValueError:
                    return False
            if ctx.channel.id == 680233219303800893:   
                try:     
                    msg = await self.client.wait_for('message',check=check,timeout=30.0)
                    await ctx.channel.purge(limit=3)
                    if msg.content.lower() != Answers[i]:
                        await asyncio.sleep(1)
                        await ctx.send(f'Incorrect. Game over. Dumb Dumb! <:wendyyikes:682673361725554785>')
                    elif msg.content.lower() == Answers[i]:
                        await asyncio.sleep(1)
                        await ctx.send('You got it <:wensun:699102648229691402> ')
                except asyncio.TimeoutError:
                    await ctx.send('Oops! Nobody solved it.')
                    return await ctx.channel.purge(limit=3)
        else:
            await ctx.send("Please go to bot channel to use the command.")

def setup(client):
    client.add_cog(Riddle(client))        