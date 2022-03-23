import nextcord.ext
from nextcord.ext import commands

class ModVC(commands.Cog):
    """
    Moderation commands related to voice channels.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Voice mute a member.")
    @commands.check_any(commands.is_owner(),
        commands.has_guild_permissions(mute_members=True))
    @commands.guild_only()
    async def vcmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Voice mute a member so that they cannot talk in a voice channel anymore.
        """ 
        await member.edit(mute=True, reason=reason)
        await ctx.reply(f"{member} has been successfully voice-muted by {ctx.author.mention} with reason '{reason}'")


    @commands.command(brief="Voice unmute a member.")
    @commands.check_any(commands.is_owner(),
        commands.has_guild_permissions(mute_members=True))
    @commands.guild_only()
    async def vcunmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Voice unmute a member so that they can talk in a voice channel again.
        """
        await member.edit(mute=False, reason=reason)
        await ctx.reply(f"{member} has been successfully voice-unmuted by {ctx.author.mention} with reason '{reason}'")


    @commands.command()
    @commands.check_any(commands.is_owner(), 
        commands.has_guild_permissions(deafen_members=True))
    @commands.guild_only()
    async def deafen(self, ctx, member: nextcord.Member, reason=None):
        """
        Deafen a member so that they cannot hear anything in a voice channel.
        """
        await member.edit(deafen=True, reason=reason)
        await ctx.reply(f"{ctx.author.mention} has been deafened by {ctx.author.mention} with reason '{reason}.'")


    @commands.command()
    @commands.check_any(commands.is_owner(), 
        commands.has_guild_permissions(deafen_members=True))
    @commands.guild_only()
    async def undeafen(self, ctx, member: nextcord.Member, reason=None):
        """
        Undeafen a member so that they can hear in a voice channel again.
        """
        await member.edit(deafen=False, reason=reason)
        await ctx.reply(f"{ctx.author.mention} has been undeafened by {ctx.author.mention} with reason '{reason}.'")


def setup(bot):
    bot.add_cog(ModVC(bot))