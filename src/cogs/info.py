import nextcord.ext
import nextcord.utils
from nextcord.ext import commands
from afks import afks

class Info(commands.Cog):
    """
    Get information about stuff.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Get the latency of the bot.
        """

        await ctx.send(f'Pong! {round (self.bot.latency * 1000)} ms')


    @commands.command()
    async def sayhi(self, ctx):
        """
        Say hello and tell the prefix.
        """

        await ctx.send(f"Hello {ctx.author.mention}! My prefix is '-'.")


    @commands.command()
    async def userinfo(self, ctx, member: nextcord.Member=None):
        """
        Get information about a member.
        """

        member = member or ctx.author
        embed = nextcord.Embed(
            title=f"UserInfo of {member}",
            colour=nextcord.Colour.green())
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar)
        embed.description = (f"""
        Avatar: {member.display_avatar.url}
        Banner: {member.banner}
        Display Name: {member.display_name}
        ID: {member.id}
        Colour: {member.colour}
        Bot: {member.bot}
        Discord Representative: {member.system}
        Created at: {member.created_at}
        Joined at: {member.joined_at}
        In Voice: {member.voice}
        Boosting Since: {member.premium_since}
        Timeout: {member.timeout}
        Top Role: {member.top_role}
        """)
        await ctx.send(embed=embed)


    @commands.command()
    async def guildinfo(self, ctx):
        """
        Get information about the guild.
        """

        humans = 0
        bots = 0

        for human in ctx.guild.humans:
            humans += 1

        for bot in ctx.guild.bots:
            bots += 1

        embed = nextcord.Embed(
            title=f"Guild info of {ctx.guild.name}",
            colour=nextcord.Colour.green())
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar)
        embed.description = (f"""
                                 Icon: {ctx.guild.icon}
                                 Banner: {ctx.guild.banner}
                                 Name: {ctx.guild.name}
                                 Owner: {ctx.guild.owner}
                                 Members: {ctx.guild.member_count}
                                 Humans: {humans}
                                 Bots: {bots}
                                 Created At: {ctx.guild.created_at}
                                 Verification Level: {ctx.guild.verification_level}
                                 """)
        await ctx.send(embed=embed)


    @commands.command()
    async def emojiinfo(self, ctx, emoji: nextcord.Emoji):
        """
        Get information about a emoji.
        """

        embed = nextcord.Embed(
            title=f"Info of {emoji}",
            colour=nextcord.Colour.green())
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar)
        embed.description = (f"""
                          Name: {emoji.name}
                          Uploaded by: {emoji.user}
                          Animated: {emoji.animated}
                          Managed by Twitch Intergration: {emoji.managed}
                          URL: {emoji.url}
                          """)
        await ctx.send(embed=embed)


    @commands.command()
    async def inviteinfo(self, ctx, invite: nextcord.Invite):
        """
        Get information about a invite.
        """

        embed = nextcord.Embed(
            title=f"Info of {invite}",
            colour=nextcord.Colour.green())
        #embed.set_author(name = ctx.bot.user, icon_url = ctx.bot.user.display_avatar)
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar)
        embed.description = (f"""
                             Code: {invite.code}
                             ID: {invite.id}
                             Channel: {invite.channel}
                             Guild: {invite.guild}
                             Uses: {invite.uses}
                             Temporary: {invite.temporary}
                             Expires At: {invite.expires_at}
                             """)
        await ctx.send(embed=embed)


    @commands.command()
    async def afk(self, ctx, *, reason = "Not provided."):
        """
        Go afk and optionally provide a reason.
        """
        member = ctx.author
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick = f"(AFK) {member.display_name}")

            except:
                pass
              
        afks[member.id] = reason
        embed = nextcord.Embed(title=":zzz: Member AFK", description=f"{member} is AFK right now.", color=member.color)
        embed.set_thumbnail(url = member.display_avatar)
        embed.add_field(name="AFK Note: ", value=reason)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
