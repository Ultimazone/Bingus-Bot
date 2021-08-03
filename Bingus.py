import random
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import Embed
from googlesearch import search
import time
import json
import os
from datetime import datetime, timedelta

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]


help_command = commands.DefaultHelpCommand(no_category = 'Commands')
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

@bot.command(name='poll', help='Makes a poll for people to answer')
async def poll(ctx, question: str, *options):
    if len(options) > 10:
        await ctx.send("You can only give 10 options!")

    else:
        embed = Embed(title="Poll",
                      colour=ctx.author.color,
                  description=question,
                  timestamp=datetime.utcnow())
        fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
            ("Instructions", "React to cast a vote!", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        message = await ctx.send(embed=embed)
        for emoji in numbers[:len(options)]:
            await message.add_reaction(emoji)


@bot.command(name='beargo', help='Makes the bears go')
async def beargo(ctx, numberofbeargo):
    numb = int(numberofbeargo)
    beargotext = '<a:beargo:525829929271689217>'
    bearmessage = ''
    for x in range(numb):
        bearmessage = bearmessage + beargotext
    await ctx.message.channel.send(bearmessage)


@bot.command(name='avatar')
async def avatar(ctx, *, useravatar: discord.Member = None):
    if not useravatar:
        useravatar = ctx.message.mentions
    pfp = useravatar.avatar_url
    await ctx.message.channel.send(pfp)

@bot.command(name='color')
async def color(ctx, *, usercolor: discord.Member = None):
    if not usercolor:
        usercolor = ctx.message.mentions
    colorr = usercolor.color
    colorembed = discord.Embed(
        title= f'{colorr}',
        color = colorr)
    await ctx.message.channel.send(embed = colorembed)


@bot.command(name='blade', help='Posts BLADE_SEQ.mp3')
async def blade(ctx):
    with open('SEQBLADE.mp3', 'rb') as fp:
        await ctx.message.channel.send(file=discord.File(fp, 'BLADE_SEQ.mp3'))


@bot.command(name='pokemon', help='Pulls up the PokemonDB page of the requested Pokemon')
async def pokemon(ctx, *, arg):
    pokemondblink = 'https://pokemondb.net/pokedex/'
    names = arg.replace(" ", "-")
    await ctx.message.channel.send(pokemondblink + names)


@bot.command(name='move', help='Pulls up the PokemonDB page of the requested move')
async def move(ctx, *, arg):
    pokemondbmovelink = 'https://pokemondb.net/move/'
    movename = arg.replace(" ", "-")
    await ctx.message.channel.send(pokemondbmovelink + movename)


@bot.command(name='chan', help='Pulls a random post from the first 5 pages of a specified 4chan board')
async def chan(ctx, board):
    boardurl = 'https://boards.4chan.org/' + f'{board}/'
    pagenumber = random.randint(1, 10)
    if pagenumber == 1:
        boardurlpage = f'{boardurl}'
    else:
        boardurlpage = f'{boardurl}' + f'{pagenumber}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    content = requests.get(boardurlpage, timeout=1000, headers=headers)
    html = requests.get(boardurlpage, timeout=1000, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    post = soup.findAll("blockquote")
    postlink = random.choice(post)
    postpar = postlink.previous_sibling
    if "Anonymous" in postpar.text:
        await ctx.message.channel.send(postlink.text)
    elif "File:" in postpar.text:
        await ctx.message.channel.send(f'https:{postpar.a["href"]}' + " " + postlink.text)
    else:
        await ctx.message.channel.send(postlink.text)



@bot.command(name='learn', help='Determines if and how a pokemon learns the given move')
async def learn(ctx, *, args):
    arg1, arg2 = args.split("|")
    bop = ' '.join(elem.capitalize() for elem in arg1.split())
    bup = ' '.join(elem.capitalize() for elem in arg2.split())
    mon = arg1.replace(" ", "-").replace("'", "")
    moves = arg2.replace(" ", "-").replace("'", "")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    monurl = 'https://pokemondb.net/pokedex/' + f'{mon}'
    content = requests.get(monurl, timeout=.1, headers=headers)
    html = requests.get(monurl, timeout=.1, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    movelocation = soup.find("a", href=f"/move/{moves}")
    if not (movelocation is None):
        mlparent = movelocation.parent
        methodnumber = mlparent.previousSibling
        methodparents = movelocation.parent.parent.parent.parent.parent
        if 'Lv.' in methodparents.text:
            await ctx.message.channel.send(f'{bop} learns {bup} at level {methodnumber.text}.')
        elif 'TM' in methodparents.text:
            await ctx.message.channel.send(f'{bop} learns {bup} from TM{methodnumber.text}.')
        elif 'TR' in methodparents.text:
            await ctx.message.channel.send(f'{bop} learns {bup} from TR{methodnumber.text}.')
        else:
            await ctx.message.channel.send(f'{bop} learns {bup} as an egg or tutor move.')
    else:
        await ctx.message.channel.send(f'{bop} does not learn {bup} or move is invalid.')


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


@bot.command(name='tune', help='Make a 16 note tune with the Animal Crossing tune maker.', description = 'Notes = a-g, Hold = s, None = z, Random = R')
async def tune(ctx, *, arg):
    notes = arg.replace(" ", "-")
    await ctx.message.channel.send(f'http://nooknet.net/tunes?melody={notes}&title=Jujigun')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "test":
        await message.channel.send("tust")
    if message.content == "PLEASE":
        await message.channel.send("I BEG YOU")
    if "<:trash:453781143976804352>" in message.content:
        emoji = '<:Yuri:642749514838442005>'
        await message.add_reaction(emoji)
    if message.content.lower() == "based":
        await message.channel.send("based on what")
    if "hey bingus" in message.content.lower():
        heyreply = random.randint(1, 2)
        yesreplies = ["Yes.", "Ye.", "Yeah.", "Yup.",
                      "Uh-huh.", "Yeet.", "Sure.", "Yuh.", "Yayuh."]
        noreplies = ["No.", "Nah.", "Nuh-uh.", "Nope.", "Uhhh, no..."]
        replyyes = random.choice(yesreplies)
        replyno = random.choice(noreplies)
        if heyreply == 1:
            await message.channel.send(replyyes)
        else:
            await message.channel.send(replyno)
    await bot.process_commands(message)


@bot.event
async def on_ready():
    # DO STUFF....
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('bing! or @Bingus'))


# Run the bot on the server
bot.run(token)

