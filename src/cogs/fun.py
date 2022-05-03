import nextcord.ext
from nextcord.ext import commands
import os
import json
import requests
import random
import nextcord.utils

RANDOMMER_API = os.getenv("RANDOMMER_API")

class Fun(commands.Cog):
    """
    Have some fun!
    """
    
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

    @commands.command()
    @commands.guild_only()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    async def someone(self, ctx):
        role = nextcord.utils.get(ctx.guild.roles, name="someone")
        if not role:
            role = await ctx.guild.create_role(name="someone", reason="Ping someone!")
            random_member = random.choice(ctx.guild.humans)
            await random_member.add_roles(role)
            await ctx.send("@someone setup successful! You can now ping @someone to ping a random human.")
            return 0
        return await ctx.send("@someone is already settled up!")


def setup(bot):
    bot.add_cog(Fun(bot))
