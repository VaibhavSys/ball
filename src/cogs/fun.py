import nextcord.ext
from nextcord.ext import commands, application_checks
import os
import json
import requests
import random
import nextcord.utils
import _helper as hp
import nextcord


class Fun(commands.Cog):
    """
    Have some fun!
    """
    
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def jotd(self, interaction: nextcord.Interaction):
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
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar)
        embed.description = (f"""
        {jokes['joke']['text']}
        ----
        Joke provided by https://jokes.one/
        """)
        await interaction.send(embed=embed)


    @nextcord.slash_command()
    async def rfullname(self, interaction: nextcord.Interaction):
        """
        Get a random fullname using randommer API.
        """

        headers = {
            'accept': '*/*',
            'X-Api-Key': hp.RANDOMMER_API,
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
        await interaction.send(respsend)


    @nextcord.slash_command()
    async def rfirstname(self, interaction: nextcord.Interaction):
        """
        Get a random firstname using randommer API.
        """

        headers = {
            'accept': '*/*',
            'X-Api-Key': hp.RANDOMMER_API,
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
        await interaction.send(respsend)


    @nextcord.slash_command()
    async def rsurname(self, interaction: nextcord.Interaction):
        """
        Get a random surname using randommer API.
        """

        headers = {
            'accept': '*/*',
            'X-Api-Key': hp.RANDOMMER_API,
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
        await interaction.send(respsend)


    @nextcord.slash_command()
    @application_checks.guild_only()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    async def someone(self, interaction: nextcord.Interaction):
        """
        Setup a role named 'someone' which randomly pings a human member.
        """
        role = nextcord.utils.get(interaction.guild.roles, name="someone")
        if not role:
            role = await interaction.guild.create_role(name="someone", reason="Ping someone!")
            random_member = random.choice(interaction.guild.humans)
            await random_member.add_roles(role)
            await interaction.send(f"{role.mention} setup successful! You can now ping {role.mention} to ping a random human.")
            return 0
        return await interaction.send(f"{role.mention} is already settled up!")


def setup(bot):
    bot.add_cog(Fun(bot))
