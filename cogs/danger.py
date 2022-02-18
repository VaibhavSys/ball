import nextcord
import nextcord.ext
import nextcord.utils
from nextcord.ext import commands, tasks

class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.red)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Confirming...', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.green)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Cancelling...', ephemeral=True)
        self.value = False
        self.stop()

class Danger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        view = Confirm()
        await ctx.send("NOTE: The bot's role should be on top to cause maximum damage!")
        await ctx.send("Are you sure that you want delete all channels in this server?", view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Timed out!")
        elif view.value:
            await ctx.send("Nuking server...")
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()

                except:
                    await ctx.send(f"Unable to delete {channel.name}!")
        else:
            await ctx.send("Cancelled.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke_roles(self, ctx):
        view = Confirm()
        await ctx.send("NOTE: The bot's role should be on top to cause maximum damage!")
        await ctx.send("Are you sure that you want to delete all roles in this guild?", view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Timed out!")
        elif view.value:
            await ctx.send("Nuking roles...")
            for role in ctx.guild.roles:
                try:
                    await role.delete()

                except:
                    await ctx.send(f"Unable to delete {role.name}!")
        else:
            await ctx.send("Cancelled.")

def setup(bot):
    bot.add_cog(Danger(bot))
