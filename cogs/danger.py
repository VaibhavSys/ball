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

    rnote = "NOTE: Make sure that the bot's role is the top role to cause maximum damage!"

    @commands.command(brief = "Deletes all channels in guild")
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        view = Confirm()
        await ctx.send(Danger.rnote)
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

    @commands.command(brief = "Deletes all roles in guild")
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

    @commands.command(brief = "Deletes all emojis in guild")
    @commands.has_permissions(administrator=True)
    async def nuke_emojis(self, ctx):
        view = Confirm()
        await ctx.send(Danger.rnote)
        await ctx.send("Are you sure that you want to delete all emojis in this guild?", view=view)
        await view.wait()

        if view.value is None:
            await ctx.send(Danger.tmsg)
        elif view.value:
            await ctx.send("Nuking emojis...")
            for emoji in ctx.guild.emojis:
                try:
                    await ctx.guild.delete_emoji(emoji, reason = f"NukeEmojis command issued by {ctx.author.name}")

                except:
                    await ctx.send(f"Unable to delete {emoji}!")
        else:
            await ctx.send("Cancelled.")

    @commands.command(brief = "Kicks all members in guild", description = "Kicks all members in guild")
    @commands.has_permissions(administrator=True)
    async def kickall(self, ctx):
        for member.member in ctx.guild.fetch_members(limit=None):
            try:
            #await ctx.send(ctx.guild.members)
                #await ctx.send(ctx.guild.fetch_members(limit=None))
                await ctx.guild.kick(user=member)
            except:
                await ctx.send(f"Unable to kick {member}")

def setup(bot):
    bot.add_cog(Danger(bot))
