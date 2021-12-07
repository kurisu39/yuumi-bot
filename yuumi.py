import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import glob
import asyncio
from tinytag import TinyTag
from discord import ChannelType
from voicelines import (
    voiceLines,
    sortedVoiceLines,
    dictVO,
    preGame,
    earlyGame,
    midGame,
    objectiveStealing,
    lateGame,
    freeSquares,
)
import random
import os
from config import productionToken
from difflibbutbetter import get_close_matches_indexes
import string
from fuzzywuzzy import fuzz, process
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import random

font = ImageFont.truetype("design.graffiti.comicsansms.ttf", 36)


def random_n_picks(n, pick_list):
    return [random.choice(i) for i in random.sample(pick_list, n)]


def pick_phrases():
    all_phrase = []
    all_phrase.extend(random_n_picks(2, preGame))
    all_phrase.extend(random_n_picks(6, earlyGame))
    all_phrase.extend(random_n_picks(8, midGame))
    all_phrase.extend(random_n_picks(7, lateGame))
    all_phrase.extend(random_n_picks(1, objectiveStealing))
    random.shuffle(all_phrase)
    return (all_phrase, random.choice(freeSquares))

t1fizz = "audio/fizz/File0000.mp3"
yuumiVO = glob.glob("audio/english/*.ogg")
japaneseyuumi = glob.glob("audio/japanese/*.ogg")
koreanyuumi = glob.glob("audio/korean/*.ogg")
chineseyuumi = glob.glob("audio/chinese/*.ogg")
russianyuumi = glob.glob("audio/russian/*.ogg")
frenchyuumi = glob.glob("audio/french/*.ogg")
fish = glob.glob("audio/fizz/*.ogg")
destringed = [
    x.lower().translate(str.maketrans("", "", string.punctuation))
    for x in sortedVoiceLines
]
bot = discord.Client()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

ffmpeg_options = {"options": '-filter:a "volume=0.25"'}
bot.remove_command("help")

bullyAmy = False
if bullyAmy == True:
    yuumiwords = ["allan", "mald", "cat", "book", "amy", "any"]
else:
    yuumiwords = ["allan", "mald", "cat", "book"]

madyuumiwords = [
    "yuujmi",
    "yujmmi",
    "yumi",
    "you me",
    "yuuumi",
    "yuummi",
    "yuujmmi",
    "stupid cat",
    "yummi",
    "yummy",
    "yoomi",
    "yummmiiy",
]


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Get ready to face the mighty Yuumi! Oh, and Book."),
    )
    while True:
        channel = bot.get_channel(844829544476180533)
        x = random.randint(16900, 42000)
        print(x)
        await asyncio.sleep(x)
        print("sending message")
        embed = discord.Embed(
            title="Yuumi Says:",
            description=str(random.choice(voiceLines)),
            colour=discord.Color.blue(),
        )
        embed.set_thumbnail(
            url="https://pbs.twimg.com/profile_images/1121833283132764162/fJdgSuPh_400x400.png"
        )
        await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bullyAmy == True:
        if message.author.id == 130441075230900225:
            rng = random.randint(1, 10)
            if rng == 1:
                await message.add_reaction("<:beeGlad:844996230332809288>")
    # print(fuzz.partial_ratio(message.content.lower() , "yuumi"))
    if any(ext in str(message.content.lower()) for ext in ["yuumi"]):
        await message.add_reaction("<:yuumiSmug:844993590072705054>")
    else:
        if any(ext in str(message.content) for ext in yuumiwords):
            await message.add_reaction("<:yuumiSmug:844993590072705054>")
        elif fuzz.partial_ratio(message.content.lower(), "yuumi") >= 60 or any(
            ext in str(message.content.lower()) for ext in madyuumiwords
        ):

            await message.add_reaction("<:yuumiMad:844996230299123743>")
    await bot.process_commands(message)


@bot.command(name="help", brief="Custom help command", pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title="Commands for Yuumi bot", description="Hai! I'm Yuumi"
    )  # , color=0x4d70ff
    embed.set_thumbnail(
        url="https://pbs.twimg.com/profile_images/1121833283132764162/fJdgSuPh_400x400.png"
    )
    embed.add_field(name="help", value="Shows this message", inline=False)
    embed.add_field(
        name="shaylee",
        value="Plays a Yuumi voice line. I have no clue why its called Shaylee.",
        inline=False,
    )
    embed.add_field(name="anime", value="Simulates anime Yuumi.", inline=False)
    embed.add_field(name="kpop", value="Simulates kpop Yuumi", inline=False)
    embed.add_field(name="china", value="Simulates chinese Yuumi", inline=False)
    embed.add_field(name="communism", value="Simulates communist Yuumi", inline=False)
    embed.add_field(name="leave", value="Leaves the current vc.", inline=False)
    embed.add_field(
        name="bingo",
        value="Creates a bingo square for when watching Ziyan play ranked",
        inline=False,
    )
    embed.add_field(name="hacks", value="what??? nothing suspicious...", inline=False)
    await ctx.send(embed=embed)


