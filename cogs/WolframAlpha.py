import asyncio
import logging
from io import BytesIO
import os
import keys

import aiohttp
from discord import File
from discord.ext import commands


logger = logging.getLogger(__name__)



class WolframAlpha(commands.Cog):
    RESULT_API_URL = 'https://api.wolframalpha.com/v1/result'
    SIMPLE_API_URL = 'https://api.wolframalpha.com/v1/simple'

    MSG_REQUEST_FAILED = 'The request to WolframAlpha\'s API failed.'
    MSG_EMPTY_RESPONSE = 'Try a different query. WolframAlpha is not cooperating.'

    def __init__(self, bot):
        self.bot = bot
        self.app_id = keys.app_id
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        asyncio.create_task(self.session.close())


    @commands.group(name='wolframalpha', aliases=['wa'], invoke_without_command=True,
                    brief='Query WolframAlpha (Limited Use)\nExample:\n_wa 40c in f\n_wa time korea')
    async def wolfram_alpha(self, ctx, *, args=None):
        if args:
            await ctx.invoke(self.simple, query=args)
        else:
            await ctx.send_help(self.wolfram_alpha)

    @wolfram_alpha.command(aliases=['s'])
    async def simple(self, ctx, *, query):
        async with self.session.get(f'{WolframAlpha.RESULT_API_URL}?appid={self.app_id}&i={query}') as response:
            if response.status != 200:
                await ctx.send(WolframAlpha.MSG_REQUEST_FAILED)
            else:
                content = await response.text()
                if content is not None:
                    await ctx.send(content)
                else:
                    await ctx.send(WolframAlpha.MSG_EMPTY_RESPONSE)

    @wolfram_alpha.command(aliases=['i'])
    async def image(self, ctx, *, query):
        async with self.session.get(f'{WolframAlpha.SIMPLE_API_URL}?appid={self.app_id}&i={query}') as response:
            if response.status != 200:
                await ctx.send(WolframAlpha.MSG_REQUEST_FAILED)
            else:
                content = await response.read()
                if content is not None:
                    file = File(BytesIO(content), filename='wolfram.gif')
                    await ctx.send(file=file)
                else:
                    await ctx.send(WolframAlpha.MSG_EMPTY_RESPONSE)

    async def cog_before_invoke(self, ctx):
        await ctx.trigger_typing()

def setup(bot):
    bot.add_cog(WolframAlpha(bot))
