import discord
import os
import time
from bs4 import BeautifulSoup
import requests
import random
import re
from discord.ext import tasks
import CatGirlRating
import CatGirl_Data

client = discord.Client(intents=discord.Intents.all())
ch = None

importantList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u'
    , 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

specialWords = ['cunt', 'stop', 'start', 'bot', 'secret']

list2 = 'qwertyuiopasdfghjklzxcvbnmüõö ä1234567890!@#$%^&*()[]{};:'"<>,./?\|"

def get_image():
    link = "http://catgirldatabase.com/picture.php?/{}/category/1".format(random.randint(0, 4260))
    a = requests.get(link).text
    soup = BeautifulSoup(a, 'html.parser')

    # ToDo if the page doesnt exsist it throws an error
    text = str(soup.find_all('img')[0])
    s = re.search('src="(.*)" title', text).group(1)

    url = "http://catgirldatabase.com/" + s
    x = discord.Embed()
    x.set_image(url=url)
    x.set_footer(text=link)
    return x

def get_image(id):
    try:
        link = "http://catgirldatabase.com/picture.php?/{}/category/1".format(id)
        a = requests.get(link).text
        soup = BeautifulSoup(a, 'html.parser')

        # ToDo check get_image()
        text = str(soup.find_all('img')[0])
        s = re.search('src="(.*)" title', text).group(1)

        url = "http://catgirldatabase.com/" + s
        x = discord.Embed()
        x.set_image(url=url)
        x.set_footer(text=link)
        return x
    except:
        x = discord.Embed()
        x.title(text="None")
        return x

def GetImgRating(id):
    emb = get_image(id)
    cg_d = CatGirl_Data.CatGirl(id)
    emb.title = "The catgirl id: " + id
    emb.add_field(name="Rating",
                  value="Average: {} ({} / ratings) ".format(round(cg_d.AvgRating(), 1), len(cg_d.ratings)),
                  inline=True)
    emb.add_field(name="Comments", value=cg_d.comments, inline=True)
    return emb


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

    if "!getrate" in message.content:
        msg = str(message.content)
        msg = msg.split(";")
        if len(msg < 1):
            if msg[1].isalnum():
                id = msg[1]
                await message.channel.send(embed=GetImgRating(id))
                return

    if "!rate" in message.content:
        msg = str(message.content)
        msg = msg.split(";")
        print(msg)
        if len(msg) > 2:
            if msg[1].isalnum() and msg[2].isalnum():
                #clamp rating to 1-5
                print("poop")
                msg[2] = int(msg[2])
                msg[2] = max(min(msg[2], 5), 1)
                #Actually add the rating now
                CatGirlRating.AddRating(int(msg[1]), msg[2])
                await message.channel.send(embed=GetImgRating(msg[1]))
                return


    if message.content == "modis" or message.content == '@Modis':
        await message.channel.send(
            'https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')

    if message.content == "start":
        ch = message.channel
        catgirl.start()

    if message.content == "stop":
        ch = message.channel
        await message.channel.send("LMAO *sToP*, there is no end to modis!")

    if "bot" in message.content.lower():
        ch = message.channel
        await message.channel.send("Minust räägite?")

    if message.content == "This nonsense needs to end!":
        ch = message.channel
        catgirl.cancel()
    try:
        if message.content[int(len(message.content)/2)].lower() in list2 and not message.content in specialWords and 'bot' not in message.content and len(message.content) > 10:
            ch = message.channel
            oldMessage = message.content
            newMessage = ''
            for i in range(int(len(message.content))):
                if i % 2 == 0:
                    newMessage += oldMessage[i].lower()
                else:
                    newMessage += oldMessage[i].upper()
            await message.channel.send(newMessage)
        else:
            await message.channel.send('OK :thumbsup:')
    except:
        await message.channel.send(":skull:")

    if message.content == "secret":
        ch = message.channel
        await message.channel.send('https://images-ext-2.discordapp.net/external/nFYzW-eGF3kfnrB4rjXhnQIolIcvImqwkVyZA6DG4Js/http/catgirldatabase.com/_data/i/upload/2020/07/06/20200706005308-520de81b-me.jpg')




@tasks.loop(seconds=5)
async def catgirl():
    randomNumber = 1  # random.randint(0, 10) while not in tartu ylikool
    if randomNumber == 0:
        await ch.send('https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')
    else:
        await ch.send(embed=GetImgRating(random.randint(0, 4260)))


client.run("MzUxMzM2MTk0OTY3MDc2ODY0.GdvZD6.EeU8chS1boc6_CtZyrweXua__K1c_iC6Am5FuE")
