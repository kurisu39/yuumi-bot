
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import glob
import asyncio
from discord import ChannelType
import time
from tinytag import TinyTag
#from nltk.sentiment import SentimentIntensityANalyzer
from voicelines import voiceLines
import random
import os

token = "ODQ1MTM1MjIyMTg1Nzg3NDEz.YKcjgg.pot5KLyWhaLbELGcIbrEkW6AFDs"

#sia = SentimentIntensityAnalyzer()
yuumiVO = glob.glob("audio/*.ogg")
bot = discord.Client()
bot = commands.Bot(command_prefix='!')
ffmpeg_options = {'options': '-filter:a "volume=0.25"'}
bot.remove_command('help')
yuumiwords = ["allan","yuumi","mald","cat","book"]

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status = discord.Status.online, activity=discord.Game('Get ready to face the mighty Yuumi! Oh, and Book.'))
    while True:
        channel = bot.get_channel(845848041054928906)
        print('sending message')
        embed = discord.Embed(title="Yuumi Says:", description = str(random.choice(voiceLines)), colour=discord.Color.blue())
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1121833283132764162/fJdgSuPh_400x400.png")
        x = random.randint(300,3600)
        print(x)
        ty_res = time.gmtime(x)
        res = time.strftime("%H hours and %M minute(s)",ty_res)
        embed.add_field(name="My next quote is in", value=res, inline=True)
        print(res)
        await channel.send(embed=embed)
        await asyncio.sleep(x)

@bot.event
async def on_message(message):
    if message.author == bot.user:
            return
    if message.author.id == 645940845245104130:
        rng = random.randint(1, 2)
        print(rng)
        if rng == 1:
            await message.add_reaction("<:beeGlad:844996230332809288>")
    if any(ext in str(message.content) for ext in yuumiwords):
        #await message.channel.send('+:yuumiSmug:')
        await message.add_reaction("<:yuumiSmug:844993590072705054>")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await member.send('Private message')

@bot.command(name='help',
            brief='Custom help command',
            pass_context=True)
async def help(ctx):
    embed=discord.Embed(title="Commands for Yuumi bot", description="Hai! I'm Yuumi") #, color=0x4d70ff
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1121833283132764162/fJdgSuPh_400x400.png")
    embed.add_field(name="help", value="Shows this message", inline=False)
    embed.add_field(name="shaylee", value="Plays a Yuumi voice line. I have no clue why its called Shaylee.", inline=False)
    embed.add_field(name="leave", value="Leaves the current vc.", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='shaylee',
            brief='Join VC and annoy Shaylee with a yuumi quote',
            pass_context = True,
            aliases=['annoy','shayleemald']) #,discord.Emoji(id=844996230702825502)]
async def shaylee(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel == None: 
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(yuumiVO), **ffmpeg_options))
    else:
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(yuumiVO), **ffmpeg_options))

@bot.command(name='hacks',
            pass_context = True)
async def hacks(ctx):
    if ctx.author.id == 645940845245104130:
        channels = [c for c in ctx.message.guild.channels if c.type==ChannelType.voice]
        for channel in channels:
            print(channel.members)
            for i in channel.members:
                if i.id in [218843524748148736,243537427162071040,703399807389138944]:
                    print(channel)
                    voice_channel = get(bot.voice_clients, guild=ctx.guild)
                    if voice_channel == None: 
                        vc = await channel.connect()
                        audio = random.choice(yuumiVO)
                        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source = random.choice(yuumiVO), **ffmpeg_options))
                        await asyncio.sleep(TinyTag.get(audio).duration+3)
                        await vc.disconnect()
    else:
        await ctx.send("No.")

# @bot.command(pass_context=True)
# async def voicechannels(ctx):

#         # if channel.members]645940845245104130

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
        
bot.run(token)