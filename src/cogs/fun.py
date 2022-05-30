import os
import json
import aiohttp
import random
from pprint import pprint
import nextcord
from nextcord.ext import commands, application_checks
import nextcord.utils
import _helper as hp


class Fun(commands.Cog):
    """
    Have some fun!
    """

    def __init__(
        self,
        bot
    ):
        self.bot = bot

    @nextcord.slash_command()
    async def jotd(
        self,
        interaction: nextcord.Interaction
    ):
        """
        Get joke of the day using jokes.one API.
        """
        headers = {'content-type': 'application/json',
                   'X-JokesOne-Api-Secret': ""
                   }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.jokes.one/jod?category=knock-knock", headers=headers) as response:
                response_json = await response.json()
                try:
                    jokes = response_json["contents"]["jokes"][0]["joke"]
                except KeyError:
                    return await interaction.send(response_json["error"]["message"])
                print(jokes)
                embed = nextcord.Embed(
                    title=jokes["title"],
                    colour=nextcord.Colour.green()
                )
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.display_avatar
            )
            embed.description = f"{jokes['text']}\n-----\nProvided by https://jokes.one"
            await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def name(
        self,
        interaction: nextcord.Interaction
    ):
        """
        Main command for other name subcommands.
        """
        pass

    @name.subcommand()
    async def fullname(
        self,
        interaction: nextcord.Interaction
    ):
        """
        Get a random fullname using randommer API.
        """
        name = await hp.request_randommer_name("fullname")
        await interaction.send(name)

    @name.subcommand()
    async def firstname(
        self,
        interaction: nextcord.Interaction
    ):
        """
        Get a random firstname using randommer API.
        """
        name = await hp.request_randommer_name("firstname")
        await interaction.send(name)

    @name.subcommand()
    async def surname(
        self,
        interaction: nextcord.Interaction
    ):
        """
        Get a random surname using randommer API.
        """
        name = await hp.request_randommer_name("surname")
        await interaction.send(name)

    @nextcord.slash_command()
    @application_checks.guild_only()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
    )
    async def someone(
        self,
        interaction: nextcord.Interaction
    ):
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
