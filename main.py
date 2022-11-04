import discord
import os
import time
from bs4 import BeautifulSoup
import requests
import random
import re
from discord.ext import tasks


client = discord.Client(intents=discord.Intents.all())
ch = None




def get_image():
    link = "http://catgirldatabase.com/picture.php?/{}/category/1".format(random.randint(0, 4260))
    a = requests.get(link).text
    soup = BeautifulSoup(a, 'html.parser')

    #ToDo if madis watches too many cat images there might be index out of range error for some reason (Error produced by line 23)
    text = str(soup.find_all('img')[0])
    s = re.search('src="(.*)" title', text).group(1)

    url = "http://catgirldatabase.com/" + s
    x = discord.Embed()
    x.set_image(url=url)
    x.set_footer(text=link)
    return x


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global ch
    if message.author == client.user:
        return

    if message.content == "Hello":
        await message.channel.send("Hello master " + message.author.nick)

    if message.content == "modis":
        await message.channel.send("https://images-ext-2.discordapp.net/external/MtBpNZXySNvNWM1Ssk_o2zpLrdyw_HPGuX7BVUFSyj0/https/cdn.weeb.sh/images/rkmBhAuD-.gif")

    if message.content == "start":

        ch = message.channel
        catgirl.start()

    if message.content == "stop":
        ch = message.channel
        catgirl.cancel()

    if message.content == "catgirl":
        await message.channel.send(embed=get_image())
        return

@tasks.loop(seconds = 5)
async def catgirl():
    await ch.send(embed=get_image())



client.run("MzUxMzM2MTk0OTY3MDc2ODY0.GdvZD6.EeU8chS1boc6_CtZyrweXua__K1c_iC6Am5FuE")
