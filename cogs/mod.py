import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks

bot = commands.Bot(command_prefix = '-')

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def addrole(ctx, user: nextcord.Member, roles: nextcord.Role):
		await bot.add_roles(member, roles)
		await ctx.send(f"{user.name} has been given role(s) {role.name} by {ctx.author.name}")

def setup(bot):
	bot.add_cog(Mod(bot))
