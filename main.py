import base64
import string

import discord
import numpy
import pwn
from discord.ext import commands

f = open("keys.txt", "r")
TOKEN = f.readline().strip()
serverID = int(f.readline().strip())

###############################################################################################
#####################################  VARIABLES  #############################################
###############################################################################################

bot = commands.Bot(command_prefix="!")


class CTF:
    def __init__(self):
        self.activeCTF = ""

    def setCTF(self, ctfname):
        self.activeCTF = ctfname

    def getCTF(self):
        return self.activeCTF


activeCTF = CTF()

###############################################################################################
#####################################  EVENTS  ################################################
###############################################################################################


@bot.event
async def on_ready():
    global activeCTF
    print("Logged on as")
    print(bot.user.name)
    print(bot.user.id)
    print("--------")


@bot.event
async def on_message(message):
    # print(
    # 	"Message from {0.author}: {0.content} in channel: {0.channel}".format(message)
    # )
    await bot.process_commands(message)


###############################################################################################
#####################################  COMMANDS  ##############################################
###############################################################################################
@bot.command()
async def currentctf(ctx):
    if activeCTF.getCTF() == "":
        await ctx.send("Please run `!setctf [ctfname]` or `!createctf [ctfname]`first.")
    else:
        await ctx.send("`{}`, is the selected CTF.".format(activeCTF.getCTF()))
    pass


@bot.command()
async def setctf(ctx, ctfname):
    print("setting ctf: " + ctfname.lower())
    category = discord.utils.get(ctx.guild.categories, name=ctfname.lower())
    # print(category)
    if category != None:
        activeCTF.setCTF(ctfname.lower())
    else:
        await ctx.send("That ctf doesn't exist :(")
    pass


@bot.command()
async def createctf(ctx, *ctfname):
    ctfname = "-".join(ctfname).lower()
    print("creating CTF: " + ctfname)
    if not discord.utils.get(ctx.guild.categories, name=ctfname):
        await ctx.guild.create_category(ctfname)
        activeCTF.setCTF(ctfname)
    else:
        await ctx.send("A CTF with this name already exists")
    pass


@bot.command()
async def q(ctx, *questionTitle):
    print("adding question")
    if activeCTF.getCTF() == "":
        await ctx.send("Please run `!setctf [ctfname]` or `!ctf [ctfname]`first.")
    else:
        questionTitle = "-".join(questionTitle).lower()
        category = discord.utils.get(ctx.guild.categories, name=activeCTF.getCTF())
        await ctx.guild.create_text_channel(questionTitle, category=category)
    pass


@bot.command()
async def merge(ctx, category):
    # merging doesn't delete the originals in case of an accidental merge
    print("merging category: " + category)
    category = discord.utils.get(ctx.guild.categories, name=category)
    ctx.guild.create_text_channel("__archive", category=category)
    file = ""
    for textChannel in category.channels:
        file = file + "\n# " + str(category.name) + ": " + str(textChannel.name)
        if str(textChannel.type) == "text" and str(textChannel.name) != "__archive":
            messages = await textChannel.history().flatten()
            m = [x.content for x in messages][::-1]  # reverse messages
            for i in m:
                file = file + "\n" + " - " + i
        file = file + "\n---"

    print(activeCTF.getCTF() + "-archive")
    print(discord.utils.get(ctx.guild.channels, name=activeCTF.getCTF() + "-archive"))

    if (
        discord.utils.get(ctx.guild.channels, name=activeCTF.getCTF() + "-archive")
        is None
    ):
        await ctx.guild.create_text_channel(
            activeCTF.getCTF() + "-archive",
            category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"),
        )
        archive_channel = bot.get_channel(
            discord.utils.get(
                ctx.guild.channels, name=activeCTF.getCTF() + "-archive"
            ).id
        )
        await archive_channel.send(file)

    else:
        await ctx.send(
            "This CTF has already been merged or something has gone very, very wrong :("
        )
    pass

# Actual CTF commands

@bot.command()
async def b64Decode(ctx, string):
	await ctx.send(base64.b64decode(string).decode("utf-8"))

@bot.command()
async def b64Encode(ctx, string):
	await ctx.send(base64.b64encode(string.encode()).decode("utf-8"))


###############################################################################################

bot.run(TOKEN)