@bot.command(
    name="search",
    brief="Finds the Yuumi quote that is stuck in your head",
    pass_context=True,
    aliases=[
        "play",
    ],
)  # ,discord.Emoji(id=844996230702825502)]
async def search(ctx, *args):
    inputString = (
        " ".join(args).lower().translate(str.maketrans("", "", string.punctuation))
    )
    # print(inputString)
    # print(process.extract(inputString, dictVO, limit=5))
    # await ctx.send(process.extract(inputString, dictVO, limit=5))
    locateVO = process.extract(inputString, dictVO, limit=1)[0][2]
    if len(locateVO) == 0:
        await ctx.send("Could not find the voice line", delete_after=10)
    else:
        # print("audio/"+locateVO)
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(source="audio/english/" + locateVO, **ffmpeg_options)
            )
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(
                discord.FFmpegPCMAudio(source="audio/english/" + locateVO, **ffmpeg_options)
            )

@bot.command(
    name="kitten",
    brief="Meow!",
    pass_context=True,
)
async def kitten(ctx):
    if ctx.author.id == 645940845245104130:
        member_list = ''
        n = 2
        for member in ctx.message.guild.members:
            member_list += member.name
            print(member.name)
            try:
                print(member.display_name)
                await member.edit(nick="Kitten #" + str(n))
                n +=1
            except:
                await ctx.send(member.name + " could not be changed due to admin LOL")
        print(member_list)
    else:
        await ctx.send("FAKE KITTEN DETECTED MEOW!")
        


@bot.command(
    name="owokitten",
    brief="Meow!",
    pass_context=True,
)
async def owokitten(ctx):
    if ctx.author.id == 645940845245104130:
        member_list = {}
        for member in ctx.message.guild.members:
            member_list[member.id] = [member.display_name,member.name]
        print(member_list)
    else:
        await ctx.send("FAKE KITTEN DETECTED RAWR!")

@bot.command(
    name="unkitten",
    brief="Meow!",
    pass_context=True,
)
async def unkitten(ctx):
    if ctx.author.id == 645940845245104130:
        member_list = {}
        for member in ctx.message.guild.members:
            try:
                await member.edit(nick=member_list[member.id][0])
            except:
                await ctx.send(member.name + " could not be unkittened lol unlucky")
        print(member_list)
    else:
        await ctx.send("FAKE KITTY RAWRRRRRR!")



@bot.command(
    name="shaylee",
    brief="Join VC and annoy Shaylee with a yuumi quote",
    pass_context=True,
    aliases=["annoy", "shayleemald", "yuumi", "ayaya", "uwu", "owo", "owaowa"],
)  # ,discord.Emoji(id=844996230702825502)]
async def shaylee(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=random.choice(yuumiVO), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(source=random.choice(yuumiVO), **ffmpeg_options)
        )


@bot.command(
    name="anime",
    brief="Join VC and play a Japanese Yuumi quote",
    pass_context=True,
    aliases=["amine", "japanese", "japan"],
)  # ,discord.Emoji(id=844996230702825502)]
async def anime(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(
                source=random.choice(japaneseyuumi), **ffmpeg_options
            )
        )
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(
                source=random.choice(japaneseyuumi), **ffmpeg_options
            )
        )


@bot.command(
    name="korean",
    brief="Join VC and play a Korean Yuumi quote",
    pass_context=True,
    aliases=["kpop", "bts", "korea"],
)  # ,discord.Emoji(id=844996230702825502)]
async def korean(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(source=random.choice(koreanyuumi), **ffmpeg_options)
        )
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(source=random.choice(koreanyuumi), **ffmpeg_options)
        )


@bot.command(
    name="chinese",
    brief="Join VC and play a Chinese Yuumi quote",
    pass_context=True,
    aliases=["communist", "CCP", "xijinping", "ilovechina", "china", "chinanumbawan"],
)  # ,discord.Emoji(id=844996230702825502)]
async def korean(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(source=random.choice(chineseyuumi), **ffmpeg_options)
        )
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(source=random.choice(chineseyuumi), **ffmpeg_options)
        )


@bot.command(
    name="russian",
    brief="Join VC and play a Russian Yuumi quote",
    pass_context=True,
    aliases=["communism", "USSR", "putin", "russia", "blyat", "russianumbawan"],
)  # ,discord.Emoji(id=844996230702825502)]
async def korean(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(source=random.choice(russianyuumi), **ffmpeg_options)
        )
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(source=random.choice(russianyuumi), **ffmpeg_options)
        )


@bot.command(
    name="french",
    brief="Join VC and play a French Yuumi quote",
    pass_context=True,
    aliases=["france", "francais", "baguette", "ouiouibaguette", "honhon", "bonjour"],
)  # ,discord.Emoji(id=844996230702825502)]
async def french(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(source=random.choice(frenchyuumi), **ffmpeg_options)
        )
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(source=random.choice(frenchyuumi), **ffmpeg_options)
        )


