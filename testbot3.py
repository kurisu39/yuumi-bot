from hashlib import algorithms_guaranteed
import discord
from difflibbutbetter import get_close_matches_indexes
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import glob
import asyncio
from tinytag import TinyTag
from discord import ChannelType
from voicelines import voiceLines, sortedVoiceLines, dictVO
import random
import os
import string
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

destringed = [x.lower().translate(str.maketrans('', '', string.punctuation)) for x in sortedVoiceLines]
from config import testToken

yuumiVO = glob.glob("audio/*.ogg")
japaneseyuumi = glob.glob("japanese/*.ogg")
koreanyuumi = glob.glob("korean/*.ogg")
chineseyuumi = glob.glob("chinese/*.ogg")
russianyuumi = glob.glob("russian/*.ogg")
frenchyuumi = glob.glob("french/*.ogg")

bot = discord.Client()
bot = commands.Bot(command_prefix='%')
ffmpeg_options = {'options': '-filter:a "volume=0.1"'}
bot.remove_command('help')

bullyAmy = False
if bullyAmy == True:
    yuumiwords = ["zoomie","zoomies","allan","mald","cat","book", "amy","any"]
else:
    yuumiwords = ["zoomie","zoomies","allan","mald","cat","book"]

madyuumiwords = ["yuujmi", "yujmmi", "yumi", "you me", "yuuumi", "yuummi", "yuujmmi", "stupid cat", "yummi", "yummy","yoomi","yummmiiy","yoommie","yooommie"]

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status = discord.Status.online, activity=discord.Game('Get ready to face the mighty Yuumi! Oh, and Book.'))
    while True:
        channel = bot.get_channel(844829544476180533)
        x = random.randint(18000,43200)
        print(x)
        await asyncio.sleep(x)
        print('sending message')
        embed = discord.Embed(title="Yuumi Says:", description = str(random.choice(voiceLines)), colour=discord.Color.blue())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1121833283132764162/fJdgSuPh_400x400.png")
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
    print(fuzz.partial_ratio(message.content.lower() , "yuumi"))
    if any(ext in str(message.content.lower()) for ext in ["yuumi"]):
        await message.add_reaction(u"\U0001F3D3")
    else:
        if any(ext in str(message.content) for ext in yuumiwords):
            await message.add_reaction(u"\U0001F3D3")
        elif fuzz.partial_ratio(message.content.lower() , "yuumi") >= 60 or any(ext in str(message.content.lower()) for ext in madyuumiwords):
            
            await message.add_reaction(u"\U0001F408")
    await bot.process_commands(message)

@bot.command(name='help',
            brief='Custom help command',
            pass_context=True)
async def help(ctx):
    embed=discord.Embed(title="Commands for Yuumi bot", description="Hai! I'm Yuumi") #, color=0x4d70ff
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1121833283132764162/fJdgSuPh_400x400.png")
    embed.add_field(name="help", value="Shows this message", inline=False)
    embed.add_field(name="shaylee", value="Plays a Yuumi voice line. I have no clue why its called Shaylee.", inline=False)
    embed.add_field(name="anime", value="Simulates anime Yuumi.", inline=False)
    embed.add_field(name="kpop", value="Simulates kpop Yuumi", inline=False)
    embed.add_field(name="china", value="Simulates chinese Yuumi", inline=False)
    embed.add_field(name="communism", value="Simulates communist Yuumi", inline=False)
    embed.add_field(name="leave", value="Leaves the current vc.", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def test(ctx, *args):
    await ctx.send(args)

@bot.command(pass_context = True)
async def iq(ctx, *args):
    await ctx.send(fuzz.partial_ratio(" ".join(args), "yuumi"))

@bot.command(name="number", 
            brief='Plays yuumi quote by number',
            pass_context = True) #,discord.Emoji(id=844996230702825502)]
async def number(ctx, arg):
# just testing to see why its not working
    voNumber = int(arg)
    print(destringed[voNumber-1])
    if voNumber <= 9:
        voFile = "audio/File000" + str(voNumber) + ".ogg"
    elif voNumber >= 100:
        voFile = "audio/File0" + str(voNumber) + ".ogg"
    else:
        voFile = "audio/File00" + str(voNumber) + ".ogg"
    print(voFile)
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = voFile, **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = voFile, **ffmpeg_options))

@bot.command(name="search", 
            brief='Finds the Yuumi quote that is stuck in your head',
            pass_context = True,
            aliases=['play',]) #,discord.Emoji(id=844996230702825502)]
