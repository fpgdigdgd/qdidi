import discord
from discord.ext import commands
import bienvenue, sugg, ticket, anti

bot = commands.Bot(command_prefix="!", description="AzBot", intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Bot en ligne")
    await bot.change_presence(activity=discord.Game("AzBot - Commissions"))

bot.add_cog(bienvenue.Bienvenue(bot))
bot.add_cog(sugg.Suggestion(bot))
bot.add_cog(ticket.Ticket(bot))
bot.add_cog(anti.OnJoinCog(bot))
bot.run("NzcyMjMwMTM4MjA0OTEzNzE1.X53pXA.fbZ_8Q1VkKVyT8j4Oe8L-xF5x10")
