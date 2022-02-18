import nextcord
import nextcord.ext
import nextcord.utils
from nextcord.ext import commands, tasks

class ModEvents(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_guild_channel_create(self, ctx):
		for channel in ctx.guild.channels:
			muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
			await channel.set_permissions(muted, send_messages=False)
	
def setup(bot):
	bot.add_cog(ModEvents(bot))
