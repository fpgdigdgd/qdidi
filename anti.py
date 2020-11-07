import discord
import json
import numpy as np
import random
import string
import Augmentor
import os
import shutil
import asyncio
import time

from discord.ext import commands
from discord.utils import get

from datetime import datetime
from random import choice
from PIL import ImageFont, ImageDraw, Image


# ------------------------ COGS ------------------------ #

class OnJoinCog(commands.Cog, name="on join"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if (member.bot):
            return

        # Read configuration.json
        with open("configuration.json", "r") as config:
            data = json.load(config)
            logChannel = self.bot.get_channel(data["logChannel"])

        # Check the user account creation date (1 day by default)
        userAccountDate = member.created_at.timestamp()
        if userAccountDate < data["minAccountDate"]:
            minAccountDate = data["minAccountDate"] / 3600
            embed = discord.Embed(title=f"**Vous avez été kick de  {member.guild.name}**",
                                  description=f"Raison : Votre compte est récent.",
                                  color=0xa90450)
            await member.send(embed=embed)
            await member.kick()

        if data["captcha"] == True:

            # Give temporary role
            try:
                getrole = get(member.guild.roles, id=data["temporaryRole"])
                await member.add_roles(getrole)
            except:
                pass

        # Create captcha
        image = np.zeros(shape=(100, 350, 3), dtype=np.uint8)

        # Create image
        image = Image.fromarray(image + 255)  # +255 : black to white

        # Add text
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font="arial", size=60)

        text = ' '.join(
            random.choice(string.ascii_uppercase) for _ in range(6))  # + string.ascii_lowercase + string.digits

        # Center the text
        W, H = (350, 100)
        w, h = draw.textsize(text, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(90, 90, 90))

        # Save
        ID = member.id
        folderPath = f"captchaFolder/captcha_{ID}"
        try:
            os.mkdir(folderPath)
        except:
            if os.path.isdir('captchaFolder') == False:
                os.mkdir("captchaFolder")
            if os.path.isdir(folderPath) == True:
                shutil.rmtree(folderPath)
            os.mkdir(folderPath)
        image.save(f"{folderPath}/captcha{ID}.png")

        # Deform
        p = Augmentor.Pipeline(folderPath)
        p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=14)
        p.process()

        # Search file in folder
        path = f"{folderPath}/output"
        files = os.listdir(path)
        captchaName = [i for i in files if i.endswith('.png')]
        captchaName = captchaName[0]

        image = Image.open(f"{folderPath}/output/{captchaName}")



        # Add noise
        noisePercentage = 0.1  # 25%

        pixels = image.load()  # create the pixel map
        for i in range(image.size[0]):  # for every pixel:
            for j in range(image.size[1]):
                rdn = random.random()  # Give a random %
                if rdn < noisePercentage:
                    pixels[i, j] = (90, 90, 90)

        # Save
        image.save(f"{folderPath}/output/{captchaName}_2.png")

        # Send captcha
        channelToSendCaptcha = self.bot.get_channel(774720754171248670)

        captchaFile = discord.File(f"{folderPath}/output/{captchaName}_2.png")
        captchaEmbed = await channelToSendCaptcha.send(
            f"**{member.mention} Vous devez passer la vérification pour avoir accès au serveur :**",
            file=captchaFile)

        try:
            shutil.rmtree(folderPath)
        except:
            pass

            # Check if it is the right user

        def check(message):
            if message.author == member:
                return message.content

        try:
            msg = await self.bot.wait_for('message', timeout=120.0, check=check)
            # Check the captcha
            password = text.split(" ")
            password = "".join(password)
            if msg.content == password:
                embed = discord.Embed(description=f"{member.mention} a passé la vérification.", color=0xa90450)  # Green
                await channelToSendCaptcha.send(embed=embed, delete_after=5)
                # Give and remove roles
                try:
                    getrole = discord.utils.get(member.guild.roles, name="Membres")
                    getroleee = discord.utils.get(member.guild.roles, name="Non vérifié")
                    if getrole != False:
                        await member.add_roles(getrole)
                        await member.remove_roles(getroleee)
                except:
                    pass

                await captchaEmbed.delete()
                await msg.delete()

            else:
                embed = discord.Embed(description=f"{member.mention} a rentré un mauvais Captcha", color=0xa90450)  # Red
                await channelToSendCaptcha.send(embed=embed, delete_after=5)
                embed = discord.Embed(title=f"*Vous avez été kick de {member.guild.name}**",
                                      description=f"Raison : Mauvais Captcha.", color=0xa90450)
                await member.send(embed=embed)
                await member.kick()  # Kick the user
                await captchaEmbed.delete()
                await msg.delete()

        except (asyncio.TimeoutError):
            embed = discord.Embed(title=f"**{member.mention} a mit trop de temps pour répondre au captcha.**",
                                  color=0xa90450)
            await channelToSendCaptcha.send(embed=embed, delete_after=5)
            try:
                embed = discord.Embed(title=f"*Vous avez été kick de {member.guild.name}**",
                                      description=f"Raison : Mauvais Captcha.", color=0xa90450)
                await member.send(embed=embed)
                await member.kick()  # Kick the user
            except:
                pass
            await captchaEmbed.delete()
