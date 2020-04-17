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
    async def riddle(self,ctx):
        Questions =['What has to be broken before you can use it?', 
                'I’m tall when I’m young, and I’m short when I’m old. What am I?',
                'What month of the year has 28 days?', 
                'The more of this there is, the less you see. What is it?',
                'What has many keys but can’t open a single lock?', 
                'Where does today come before yesterday?', 
                'What invention lets you look right through a wall?',
                'If you’ve got me, you want to share me; if you share me, you haven’t kept me. What am I?',
                'It belongs to you, but other people use it more than you do. What is it?']
        Answers =['egg','candle','all','darkness','piano','dictionary','window','secret','name']
        if ctx.channel.id == 680233219303800893:
            i = random.choice(range(len(Questions)))
            await ctx.send(Questions[i])
            await ctx.send('Type your answer below. You have 30 seconds and only 1 chance.')
            def check(m):
                try:
                    return str(m.content) and m.channel.id == 680233219303800893
                except ValueError:
                    return False
            if ctx.channel.id == 680233219303800893:   
                try:     
                    msg = await self.client.wait_for('message',check=check,timeout=30.0)
                    if msg.content.lower() != Answers[i]:
                        await asyncio.sleep(1)
                        await ctx.send(f'Incorrect. Game over. Dumb Dumb!')
                    elif msg.content.lower() == Answers[i]:
                        await asyncio.sleep(1)
                        await ctx.send('You got it')
                except TimeoutError:
                    return await ctx.send('Oops! Nobody solved it.')
        else:
            await ctx.send("Please go to bot channel to use the command.")

def setup(client):
    client.add_cog(Riddle(client))        