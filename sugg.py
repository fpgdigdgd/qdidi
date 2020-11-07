import discord
from discord.ext import commands
import datetime
from discord.utils import get


class Suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 772268698597457920:
            bot = message.author
            if bot.id == 772230138204913715:
                pass
            else:
                m = message
                emoji = get(message.guild.emojis, name='disboat')
                embed = discord.Embed(
                    description=f"{emoji} ** |  AzBot - Suggestions** \n\n"
                                f"**__Pseudo__** : {message.author.mention} \n\n"
                                f"**__Suggestion__** : {message.content} \n\n"
                                f"__(Pour réagir à cette suggestion, veuillez ajouter une des réactions ci-dessous.)__",
                    color=0xa90450
                )
                embed.set_footer(text="Posté ",
                                 icon_url="https://media.discordapp.net/attachments/722196449294811167/772228421941329920/disboat.jpg")
                embed.timestamp = datetime.datetime.utcnow()
                await message.delete()
                me = await m.channel.send(embed=embed)
                await me.add_reaction("<:tick_green:768939462112706560>")
                await me.add_reaction("<:tick_red:768939475060785184>")
