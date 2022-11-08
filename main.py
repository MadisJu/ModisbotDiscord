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

importantList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u'
    , 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

specialWords = ['cunt', 'stop', 'start']

list2 = 'qwertyuiopasdfghjklzxcvbnmüõö ä1234567890!@#$%^&*()[]{};:'"<>,./?\|"

def get_image():
    link = "http://catgirldatabase.com/picture.php?/{}/category/1".format(random.randint(0, 4260))
    a = requests.get(link).text
    soup = BeautifulSoup(a, 'html.parser')

    # ToDo if madis watches too many cat images tere might be index out of range error for some reason
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
    global ch, loopTime
    if message.author == client.user:
        return

    if message.content == "Hello":
        await message.channel.send("Hello master " + message.author.nick)

    if message.content == "modis" or message.content == '@Modis':
        await message.channel.send(
            'https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')

    if message.content == "start":
        ch = message.channel
        catgirl.start()

    if message.content == "stop":
        ch = message.channel
        await message.channel.send("LMAO *sToP*, there is no end to modis!")

    if message.content == "This nonsense needs to end!":
        ch = message.channel
        catgirl.cancel()
        await message.channel.send("The catgirls have been imprisoned (end)")
    try:
        if message.content[int(len(message.content)/2)].lower() in list2 and not message.content in specialWords:
            ch = message.channel
            oldMessage = message.content
            newMessage = ''
            for i in range(int(len(message.content))):
                if i % 2 == 0:
                    newMessage += oldMessage[i].lower()
                else:
                    newMessage += oldMessage[i].upper()
            await message.channel.send(newMessage)
    except:
        await message.channel.send(":skull:")

    if message.content == "secret":
        ch = message.channel
        await message.channel.send('https://images-ext-2.discordapp.net/external/nFYzW-eGF3kfnrB4rjXhnQIolIcvImqwkVyZA6DG4Js/http/catgirldatabase.com/_data/i/upload/2020/07/06/20200706005308-520de81b-me.jpg')


@tasks.loop(seconds=5)
async def catgirl():
    randomNumber = 0  # random.randint(0, 10) while not in tartu ylikool
    if randomNumber == 0:
        await ch.send('https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')
    else:
        await ch.send(embed=get_image())


client.run("MzUxMzM2MTk0OTY3MDc2ODY0.GdvZD6.EeU8chS1boc6_CtZyrweXua__K1c_iC6Am5FuE")
