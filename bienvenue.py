from discord.ext import commands
from discord.utils import get
import discord
import datetime


class Bienvenue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        emoji = get(member.guild.emojis, name='disboat')
        embed = discord.Embed(
            title=f"{member.guild.name}",
            color=0xa90450,
            description=f"**{emoji} | {member.name}** a rejoint le discord ! \n\n"
                        f"Le **Discord** compte désormais **{member.guild.member_count}** membres !")
        embed.set_footer(text=f"{member.guild.name}",
                         icon_url="https://media.discordapp.net/attachments/722196449294811167/772228421941329920/disboat.jpg")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        channel = self.bot.get_channel(772234256814440479)
        await channel.send(embed=embed)
        rolee = discord.utils.get(member.guild.roles, name="Non vérifié")
        await member.add_roles(rolee)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "discord.gg" in message.content.lower():
            await message.delete()
            await message.channel.send("La publicité est interdite sur le discord ! ")
