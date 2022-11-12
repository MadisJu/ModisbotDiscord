import asyncio
import random
import re

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord import app_commands
import CatGirl_Data
import CatGirlRating


#New stuff
class Bot(commands.Bot):

    ch = None
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

#Stuff

bot = Bot()

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
    emb.title = "The catgirl id: " + str(id)
    emb.add_field(name="Rating",
                  value="Average: {} ({} / ratings) ".format(round(cg_d.AvgRating(), 1), len(cg_d.ratings)),
                  inline=True)
    emb.add_field(name="Comments", value=cg_d.comments, inline=True)
    return emb

class RatingView(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.value = None
        self.response = None

    @discord.ui.button(label="1", style=discord.ButtonStyle.green)
    async def rate1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 1
        self.clear_items()
        self.stop()

    @discord.ui.button(label="2", style=discord.ButtonStyle.green)
    async def rate2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 2
        self.clear_items()
        self.stop()

    @discord.ui.button(label="3", style=discord.ButtonStyle.green)
    async def rate3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 3
        self.clear_items()
        self.stop()

    @discord.ui.button(label="4", style=discord.ButtonStyle.green)
    async def rate4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 4
        self.clear_items()
        self.stop()

    @discord.ui.button(label="5", style=discord.ButtonStyle.green)
    async def rate5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 5
        self.clear_items()
        self.stop()

class CommentModal(discord.ui.Modal, title="Enter your comment"):
    text = discord.ui.TextInput(label="Comment")
    async def on_submit(self, interaction: discord.Interaction):
        self.text = str(self.text)
        await interaction.response.send_message("Comment added!")


class CommentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=50)
        self.value = None

    @discord.ui.button(label="Press here to write a comment", style=discord.ButtonStyle.green)
    async def rate1(self, interaction: discord.Interaction, button: discord.ui.Button):
        cmodal = CommentModal()

        await interaction.response.send_modal(cmodal)
        await cmodal.wait()
        print(str(cmodal.text))
        self.value = cmodal.text
        self.stop()


@bot.command()
async def ask(ctx):
    view = RatingView()
    await ctx.send("buttonhole", view=view)
    await view.wait()

@bot.command()
async def getrate(ctx, id):
    msg = await ctx.channel.send(embed=GetImgRating(id))
    thread = await msg.create_thread(name = id)
    cg = CatGirl_Data.CatGirl(id)
    for cmt in cg.comments:
        await thread.send(cmt)
    await msg.delete(delay = 20)
    await ctx.message.delete()
    await asyncio.sleep(20)
    await thread.delete()
    return

@bot.command()
async def comment(ctx, id : int):

    cview = CommentView()
    await ctx.channel.send(embed=GetImgRating(id), view= cview)
    await cview.wait()
    print(cview.value)
    if cview.value != None:
        CatGirlRating.AddComment(id, "{} > {}".format(ctx.author.name, str(cview.value)))
    return

@bot.command()
async def rate(ctx, id):
    await ctx.channel.send(embed=GetImgRating(id))
    btns = RatingView(timeout= 10)
    output = await ctx.channel.send("Rate this catgirl", view=btns)
    await btns.wait()
    rating = btns.value
    await output.delete()
    if rating != None:
        rating = max(min(int(rating), 5), 1)
        #Actually add the rating now
        CatGirlRating.AddRating(id, rating)
        await ctx.channel.send("You have rated this catgirl: ({}/5)".format(rating))
    else:
        await ctx.channel.send("Timout")
    return

async def RateCommand(ch, id):
    await ch.send(embed=GetImgRating(id))
    btns = RatingView(timeout= 10)
    output = await ch.send("Rate this catgirl", view=btns)
    await btns.wait()
    rating = btns.value
    await output.delete()
    if rating != None:
        rating = max(min(int(rating), 5), 1)
        #Actually add the rating now
        CatGirlRating.AddRating(id, rating)
        await ch.send("You have rated this catgirl: ({}/5)".format(rating))
    else:
        await ch.send("Timout")

    return

@bot.command()
async def start(ctx):
    bot.ch = ctx.channel
    catgirl.start()

@bot.command()
async def stop(ctx):
    bot.ch = ctx.channel
    catgirl.cancel()

@bot.command()
async def secret(ctx):
    await ctx.channel.send(
        'https://images-ext-2.discordapp.net/external/nFYzW-eGF3kfnrB4rjXhnQIolIcvImqwkVyZA6DG4Js/http/catgirldatabase.com/_data/i/upload/2020/07/06/20200706005308-520de81b-me.jpg')
    return
@bot.command()
async def modis(ctx):
    await ctx.channel.send(
        'https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')
    return



"""
@bot.event
async def on_message(message):
    global ch, loopTime
    if message.author == bot.user:
        return

    if message.content == "!Hello":
        await ask()

    if message.content == "modis" or message.content == '@Modis':
        await message.channel.send(
            'https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')

    if message.content == "start":
        ch = message.channel
        catgirl.start()

    if message.content == "stop":
        ch = message.channel
        catgirl.cancel()


    #Shitpost
    if "bot" in message.content.lower():
        ch = message.channel
        await message.channel.send("Minust räägite?")
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
        ch = message.channel;
        """

#Catgirls every 5 seconds
@tasks.loop(seconds=5)
async def catgirl():
    randomNumber = 1  # random.randint(0, 10) while not in tartu ylikool
    if randomNumber == 0:
        await bot.ch.send('https://media.discordapp.net/attachments/1033478386196156446/1033495265367306330/madis_hmm_gif.gif')
    else:
        await RateCommand(bot.ch, random.randint(0, 4260))




bot.run("MzUxMzM2MTk0OTY3MDc2ODY0.GdvZD6.EeU8chS1boc6_CtZyrweXua__K1c_iC6Am5FuE")