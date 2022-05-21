import nextcord
import nextcord.ext
from nextcord.ext import commands, application_checks
import _helper as hp

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        """
        Error handling for the most common errors.
        """
        if isinstance(error, application_checks.errors.ApplicationMissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions", colour=nextcord.Colour.red())
            embed.description = "You do not have required permission(s) to execute this command."
            for permission in hp.parse_permissions_human(error.missing_permissions):
                embed.add_field(name="Missing Permission", value=permission)
            await interaction.send(embed=embed)


        elif isinstance(error, application_checks.errors.ApplicationCheckAnyFailure):
            errors = error.errors
            missing_permissions_errors = []
            missing_role_errors = []
            missing_permissions = []
            missing_roles = []

            for error in errors:
                if isinstance(error, application_checks.errors.ApplicationMissingPermissions):
                    missing_permissions_errors.append(error)
                elif isinstance(error, application_checks.errors.ApplicationMissingRole):
                    missing_role_errors.append(error)

            embed = nextcord.Embed(title="Missing Requirements", colour=nextcord.Colour.red())
            embed.description = "You do not meet the requirements to execute this command."

            if len(missing_permissions_errors) > 0:
                for error in missing_permissions_errors:
                    missing_permissions.append(error.missing_permissions[0])
                missing_permissions = hp.parse_permissions_human(missing_permissions)
            
            if len(missing_permissions_errors) > 0:
                for error in missing_role_errors:
                    missing_roles.append(error.missing_role)

            if len(missing_permissions_errors) > 0:
                for permission in missing_permissions:
                    embed.add_field(name="Missing Permission", value=permission)

            if len(missing_role_errors) > 0:
                for role in missing_roles:
                    embed.add_field(name="Missing Role", value=role)
            await interaction.send(embed=embed)


        elif isinstance(error, application_checks.ApplicationPrivateMessageOnly):
            embed = nextcord.Embed(title="DM Only Command", colour=nextcord.Colour.red())
            embed.description = "This command can only be used in private messages."
            await interaction.send(embed=embed)


        elif isinstance(error, application_checks.ApplicationNoPrivateMessage):
            embed = nextcord.Embed(title="Not allowed in DMs", colour=nextcord.Colour.red())
            embed.description = "This command can not be used in private messages."
            await interaction.send(embed=embed)


        elif isinstance(error, application_checks.ApplicationBotMissingPermissions):
            embed = nextcord.Embed(title="Bot Lacking Permissions", colour=nextcord.Colour.red())
            embed.description = "I do not have enough permission(s) to execute this command."
            for permission in hp.parse_permissions_human(error.missing_permissions):
                embed.add_field(name="Missing Permission", value=permission)
            await interaction.send(embed=embed)
            
        else:
            await interaction.send(f"An unexpected error has occurred, please report it to the developer.\nError:\n```py\n{error}\n```")
            raise(error)


def setup(bot):
    bot.add_cog(Errors(bot))