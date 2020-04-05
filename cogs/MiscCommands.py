import discord
import random
import asyncio

from discord.ext import commands
from random import choice as randchoice

class MicsCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[ '8ball'])
    async def _8ball(self, ctx, *, question):
        responses = [ 'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    async def add(self,ctx, a: int, b: int):
        await ctx.send(a+b)

    @commands.command()
    async def multiply(self,ctx, a: int, b: int):
        await ctx.send(a*b)

    @commands.command()
    async def subtract(self,ctx, a: int, b: int):
        await ctx.send(a-b)

    @commands.command()
    async def divide(self,ctx, a: int, b: int):
        await ctx.send(a/b)

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    async def choose(self,ctx, *,choices: str):
        """Chooses between multiple choices."""
        realchoices = str.split(choices,',')
        if len(realchoices) < 2:
            await ctx.send('Not enough choices to pick from.')
        else:
            await ctx.send(randchoice(realchoices))

    @commands.command(no_pm=True, hidden=True)
    async def hug(self,ctx, user : discord.Member):
        msg = ["(っ˘̩╭╮˘̩)っ","(っ´▽｀)っ","╰(*´︶`*)╯","(つ≧▽≦)つ","(づ￣ ³￣)づ" " ⊂(´・ω・｀⊂)"]
        await ctx.send(random.choice(msg))

    @commands.command()
    async def tableflip(self, ctx):
        """Tableflip!"""
        await ctx.send('(╯°□°）╯︵ ┻━┻')

    @commands.command()
    async def unflip(self, ctx):
        """Unfips!"""
        await ctx.send('┬─┬﻿ ノ( ゜-゜ノ)')

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"I'd rate {thing} a **{num}.{deci} / 100**")

    @commands.command(aliases=['howhot', 'hot'])
    async def hotcalc(self, ctx, *, someone: commands.clean_content):
        """ Returns a random percent for how hot is a discord user """
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"{someone} is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command()
    async def numgame(self,ctx):
        number = random.randint(1,100)
        await ctx.send('Guess a number between 1 and 100. You have 5 chances.')
        def check(m):
            return m.channel == ctx.channel
        guess = 5
        while guess != 0:
            msg = await self.client.wait_for('message',check=check)
            attempt = int(msg.content)
            if attempt > number:
                await asyncio.sleep(1)
                await ctx.send('Try going lower')
                guess -= 1
                await ctx.send(f"You have {guess} chances left.")
            elif attempt < number:
                await asyncio.sleep(1)
                await ctx.send('Try going higher')
                guess -=1
                await ctx.send(f"You have {guess} chances left.")
            elif attempt == number:
                await ctx.send('You guessed it! Good job!')
                break
        else:
            guess == 0
            await ctx.send("<:ireneyikes:679733703647559720> What a loser!")
    @numgame.error
    async def numgame_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Invalid input.Plese restart the game.")
                


def setup(client):
    client.add_cog(MicsCommands(client))
