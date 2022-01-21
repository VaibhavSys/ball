import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks

bot = commands.Bot(command_prefix = '-')

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.has_permissions(manage_roles=True)
	async def addrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
		await member.add_roles(roles)
		await ctx.send(f"{member.mention} has been given role(s) {roles.name}({roles.id}) by {ctx.author.mention}")
	
	@commands.command(pass_context=True)
	@commands.has_permissions(manage_roles=True)
	async def rmrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
		await member.remove_roles(roles)
		await ctx.send(f"{member.mention} has been removed from {roles.name}({roles.id}) role(s) by {ctx.author.mention}")
		
	@commands.command(pass_context=True)
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: nextcord.Member, *, reason=None):
		await ctx.guild.kick(user=member, reason=reason)
		await ctx.send(f"User {member}({member.id})) has kicked by {ctx.author.mention} with reason '{reason}''.")
	
	@commands.command(pass_context=True)
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member : nextcord.Member, *, reason=None):
		await member.ban(reason=reason)
		await ctx.send(f"{member} has been banned by {ctx.author.mention} with reason '{reason}'.")
		
	@commands.command(pass_context=True)
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, *, member, reason=None):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split("#")

		for ban_entry in banned_users:
			user = ban_entry.user

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user, reason=reason)
				await ctx.send(f"{user.name}#{user.discriminator} has been unbanned by {ctx.author.mention} with reason '{reason}'")

	
def setup(bot):
	bot.add_cog(Mod(bot))
