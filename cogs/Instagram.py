import asyncio
import json
import logging
from io import BytesIO
from os.path import basename
from urllib.parse import urlparse
import re

import aiohttp
from discord import File
from discord.ext import commands

logger = logging.getLogger(__name__)

INSPECT_EMOJI = '\N{RIGHT-POINTING MAGNIFYING GLASS}'

@staticmethod
def chunker(iterable, n, return_index=False):
        """
        Produces a generator that yields chunks of given size from an iterator.
        :param iterable: iterable to generate chunks from
        :param n: number of items in each chunk
        :param return_index: set to true if first yielded value should be the chunk's starting index
        :return: the individual chunks
        """
        for i in range(0, len(iterable), n):
            if return_index:
                yield i, iterable[i:i + n]
            else:
                yield iterable[i:i + n]      


class Instagram(commands.Cog):
    URL_REGEX = r"https?://www.instagram.com/(p|tv)/(.*?)/"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

        self.cookies_file = self.bot.config['instagram']['cookies_file']
        with open(self.cookies_file, 'r') as f:
            self.session.cookie_jar.update_cookies(cookies=json.load(f))

        logger.info(f'Loaded {len(self.session.cookie_jar)} cookies')

    def cog_unload(self):
        asyncio.create_task(self.session.close())

    async def get_media(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        }

        params = {
            '__a': 1
        }

        async with self.session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            data = data['graphql']['shortcode_media']

        media_type = data['__typename']

        if media_type == 'GraphImage':
            return [data['display_url']]
        elif media_type == 'GraphVideo':
            return [data['video_url']]
        else:
            media = data['edge_sidecar_to_children']['edges']
            return [media['node']['display_url'] if
                    media['node']['__typename'] == 'GraphImage' else media['node']['video_url'] for media in media]
          

    async def show_media(self, ctx, url):
        media = await self.get_media(url)
        if len(media) == 0:
            raise commands.BadArgument('This Instagram post contains no images or videos.')

        files = []

        for url in media:
            async with self.session.get(url) as response:
                filename = basename(urlparse(url).path)
                file = File(BytesIO(await response.read()), filename=filename)
                files.append(file)

        # remove discord's default instagram embed
        await ctx.message.edit(suppress=True)

        chunks = chunker(files, 10)
        for chunk in chunks:
            await ctx.send(files=chunk)


    @commands.group(aliases=['ig'], invoke_without_command=True, brief='Display posts from Instagram')
    async def instagram(self, ctx, args=None):
        if args:
            await ctx.invoke(self.show, url=args)
        else:
            await ctx.send_help(self.instagram)

    @instagram.command()
    async def show(self, ctx, url):
        result = re.match(self.URL_REGEX, url)
        if result:
            url = result.group(0)
        else:
            raise commands.BadArgument('Invalid Instagram URL.')

        await self.show_media(ctx, url)

    @instagram.command()
    @commands.is_owner()
    async def reload(self, ctx):
        with open(self.cookies_file, 'r') as f:
            self.session.cookie_jar.update_cookies(cookies=json.load(f))

        await ctx.send(f'Loaded {len(self.session.cookie_jar)} cookies')


    async def cog_before_invoke(self, ctx):
        await ctx.trigger_typing()