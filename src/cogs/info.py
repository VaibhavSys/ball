import nextcord.ext
import nextcord.utils
from nextcord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Latency of bot", description="Latency of bot")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round (self.bot.latency * 1000)} ms')

    @commands.command(brief="Say hello and tell the prefix", description="Say hello and tell the prefix")
    async def sayhi(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}! My prefix is '-'.")

    @commands.command(brief="Information about a user", description="Information about a user")
    async def userinfo(self, ctx, member: nextcord.Member):
        embed = nextcord.Embed(title = f"UserInfo of {member}", colour=nextcord.Colour.green())
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar)
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

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Missing argument: member")

    @commands.command(brief="Information about the current guild", description="Information about the current guild")
    async def guildinfo(self, ctx):
        humans = 0
        bots = 0

        for human in ctx.guild.humans:
            humans += 1

        for bot in ctx.guild.bots:
            bots += 1

        embed = nextcord.Embed(title = f"Guild info of {ctx.guild.name}", colour=nextcord.Colour.green())
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar)
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

    @commands.command(brief="Information about a emoji", description="Information about a emoji")
    async def emojiinfo(self, ctx, emoji: nextcord.Emoji):
        embed = nextcord.Embed(title = f"Info of {emoji}", colour=nextcord.Colour.green())
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar)
        embed.description = (f"""
                          Name: {emoji.name}
                          Uploaded by: {emoji.user}
                          Animated: {emoji.animated}
                          Managed by Twitch Intergration: {emoji.managed}
                          URL: {emoji.url}
                          """)
        await ctx.send(embed=embed)

    @emojiinfo.error
    async def emojiinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Missing argument: emoji")

    @commands.command(brief="Information about a invite", description="Information about a invite")
    async def inviteinfo(self, ctx, invite: nextcord.Invite):
        embed = nextcord.Embed(title = f"Info of {invite}", colour=nextcord.Colour.green())
        #embed.set_author(name = ctx.bot.user, icon_url = ctx.bot.user.display_avatar)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar)
        embed.description = (f"""
                             Code: {invite.code}
                             ID: {invite.id}
                             Inviter: {invite.inviter}
                             Channel: {invite.channel}
                             Guild: {invite.guild}
                             Uses: {invite.uses}
                             Temporary: {invite.temporary}
                             Expires At: {invite.expires_at}
                             """)
        await ctx.send(embed=embed)

    @inviteinfo.error
    async def inviteinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Missing argument: invite")

def setup(bot):
    bot.add_cog(Info(bot))
