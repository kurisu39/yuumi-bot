
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import glob
import asyncio
from discord import ChannelType
import time


from voicelines import voiceLines
import random
import os

token = "ODIxMTEwNzAyMTA2MzQ1NTMz.YE-87g.PHpMgIL9bI5O9-qf-M2H6vsOrdU"

yuumiVO = glob.glob("audio/*.ogg")
bot = discord.Client()
bot = commands.Bot(command_prefix='!')
ffmpeg_options = {'options': '-filter:a "volume=0.25"'}
bot.remove_command('help')
yuumiwords = ["allan","yuumi","mald","cat","book"]

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status = discord.Status.online, activity=discord.Game('Metal is perfection.'))


# @bot.event
# async def on_member_join(member):
#     await member.send('Private message')

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

@bot.command(pass_context=True)
async def voicechannels(ctx):
    channels = [c for c in ctx.message.guild.channels if c.type==ChannelType.voice]
    for channel in channels:
        print(channel.members)
        for i in channel.members:
            if i.id == 645940845245104130:
                print(channel.id)
        # if channel.members]645940845245104130

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