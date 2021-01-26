import random
import discord
import requests
from discord.ext import commands
from googlesearch import search
import json
import os

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)


@bot.command(name='beargo', help='Makes the bears go')
async def beargo(ctx, numberofbeargo):
    numb = int(numberofbeargo)
    beargotext = '<a:beargo:525829929271689217>'
    bearmessage = ''
    for x in range(numb):
        bearmessage = bearmessage + beargotext
    await ctx.message.channel.send(bearmessage)


@bot.command(name='blade', help='Posts BLADE_SEQ.mp3')
async def blade(ctx):
    with open('SEQBLADE.mp3', 'rb') as fp:
        await ctx.message.channel.send(file=discord.File(fp, 'BLADE_SEQ.mp3'))


@bot.command(name='pokemon', help='Pulls up the PokemonDB page of the requested Pokemon')
async def pokemon(ctx, *, arg):
    pokemondblink = 'https://pokemondb.net/pokedex/'
    names = arg.replace(" ", "-")
    await ctx.message.channel.send(pokemondblink + names)

    
@bot.command(name='move', help='Determines if and how a pokemon learns the given move')
async def move(ctx, *, args):
    arg1, arg2 = args.split("|")
    moves = arg1.replace(" ", "-")
    mon = arg2.replace(" ", "-")
    moveurl = 'https://pokemondb.net/move/' + f'{moves}'
    content = requests.get(moveurl)
    if content.text.lower().__contains__(mon):
        await ctx.message.channel.send(f'Yes, {arg2} learns {arg1}.')
    else:
        await ctx.message.channel.send(f'No, {arg2} does not learn {arg1}.')
    

@bot.command(aliases=['search', 'g'], help='Grabs the first five search results')
async def google(ctx, *, text):
    re = search(query=text, tld='com', lang='en', num=5, stop=5, pause=2.0)
    st = []
    for s in re:
        st.append(f"<{s}>")
    fmt = '\n'.join(st)
    mbd = discord.Embed(title="Search Results", color=0xf0ead6)
    mbd.add_field(name="Any of these what you're looking for?", value=fmt)
    await ctx.message.channel.send(embed=mbd)


@bot.command(name='8ball', help='Ask Bingus a question, get one of many answers')
async def eightball(ctx):
    ballstatus = random.randint(1, 3)
    yeschoices = ["This is the way.", "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes."]
    maybechoices = ["Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again."]
    nochoices = ["Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    ballyes = random.choice(yeschoices)
    ballmaybe = random.choice(maybechoices)
    ballno = random.choice(nochoices)
    if ballstatus == 1:
        await ctx.message.channel.send(ballyes)
    if ballstatus == 2:
        await ctx.message.channel.send(ballmaybe)
    if ballstatus == 3:
        await ctx.message.channel.send(ballno)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "test":
        await message.channel.send("tust")
        print("sah")
    if "<:trash:453781143976804352>" in message.content:
        emoji = '<:Yuri:642749514838442005>'
        await message.add_reaction(emoji)
        print("bingbong")
    if message.content.lower() == "based":
        await message.channel.send("based on what")
    if "hey bingus" in message.content.lower() or "<@!788956209260134423>" in message.content:
        heyreply = random.randint(1, 2)
        if heyreply == 1:
            await message.channel.send("Ye")
        else:
            await message.channel.send("No")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    # DO STUFF....
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('bing!'))


# Run the bot on the server
bot.run(token)
