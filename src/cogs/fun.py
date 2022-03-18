import nextcord.ext
from nextcord.ext import commands
import os
import json
import requests

RANDOMMER_API = os.getenv("RANDOMMER_API")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jotd(self, ctx):
        """
        Get joke of the day using jokes.one API.
        """

        url = 'https://api.jokes.one/jod?category=knock-knock'
        api_token = None
        headers = {'content-type': 'application/json',
                   'X-JokesOne-Api-Secret': format(api_token)}

        response = requests.get(url, headers=headers)
        jokes = response.json()['contents']['jokes'][0]
        embed = nextcord.Embed(
            title=jokes['joke']['title'],
            colour=nextcord.Colour.green())
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar)
        embed.description = (f"""
        {jokes['joke']['text']}
        ----
        Joke provided by https://jokes.one/
        """)
        await ctx.send(embed=embed)


    @commands.command()
    async def rfullname(self, ctx):
        """
        Get a random fullname using randommer API.
        """

        headers = {
            'accept': '*/*',
            'X-Api-Key': RANDOMMER_API,
        }

        params = (
            ('nameType', 'fullname'),
            ('quantity', 1),
        )

        response = requests.get(
            'https://randommer.io/api/Name',
            headers=headers,
            params=params)
        respjson = json.loads(response.text)
        respsend = respjson[0]
        await ctx.reply(respsend)


    @commands.command()
    async def rfirstname(self, ctx):
        """
        Get a random firstname using randommer API.
        """

        headers = {
            'accept': '*/*',
            'X-Api-Key': RANDOMMER_API,
        }

        params = (
            ('nameType', 'firstname'),
            ('quantity', 1),
        )

        response = requests.get(
            'https://randommer.io/api/Name',
            headers=headers,
            params=params)
        respjson = json.loads(response.text)
        respsend = respjson[0]
        await ctx.reply(respsend)


    @commands.command()
    async def rsurname(self, ctx):
        """
        Get a random surname using randommer API.
        """

        headers = {
            'accept': '*/*',
            'X-Api-Key': RANDOMMER_API,
        }

        params = (
            ('nameType', 'surname'),
            ('quantity', 1),
        )

        response = requests.get(
            'https://randommer.io/api/Name',
            headers=headers,
            params=params)
        respjson = json.loads(response.text)
        respsend = respjson[0]
        await ctx.reply(respsend)


def setup(bot):
    bot.add_cog(Fun(bot))
