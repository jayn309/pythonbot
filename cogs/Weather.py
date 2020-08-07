import asyncio
import logging
import os

import aiohttp
import pendulum
from discord import Embed
from discord.ext import commands

logger = logging.getLogger(__name__)

WEATHER_EMOJI = {
    '01': '\N{BLACK SUN WITH RAYS}',
    '02': '\N{SUN BEHIND CLOUD}',
    '03': '\N{CLOUD}',
    '04': '\N{CLOUD}',
    '09': '\N{CLOUD WITH RAIN}',
    '10': '\N{WHITE SUN BEHIND CLOUD WITH RAIN}',
    '11': '\N{THUNDER CLOUD AND RAIN}',
    '13': '\N{SNOWFLAKE}',
    '50': '\N{FOG}'
}

def celsius_to_fahrenheit(temp):
    return temp * (9 / 5) + 32


def meters_to_miles(meters):
    return meters * 0.000621371


def temp_string(temp):
    return f"{round(temp, 1)}°C ({round(celsius_to_fahrenheit(temp), 1)}°F)"


def visibility_string(visibility):
    if visibility is not None:
        return f"{round(visibility / 1000, 3)} km  ({round(meters_to_miles(visibility), 3)} mi)"
    else:
        return 'N/A'


def precipitation_string(rain, snow):
    rain_emoji, snow_emoji = (WEATHER_EMOJI['09'], WEATHER_EMOJI['13'])
    if rain > 0 < snow:
        return f'{rain_emoji} {rain} mm, {snow_emoji} {snow} mm'
    elif rain > 0:
        return f'{rain_emoji} {rain} mm'
    elif snow > 0:
        return f'{snow_emoji} {snow} mm'

    return '0 mm'


def icon_to_emoji(icon_string):
    icon = icon_string[:2]
    return WEATHER_EMOJI[icon]


class OpenWeatherMapApiException(Exception):
    pass


class Weather(commands.Cog):
    CURRENT_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
    ONECALL_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/onecall'

    MSG_REQUEST_FAILED = 'The request to OpenWeatherMap\'s API failed.'

    def __init__(self, bot):
        self.bot = bot
        self.app_id = os.environ['wtapp_id']
        self.session = aiohttp.ClientSession()

    async def _make_request(self, method, route):
        async with self.session.request(method, route) as response:
            if response.status == 200:
                content = await response.json()
                return content
            elif response.status == 404:
                content = await response.json()
                raise commands.BadArgument(content['message'])
            else:
                content = await response.json()
                raise OpenWeatherMapApiException(content['message'])

    def cog_unload(self):
        asyncio.create_task(self.session.close())

    @commands.group(name='weather',aliases=['wt'], invoke_without_command=True, brief='Query OpenWeatherMap for weather info (Limited Use)')
    async def weather(self, ctx, *, location):
        await ctx.invoke(self.current, location=location)
        
    @weather.command()
    async def current(self, ctx, *, location):
        response = await self._make_request('get',
                                            f'{Weather.CURRENT_WEATHER_API_URL}?appid={self.app_id}&q={location}&units=metric')
        coords = response['coord']
        lon, lat = coords.values()

        response_onecall = await self._make_request('get',
                                                    f'{Weather.ONECALL_WEATHER_API_URL}?appid={self.app_id}&lon={lon}&lat={lat}&units=metric')
        current = response_onecall['current']

        content = {
            'id': response['id'],
            'city': response['name'],
            'country': response['sys']['country'],
            'main': current['weather'][0]['main'],
            'description': current['weather'][0]['description'],
            'pressure': current['pressure'],
            'humidity': current['humidity'],
            'temp': current['temp'],
            'temp_min': min([hourly['temp'] for hourly in response_onecall['hourly']]),
            'temp_max': max([hourly['temp'] for hourly in response_onecall['hourly']]),
            'feels_like': current['feels_like'],
            'visibility': current['visibility'] if 'visibility' in current else None,
            'wind_deg': current['wind_deg'],
            'wind_speed': current['wind_speed'],
            'clouds': current['clouds'],
            'uvi': current['uvi'],
            'rain': current['rain']['1h'] if 'rain' in current and '1h' in current['rain'] else 0,
            'snow': current['snow']['1h'] if 'snow' in current and '1h' in current['snow'] else 0,
            'icon': f"http://openweathermap.org/img/wn/{current['weather'][0]['icon']}.png",
            'emoji': icon_to_emoji(current['weather'][0]['icon'])
        }

        embed = Embed()
        embed.add_field(name='Currently', value=f"{content['emoji']} {content['description']}")
        embed.add_field(name='Pressure', value=f"{content['pressure']} mbar")
        embed.add_field(name='Humidity', value=f"{content['humidity']}%")
        embed.add_field(name='Temperature Low', value=temp_string(content['temp_min']))
        embed.add_field(name='Temperature', value=temp_string(content['temp']))
        embed.add_field(name='Temperature High', value=temp_string(content['temp_max']))
        embed.add_field(name='Visibility', value=visibility_string(content['visibility']))
        embed.add_field(name='Wind Direction', value=f"{content['wind_deg']}°")
        embed.add_field(name='Wind Speed', value=f"{content['wind_speed']} m/s")
        embed.add_field(name='Precipitation (last h)', value=precipitation_string(content['rain'], content['snow']))
        embed.add_field(name='Cloud cover', value=f"{content['clouds']}%")
        embed.add_field(name='UV Index', value=content['uvi'])
        embed.timestamp = pendulum.now('UTC')
        embed.set_author(name=f"{content['city']}, {content['country']} at openweathermap.org",
                         url=f"https://openweathermap.org/city/{content['id']}",
                         icon_url=content['icon'])
        embed.set_footer(text='Powered by openweathermap.org')
        await ctx.send(embed=embed)


    async def cog_before_invoke(self, ctx):
        await ctx.trigger_typing()

def setup(bot):
    bot.add_cog(Weather(bot))