async def search(ctx, *args):
    inputString = " ".join(args).lower().translate(str.maketrans('', '', string.punctuation))
    print(inputString)
    print(process.extract(inputString, dictVO, limit=5))
    await ctx.send(process.extract(inputString, dictVO, limit=10))
    bestMatch = process.extract(inputString, dictVO, limit=10)[0][1]
    possibleFiles = []
    for i in process.extract(inputString, dictVO, limit=10):
        if i[1] == bestMatch:
            possibleFiles.append(i[2])
        else:
            break
    locateVO = process.extract(inputString, dictVO, limit=1)[0][2]
    if len(locateVO) == 0:
        await ctx.send("Could not find the voice line", delete_after=10)
    else:
        print("audio/"+locateVO)
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None: 
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = "audio/"+locateVO, **ffmpeg_options))
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = "audio/"+locateVO, **ffmpeg_options))


@bot.command(name='shaylee',
            brief='Join VC and annoy Shaylee with a yuumi quote',
            pass_context = True,
            aliases=['annoy','shayleemald','yuumi','ayaya','uwu','owo','owaowa']) #,discord.Emoji(id=844996230702825502)]
async def shaylee(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(yuumiVO), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(yuumiVO), **ffmpeg_options))

@bot.command(name='anime',
            brief='Join VC and play a Japanese Yuumi quote',
            pass_context = True,
            aliases=['amine','japanese','japan']) #,discord.Emoji(id=844996230702825502)]
async def anime(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(japaneseyuumi), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(japaneseyuumi), **ffmpeg_options))

@bot.command(name='korean',
            brief='Join VC and play a Korean Yuumi quote',
            pass_context = True,
            aliases=['kpop','bts','korea']) #,discord.Emoji(id=844996230702825502)]
async def korean(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(koreanyuumi), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(koreanyuumi), **ffmpeg_options))

@bot.command(name='chinese',
            brief='Join VC and play a Chinese Yuumi quote',
            pass_context = True,
            aliases=['communist','CCP','xijinping','ilovechina','china','chinanumbawan']) #,discord.Emoji(id=844996230702825502)]
async def korean(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(chineseyuumi), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(chineseyuumi), **ffmpeg_options))

@bot.command(name="russian",
            brief='Join VC and play a Russian Yuumi quote',
            pass_context = True,
            aliases=['communism','USSR','putin','russia','blyat','russianumbawan']) #,discord.Emoji(id=844996230702825502)]
async def korean(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(russianyuumi), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(russianyuumi), **ffmpeg_options))

@bot.command(name="french",
            brief='Join VC and play a French Yuumi quote',
            pass_context = True,
            aliases=['france','francais','baguette','ouiouibaguette','honhon', 'bonjour']) #,discord.Emoji(id=844996230702825502)]
async def french(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(frenchyuumi), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(frenchyuumi), **ffmpeg_options))

@bot.command(name="playall",
            brief="Plays all of the voice lines for a certain language",
            pass_context = True,
            aliases = ['all'])
async def playall(ctx, arg):
    if arg.lower() in ['russian','chinese','japanese','korean', "english","french"]:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None: 
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = arg+"yuumi.mp3", **ffmpeg_options))
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = arg+"yuumi.mp3", **ffmpeg_options))
    else:
        await ctx.send("Pick a langauge!")


@bot.command(name='stop',
            brief='Stops the music',
            pass_context=True)
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

@bot.command(name='hacks',
            pass_context = True)
async def hacks(ctx):
    if ctx.author.id == 645940845245104130:
        channels = [c for c in ctx.message.guild.channels if c.type==ChannelType.voice]
        for channel in channels:
            print(channel.members)
            for i in channel.members:
                if i.id in [218843524748148736,243537427162071040]:
                    print(channel)
                    voice_channel = get(bot.voice_clients, guild=ctx.guild)
                    if voice_channel == None: 
                        vc = await channel.connect()
                        audio = random.choice(yuumiVO)
                        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(yuumiVO), **ffmpeg_options))
                        await asyncio.sleep(TinyTag.get(audio).duration+3)
                        await vc.disconnect()
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel == None: 
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = "apyuumi.mp3", **ffmpeg_options))
        else:
            voice_channel = get(bot.voice_clients, guild=ctx.guild)
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = "apyuumi.mp3", **ffmpeg_options))

@bot.command(name='leave',
            brief='Tries to leave the current channel the message author is in',
            pass_context=True)
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and voice.is_connected():
        await ctx.send('Disconnecting', delete_after=20)
        await voice.disconnect()


@bot.command(name="a",
            brief="a",
            pass_context = True)
async def a(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source = "audio/a.mp3", **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(source = "audio/a.mp3", **ffmpeg_options))

bot.run(testToken)