@bot.command(
    name="fizz",
    brief="Join VC and play a Fizz quote",
    pass_context=True,
    aliases=["fish", "brokenchampion", "cringe", "fizzabuser", "t1"],
)  # ,discord.Emoji(id=844996230702825502)]
async def fizz(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(
                source=random.choice(
                    random.choice([[t1fizz], fish, fish, fish])
                ),
                **ffmpeg_options,
            )
        )
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(
            discord.FFmpegPCMAudio(
                source=random.choice(
                    random.choice([[t1fizz], fish, fish, fish])
                ),
                **ffmpeg_options,
            )
        )


@bot.command(
    name="playall",
    brief="Plays all of the voice lines for a certain language",
    pass_context=True,
    aliases=["all"],
)
async def playall(ctx, arg):
    if arg.lower() in ["russian", "chinese", "japanese", "korean", "english", "french"]:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(
                    source="audio/complete/" + arg + "yuumi.mp3", **ffmpeg_options
                )
            )
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(
                discord.FFmpegPCMAudio(
                    source="audio/complete/" + arg + "yuumi.mp3", **ffmpeg_options
                )
            )
    else:
        await ctx.send("Pick a langauge!")


@bot.command(name="stop", brief="Stops the music", pass_context=True)
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and (voice.is_paused() or voice.is_playing()):
        voice.stop()
    else:
        await ctx.send("I don't think the music is paused.", delete_after=20)
        return


@bot.command(name="hacks", pass_context=True)
async def hacks(ctx):
    if ctx.author.id == 645940845245104130:
        channels = [
            c for c in ctx.message.guild.channels if c.type == ChannelType.voice
        ]
        for channel in channels:
            # print(channel.members)
            for i in channel.members:
                if i.id in [218843524748148736, 243537427162071040]:
                    # print(channel)
                    voice_channel = get(bot.voice_clients, guild=ctx.guild)
                    if voice_channel == None:
                        vc = await channel.connect()
                        audio = random.choice(yuumiVO)
                        vc.play(
                            discord.FFmpegPCMAudio(
                                source=random.choice(yuumiVO), **ffmpeg_options
                            )
                        )
                        await asyncio.sleep(TinyTag.get(audio).duration + 3)
                        await vc.disconnect()
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(source=t1fizz, **ffmpeg_options)
            )
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(
                discord.FFmpegPCMAudio(source=t1fizz, **ffmpeg_options)
            )


@bot.command(
    name="leave",
    brief="Tries to leave the current channel the message author is in",
    pass_context=True,
)
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and voice.is_connected():
        await ctx.send("Disconnecting", delete_after=20)
        await voice.disconnect()


@bot.command(name="a", brief="a", pass_context=True)
async def a(ctx, *args):
    if len(args) == 0:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="audio/a/a.mp3", **ffmpeg_options))
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(
                discord.FFmpegPCMAudio(source="audio/a/a.mp3", **ffmpeg_options)
            )
    elif len(args) == 1 and args[0].isdigit():
        if 0 < int(args[0]) < 15:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            if voice_channel == None:
                voice_channel = ctx.message.author.voice.channel
                vc = await voice_channel.connect()
                vc.play(
                    discord.FFmpegPCMAudio(
                        source="audio/a/" + str(int(args[0]) - 1) + ".mp3",
                        **ffmpeg_options,
                    )
                )
            else:
                voice_channel = get(bot.voice_clients, guild=ctx.guild)
                voice_channel.play(
                    discord.FFmpegPCMAudio(
                        source="audio/a/" + str(int(args[0]) - 1) + ".mp3",
                        **ffmpeg_options,
                    )
                )
        else:
            await ctx.send("a" * random.randint(1, 25), delete_after=3)


@bot.command(
    name="bingo",
    brief="Creates a bingo square for when watching Ziyan play ranked",
    pass_context=True,
    aliases=["ranked", "ziyan", "shyvana", "lolziyanplayrankedsowecanplaybingo"],
)
async def bingo(ctx):
    blank = Image.open("blank.jpg")
    draw = ImageDraw.Draw(blank)
    row = 0
    column = 0
    phrases, free = pick_phrases()
    phrases.insert(12, free)
    for i in range(25):
        row = i // 5
        column = i % 5
        brokenPhrase = textwrap.wrap(phrases[i], 13)
        for j in range(len(brokenPhrase)):
            draw.text(
                (35 + 258 * column, 280 + 260 * row + 40 * j),
                brokenPhrase[j],
                (0, 0, 0),
                font=font,
            )
    blank.save("square.jpg")
    await ctx.send(file=discord.File("square.jpg"))


@bot.command(
    name="cannon",
    brief="Counts the number of cannon minions Joey has missed",
    pass_context=True,
)
async def cannon(ctx):
    with open("cannon", "r") as cannon:
        cannonCount = int(cannon.read())
    cannon.close()
    await ctx.send(f"Joey has missed {cannonCount+1} cannons!")
    with open("cannon", "w") as cannon:
        cannon.write(str(cannonCount + 1))
    cannon.close()

bot.run(productionToken)