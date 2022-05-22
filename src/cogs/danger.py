import nextcord
from nextcord import Interaction
from nextcord.ext import commands, application_checks
import nextcord.utils


class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their
    # choice.
    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.red)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('The action is being confirmed...', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner
    # value to `False`
    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.green)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('The action is being cancelled...', ephemeral=True)
        self.value = False
        self.stop()


class Danger(commands.Cog):
    """
    Dangerous commands! Use with caution!
    """

    def __init__(self, bot):
        self.bot = bot
        self.rnote = "NOTE: Make sure that the bot's role is the top role to cause maximum damage!"
        self.tmsg = "Timed out!"


    @nextcord.slash_command()
    @application_checks.guild_only()
    async def nuke(
        self,
        interaction: nextcord.Interaction
        ):
        """
        The main command which contains other nuke commands.
        """
        pass


    @nuke.subcommand()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(administrator=True)
        )
    async def channels(
        self,
        interaction: nextcord.Interaction
        ):
        """
        Deletes all channels in the guild.
        """
        view = Confirm()

        await interaction.send(f"{self.rnote}\nAre you sure that you want to delete all channels in this guild?", view=view)
        await view.wait()

        if view.value is None:
            await interaction.send(self.tmsg)
        elif view.value:
            await interaction.send("Nuking channels...")
            for channel in interaction.guild.channels:
                try:
                    await channel.delete()
                    await asyncio.sleep(2)

                except nextcord.Forbidden:
                    await interaction.send(f"Unable to delete {channel.name} due to insufficient permissions!")
        else:
            await interaction.send("Action cancelled successfully.")


    @nuke.subcommand()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(administrator=True)
        )
    async def roles(
        self,
        interaction: nextcord.Interaction
        ):
        """
        Deletes all roles in guild.
        """
        view = Confirm()
        await interaction.send(f"{self.rnote}\nAre you sure that you want to delete all roles in this guild?", view=view)
        await view.wait()

        if view.value is None:
            await interaction.send(self.tmsg)
        elif view.value:
            await interaction.send("Nuking roles...")
            for role in interaction.guild.roles:
                if role != interaction.guild.default_role:
                    try:
                        await role.delete()
                        await asyncio.sleep(2)

                    except nextcord.Forbidden:
                        await interaction.send(f"Unable to delete {role.mention} due to insufficient permissions!")
        else:
            await interaction.send("Action cancelled successfully.")

    @nuke.subcommand()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(administrator=True)
        )
    async def emojis(
        self,
        interaction: nextcord.Interaction
        ):
        """
        Deletes all emojis in guild.
        """
        view = Confirm()
        await interaction.send(f"{self.rnote}\nAre you sure that you want to delete all emojis in this guild?", view=view)
        await view.wait()

        if view.value is None:
            await interaction.send(self.tmsg)
        elif view.value:
            await interaction.send("Nuking emojis...")
            for emoji in interaction.guild.emojis:
                try:
                    await emoji.delete()
                    await asyncio.sleep(2)

                except nextcord.Forbidden:
                    await interaction.send(f"Unable to delete {emoji} due to insufficient permissions!")
        else:
            await interaction.send("Action cancelled successfully.")


    @nuke.subcommand()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(administrator=True)
        )
    async def members(
        self,
        interaction: nextcord.Interaction
        ):
        """
        Kicks all members in the guild.
        """
        view = Confirm()
        await interaction.send(f"{self.rnote}\nAre you sure that you want to kick all members in this guild?", view=view)
        await view.wait()

        if view.value is None:
            await interaction.send(self.tmsg)
        elif view.value:
            for member in interaction.guild.members:
                try:
                    await interaction.guild.kick(user=member, reason=f"{interaction.user} ({interaction.user.id}) issued nuke members command.")
                    await asyncio.sleep(2)
                    
                except:
                    await interaction.send(f"Unable to kick {member} due to insufficient permissions!")
        else:
            await interaction.send("Action cancelled successfully.")


def setup(bot):
    bot.add_cog(Danger(bot))
