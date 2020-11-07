import discord
from discord.ext import commands
import asyncio
from discord.utils import get


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tic(self, ctx):
        emo = get(ctx.guild.emojis, name='disboat')
        embed = discord.Embed(title="AzBot - Commissions",
                              color=0xa90450,
                              description=f"Pour prendre **commande**, réagissez avec **l'emoji** {emo} juste en dessous.")

        me = await ctx.send(embed=embed)
        await me.add_reaction(emo)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        member = payload.member
        if message_id == 772440628541259779:
            guild_id = payload.guild_id
            role = discord.utils.get(member.guild.roles, name='Manager')
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            channel = self.bot.get_channel(payload.channel_id)
            user = guild.get_member(payload.user_id)
            emoji = payload.emoji
            m = await channel.fetch_message(message_id)
            cat = discord.utils.get(guild.channels, id=772273135721644072)
            ticket_chan = await guild.create_text_channel(name=f"Commande de {member.name}", category=cat)
            await m.remove_reaction(emoji, user)
            pin = await ticket_chan.send({role.mention})
            await pin.delete()

            p = discord.utils.get(member.guild.roles, name='Membres')
            await ticket_chan.set_permissions(member, send_messages=True, read_messages=True)
            await ticket_chan.set_permissions(p, send_messages=False, read_messages=False)
            embed = discord.Embed(
                color=0xa90450,
                title=f"**Salut {member.name} !**",
                description=f"Un membre de l'équipe devrait arriver sous peu."
            )
            embed.set_footer(text="!close pour fermer ce ticket.")
            await ticket_chan.send(embed=embed)
            await m.remove_reaction(emoji, user)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def close(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "oui"

        try:

            em = discord.Embed(title="AzBot - Commissions",
                               description="Répondez par **oui** si vous voulez vraiment fermer ce ticket",
                               color=0xa90450)

            await ctx.send(embed=em)
            await self.bot.wait_for('message', check=check, timeout=30)
            await ctx.channel.delete()

        except asyncio.TimeoutError:
            em = discord.Embed(title="AzBot - Commissions",
                               description="Vous avez mis trop de temps pour fermer le ticket, réesayer par "
                                           "**!close**",
                               color=0xa90450)
            await ctx.send(embed=em)
