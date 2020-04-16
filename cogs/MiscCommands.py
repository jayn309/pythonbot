import discord
import random
import asyncio

from discord.ext import commands
from random import choice as randchoice
from random import randint, sample

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
            try:
                int(m.content) and m.channel == ctx.channel
                return True
            except ValueError:
                return False

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

    @commands.command()
    async def rps(self,ctx, msg: str):
        t = ["rock","paper","scissors"]
        computer = t[randint(0, 2)]
        win = ["<a:wendyhype:696114546850529341>" , "<a:irenelikeit:696142888500985896>" , "<a:wendyshrug:696150254441201674>" , "<:wendysip:681749452859506696>", "<a:wenrenelaugha:698972968004485221><a:wenrenelaughb:698972969115844608>"]
        lose = ["<a:wendyspeechless:684122984801107983>" , "<:wendypleading:695287540617445446>" , "<:irenepout:683431934860591128>" , "<a:irenefreeze:696114438092095489>", "<:wendyfist:684275169585528852> "]
        huh = ["<:wendywhat:681337728910098434>" , "<:seulgisquint:683715248645210152>" , "<:irenejudge:685426997224144916>" , "<:irenemunch:685426997337653258>", "<a:wenrenefeedinga:683682968828379170><a:wenrenefeedingb:683682971353612334> "]
        tie = ["<:wendyfacepalm:685311963051327488>" , "<:irenemock:686573132185600010>" , "<:ireneunimpressed:686737662597398745>" , "<:ireneevilsmile:682673054924537954> "]
        player = msg.lower()
        print(msg)
        if player == computer:
            await asyncio.sleep(1)
            await ctx.send("Tie! ")
            await ctx.send(randchoice(tie))
        elif player == "rock":
            if computer == "paper":
                await asyncio.sleep(1)
                await ctx.send(f"paper. You lose!")
                await ctx.send(randchoice(win))
            else:
                await asyncio.sleep(1)
                await ctx.send("scissors. You win!")
                await ctx.send(randchoice(lose))
        elif player == "paper":
            if computer == "scissors":
                await asyncio.sleep(1)
                await ctx.send("scissors. You lose!")
                await ctx.send(randchoice(win))
            else:
                await asyncio.sleep(1)
                await ctx.send("rock. You win!")
                await ctx.send(randchoice(lose))
        elif player == "scissors":
            if computer == "rock":
                await asyncio.sleep(1)
                await ctx.send("rock. You lose!")
                await ctx.send(randchoice(win))
            else:
                await asyncio.sleep(1)
                await ctx.send("paper. You win!")
                await ctx.send(randchoice(lose))
        else:
            await asyncio.sleep(1)
            await ctx.send(randchoice(huh))


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

        await ctx.send('Pick a number from 0 to 9 to get a question')
        def check(m):
            try:
                int(m.content) and m.channel == ctx.channel
                return True
            except ValueError:
                return False
        num = await self.client.wait_for('message',check=check)
        position = int(num.content)
        await ctx.send(Questions[position])
        guess = 5
        while guess != 0:
            await asyncio.sleep(1)
            await ctx.send('Type answer along with your answer. Ex: answer a')
            def check1(n):
                try:
                    str(n.content) and n.channel == ctx.channel
                    return True
                except ValueError:
                    return False
            msg = await self.client.wait_for('message',check=check1)
            ans = msg.split()
            i = position
            for i in Answers:
                if ans.lower() != Answers[i].lower():
                    guess -=1
                    await ctx.send(f'Incorrect. you have {guess} chances left.')
                else:
                    await ctx.send('You got it')
        else:
            guess == 0
            await ctx.send('Try again. Dumb Dumb!')

def setup(client):
    client.add_cog(MicsCommands(client))
