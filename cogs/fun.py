import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks
import requests
import json

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()   
	async def joke(self, ctx):
		url = 'https://api.jokes.one/jod?category=knock-knock'
		api_token = None
		headers = {'content-type': 'application/json',
			   'X-JokesOne-Api-Secret': format(api_token)}
		
		response = requests.get(url, headers=headers)
		jokes=response.json()['contents']['jokes'][0]
		embed = nextcord.Embed(title = jokes['joke']['title'], colour=0x2ecc71)
		embed.set_author(name = "Pengoon")
		embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)
		embed.description = (f"""
		{jokes['joke']['text']}
		----
		Joke provided by https://jokes.one/
		""")
		await ctx.send(embed=embed)
   
def setup(bot):
    bot.add_cog(Fun(bot))
