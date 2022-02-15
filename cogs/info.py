import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round (self.bot.latency * 1000)} ms')
        
    @commands.command()
    async def userinfo(self, ctx, member: nextcord.Member):
        embed = nextcord.Embed(title = f"UserInfo of {member}")
        embed.set_author(name = "Pengoon", url=nextcord.Embed.Empty, icon_url=self.bot.user.display_avatar)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        embed.description = (f"""
        Avatar: {member.display_avatar.url}
        Guild Avatar: {member.guild_avatar}
        Banner: {member.banner}
        Name: {member.name}
        Discriminator: {member.discriminator}
        Display Name: {member.display_name}
        Nick: {member.nick}
        Mention: {member.mention}
        ID: {member.id}
        Colour: {member.colour}
        Bot: {member.bot}
        Discord Representative: {member.system}
        Created at: {member.created_at}
        Joined at: {member.joined_at}
        Desktop: {member.desktop_status}
        Web: {member.web_status}
        Mobile: {member.mobile_status}
        On Mobile: {member.is_on_mobile()}
        In Voice: {member.voice}
        Status: {member.status}
        Raw Status: {member.raw_status}
        Actvity: {member.activity}
        Activities: {member.activities}
        Boosting Since: {member.premium_since}
        Timeout: {member.timeout}
        Top Role: {member.top_role}
        Guild Roles: {member.roles}
        Guild Permissions: {member.guild_permissions}
        """)
        await ctx.send(embed=embed)
                        
def setup(bot):
    bot.add_cog(Info(bot))
