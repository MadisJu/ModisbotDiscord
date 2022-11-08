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

    #ToDo if madis watches too many cat images tere might be index out of range error for some reason
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

    if message.content == "modis" or message.content == '@Modis':
        await message.channel.send('https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')

    if message.content == "start":

        ch = message.channel
        catgirl.start()

    if message.content == "stop" or message.content == "This nonsense needs to end!":
        ch = message.channel
        catgirl.cancel()
        await message.channel.send("The catgirls have been imprisoned (end)")

@tasks.loop(seconds = 5)
async def catgirl():
    randomNumber = 0 #random.randint(0, 10) while not in tartu ylikool
    if randomNumber == 0:
        await ch.send(
            'https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')
    else:
        await ch.send(embed=get_image())



client.run("MzUxMzM2MTk0OTY3MDc2ODY0.GdvZD6.EeU8chS1boc6_CtZyrweXua__K1c_iC6Am5FuE")
