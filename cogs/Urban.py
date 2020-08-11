import aiohttp
from discord.ext import commands
import discord
import typing


class Urban(commands.Cog):  # Creates class
	def __init__(self, bot):  # Defines initialise
		self.bot = bot

	@commands.command(aliases=['ub'],brief='search for definition from urban dictionary')  # Creats command object
	async def urban(self, ctx, index: typing.Optional[int] = 0, *, term: str):  # Defines command
		try:

			async with aiohttp.ClientSession() as session:  # Opens client session
				async with session.get("https://api.urbandictionary.com/v0/define", params={"term": term}) as r:  # Result
					result = await r.json()  # Parses file as json

				data = result["list"][index]  # Assigns list in dict as 'data'

				defin = data["definition"]  # Gets key value
				if "2." in defin:  # If there is a second definition
					defin = data["definition"].split("2.")  # Splits data
					defin = defin[0]  # Sets defin as first definition
				elif len(defin) > 250:  # Sets a 250 character limit
					defin = defin[:250]

				example = data["example"]  # Gets key value
				if "2." in defin:  # If there is a second example splits data
					example = data["example"].split("2.")  # Splits data
					example = example[0]  # Sets defin as first example
				elif len(example) > 250:   # Sets a 250 character limit
					example = example[:250]

				urban_embed = discord.Embed(title="Result for {0}".format(term),
											url=data["permalink"],
											colour=ctx.author.color)
				# Creates# embed with a title with a hyperlink and set's the colour of the bar
				urban_embed.add_field(name="Definition", value=defin, inline=False)  # Adds field
				urban_embed.add_field(name="Example", value=example or "N/A", inline=False)
				urban_embed.add_field(name="👍", value=data["thumbs_up"], inline=True)
				urban_embed.add_field(name="👎", value=data["thumbs_down"], inline=True)
				urban_embed.set_footer(text="Author: " + data["author"])
				await ctx.send(embed=urban_embed)  # Sends the embed
				return  # Halts further action
		except IndexError:
			await ctx.send("Your search terms gave no results.")
		except:
			return


def setup(bot):
	bot.add_cog(Urban(bot))