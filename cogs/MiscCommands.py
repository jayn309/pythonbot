import discord
import random
import asyncio
import re
import aiohttp
import pendulum
import googletrans
import datetime

from discord import Spotify
from discord.ext import commands
from discord.ext.commands import EmojiConverter, PartialEmojiConverter
from random import choice as randchoice
from random import randint, sample
from googletrans import Translator, LANGUAGES,LANGCODES
from typing import Union

class MicsCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[ '8b'],brief='get random answer for a question')
    async def eightb(self, ctx, *, question):
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
    
    @commands.command(pass_context=True,brief='Solves a math problem\n+ = add, - = subtract, * = multiply, and / = divide\nExample:\n_calc 1+1+3*4')
    async def calc(self, ctx, evaluation):
        prob = re.sub("[^0-9+-/* ]", "", ctx.message.content[len(ctx.prefix + ctx.command.name) + 1:].strip())
        if len(evaluation) > 64:
            await ctx.send("That evalution is too big, I can allow a maximum of 64 characters, I suggest you divide it in smaller portions.")
            return
        try:
            answer = str(eval(prob))
            await ctx.send("`{}` = `{}`".format(prob, answer))
        except:
            await ctx.send("I couldn't solve that problem, it's too hard.")

    @commands.command(aliases=['flip', 'coin'],brief='flip a coin')
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command(brief='pay your respect')
    async def f(self, ctx, *, reason: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{reason}** " if reason else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command(aliases=[ 'ch'],brief='choose between choices .Use , between your choices.')
    async def choose(self,ctx, *,choices: str):
        """Chooses between multiple choices."""
        realchoices = str.split(choices,',')
        if len(realchoices) < 2:
            await ctx.send('Not enough choices to pick from.')
        else:
            await ctx.send(randchoice(realchoices))

    @commands.command(no_pm=True, hidden=True,brief='give a hug to a member')
    async def hug(self,ctx, user : discord.Member):
        msg = ["(っ˘̩╭╮˘̩)っ","(っ´▽｀)っ","╰(*´︶`*)╯","(つ≧▽≦)つ","(づ￣ ³￣)づ" " ⊂(´・ω・｀⊂)"]
        await ctx.send(random.choice(msg))

    @commands.command(aliases=[ 'tbf'],brief ='flip the table')
    async def tableflip(self, ctx):
        """Tableflip!"""
        await ctx.send('(╯°□°）╯︵ ┻━┻')

    @commands.command(aliases=[ 'unf'],brief='unflip the table')
    async def unflip(self, ctx):
        """Unfips!"""
        await ctx.send('┬─┬﻿ ノ( ゜-゜ノ)')

    @commands.command(brief='rate something')
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"I'd rate {thing} a **{num}.{deci} / 100**")

    @commands.command(aliases=['hot'],brief='how hot someone/something is')
    async def hotcalc(self, ctx, *, object: commands.clean_content):
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

        await ctx.send(f"{object} is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=['slots', 'bet'],brief='play slot machine',description='_slot to start')
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

    @commands.command(aliases=['ng'],brief='guess a number',description='_ng to start')
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def numgame(self,ctx):
        number = random.randint(1,100)
        await ctx.send('Guess a number between 1 and 100. You have 5 chances.')
        def check(m):
            try:
                return int(m.content) and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            except ValueError:
                return False
        guess = 5
        while guess != 0:
            try:
                msg = await self.client.wait_for('message',check=check,timeout=60.0)
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
                    await ctx.send('You guessed it! Good job! <a:awendythumbsup:700918916637130753> ')
                    break
            except asyncio.TimeoutError:
                await ctx.send('Nobody guessed it. Bye.')
                return
        else:
            guess == 0
            await ctx.send("<:ireneyikes:679733703647559720> What a loser!")

    @commands.command(brief='play rps',description='_rps to start')
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

    @commands.command(brief='mocking the previous message or a specific message by id',description= '_mock to mock the lasted message sent in the channel or _mock id to mock a specific message in the same channel.')
    async def mock(self, ctx, *, args=""):
        emoteregex=re.compile(r'<(a)*:[\w]+:([0-9]+)>( )*')
        def mockthis(s):
            #remove custom emotes (keeps unicode emojis)
            s=re.sub(emoteregex,"",s)
            m=""
            #build new string swapcasing at random
            for i in range(len(s)):
                if random.getrandbits(1)==1:
                    m+=s[i].swapcase()
                else:
                    m += s[i]
            return m

        #if args empty then mock a previous message
        if len(args.strip())==0:
            #get the last x num of messages in channel
            lastmessagelist = await ctx.channel.history(limit=16).flatten()
            i=0
            while i < len(lastmessagelist):
                #valid mock if msg is not from the bot, does not only contain emotes, is not a mock command
                validmock=(not lastmessagelist[i].author.id==685307035142586380) and (len(re.sub(emoteregex,"",lastmessagelist[i].clean_content.strip()))>0) and (not lastmessagelist[i].clean_content[1:5]=="mock")
                if validmock:
                    break
                i+=1
            #if loop didn't finish then i refers to a valid mock message in list
            if i<len(lastmessagelist):
                await ctx.send(mockthis(lastmessagelist[i].clean_content))
                await ctx.send("<:irenemock:686573132185600010>")
            else:
                await ctx.send("<:wendycry:706669625030606858> found nothing to mock")
            return

        try:
            # if args is not empty it's a possible msg id
            msgid=int(args.strip())
            msg=await ctx.channel.fetch_message(msgid)
            msgctx = await self.client.get_context(msg)
            # if targetted msg was from the bot
            if msg.author.id==685307035142586380:
                await ctx.send(f"{msg.clean_content}")
                await ctx.send("<:ireneevilsmile:682673054924537954>")
            #if targetted msg was a mock command
            elif msgctx.valid and msg.clean_content[1:5]=="mock":
                await ctx.send("Mocking the mock command")
                await ctx.send("<:wendywhat:681337728910098434>")
            # if targetted msg only had an emote
            elif len(re.sub(emoteregex,"",msg.clean_content.strip()))==0:
                await ctx.send("Mocking emotes")
                await ctx.send("<:wendywhat:681337728910098434>")
            #else mock targetted msg
            else:
                await ctx.send(mockthis(msg.clean_content))
                await ctx.send("<:irenemock:686573132185600010>")
        except discord.NotFound:
            await ctx.send("<a:wendyanxious:697964082619351142> message not found")
        except discord.Forbidden:
            await ctx.send("<:wendyconcerned:684198747923939341> forbidden message")
        except discord.HTTPException:
            await ctx.send("<a:wendyspeechless:684122984801107983> error finding message")
        #args is not num/msgid. mock args
        except ValueError:
            await ctx.send(mockthis(ctx.message.clean_content[6:]))
            await ctx.send("<:irenemock:686573132185600010>")

    @commands.command(aliases=['gg'],brief='google search')
    async def google(self,ctx, *,argument):
        author = ctx.message.author
        embed = discord.Embed(title="Google Result", color= ctx.message.author.colour)
        argument1 = argument.replace(" ","+")
        embed.add_field(name="Here is your result:", value=f"**Request**: {argument}\n**Result**: Click [here](https://www.google.com/search?q={argument1})")
        embed.set_footer(text=f"Requested by {author}")
        await ctx.send(embed=embed)   

    @commands.command(aliases=['ytb'],brief='youtube search')
    async def youtube(self,ctx, *, query:str):
        async with aiohttp.request("GET", f'https://www.youtube.com/results?search_query={query}') as resp:
            res2= await resp.text()
            search_results = re.findall('\"\/watch\?v=(.{11})',res2)
            result = "https://www.youtube.com/watch?v=" + search_results[0]
            await ctx.send(f"{ctx.author.mention} {result}")  

    @commands.command(aliases=['stf'],brief='show what you are listening to on Spotify')
    async def spotify(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                em = discord.Embed(color=activity.color)
                em.title = f'{user.name} is listening to {activity.title}'
                em.set_thumbnail(url=activity.album_cover_url)
                em.description = f"**Song Name**: {activity.title}\n**Song Artist**: {activity.artist}\n**Song Album**: {activity.album}\n**Song Lenght**: {pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}"
                await ctx.send(embed=em)
                break
        else:
            embed = discord.Embed(color=ctx.author.colour)
            embed.title = f'{user.name} is not listening to Spotify right now!'
            await ctx.send(embed=embed)

    @commands.command(aliases=['tl'],brief='google translate')
    async def translate(self,ctx, lang, *, args):
        if lang is None:
            await ctx.send('Please provide a language.')
        else:
            try:
                t = Translator()
                a = t.translate(args, dest=lang)
                await ctx.send(a.text)
            except ValueError:
                await ctx.send('Invalid language.')
                return


    @commands.command(aliases=['svinfo','si'],brief='get info of the server')
    async def serverinfo(self, ctx):
        embed = discord.Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(aliases=['el','l'],brief='get an enlarged verson of an emote')
    async def enlarge(self, ctx, emoji : str):
        base_url = 'https://cdn.discordapp.com/emojis/{}.png?v=1'
        match = re.match(r'<:(\w+):(\d+)>', emoji)
        animated_url = 'https://cdn.discordapp.com/emojis/{}.gif?v=1'
        amatch = re.match(r'<[a-n]:(\w+):(\d+)>', emoji)
        if match:
            url = base_url.format(match.group(2))
            await ctx.send(f'{url}')
        elif amatch:
            x = re.search(r'<(\d+)>', emoji)
            await ctx.send(x)
            aurl = animated_url.format(match.group(3))
            await ctx.send(f'{aurl}')
        else:
            await ctx.send(f'``{emoji}`` is not an emoji')

def setup(client):
    client.add_cog(MicsCommands(client))
