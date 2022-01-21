import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks

bot = commands.Bot(command_prefix = '-')

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def addrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
		await member.add_roles(roles)
		await ctx.send(f"{member.mention} has been given role(s) {roles.name}({roles.id}) by {ctx.author.mention}")
	
	@commands.command(pass_context=True)
	async def rmrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
		await member.remove_roles(roles)
		await ctx.send(f"{member.mention} has been removed from {roles.name}({roles.id}) role(s) by {ctx.author.mention}")
		
	@commands.command(pass_context=True)
	async def kick(self, ctx, member: nextcord.Member, *, reason=None):
		await ctx.guild.kick(user=member, reason=reason)
		await ctx.send(f'User {member}) has kicked by {ctx.author.mention} with reason "{reason}".')
	
	
def setup(bot):
	bot.add_cog(Mod(bot))
