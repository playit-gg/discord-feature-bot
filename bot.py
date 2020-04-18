import discord
import asyncio
from log import Log
from datetime import date, datetime, timedelta
from discord.ext import commands
TOKEN = open("discord.key","r").readline()
bot = commands.Bot(command_prefix='!')

timeout = 4
logs = {}

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'Bot is ready')
    await bot.change_presence(activity=discord.Game(name=f'Suggestion Bot'))

@bot.event
async def on_message(message):
    if message.channel.id == 688834216737505358:
        await message.add_reaction('✅')
        await message.add_reaction('❌')
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.name in logs:
        delta = message.created_at-logs[message.author.name].lastMessage
        userid = message.author.id
        if(delta.seconds < timeout):
            logs[message.author.name].violations += 1
            await message.delete()
            await(await message.channel.send(f'<@!{userid}> no spamming allowed!'.format(message.author))).delete(delay=5)
            await asyncio.sleep(4)
        
        logs[message.author.name].lastMessage = message.created_at
    else:
        logs[message.author.name] = Log(message.created_at)
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def timeoutset(ctx, span : int):
    timeout = span
    await ctx.send('Updated spam timeout to {0} seconds.'.format(timeout))

@bot.command(pass_context=True)
async def checkspam(ctx, member : discord.Member= None):
    name = ctx.author if not member else member
    sub
    print(name)
    if name in logs:
        log = logs[name]
        if log.violations > 0:
            await ctx.send('{} has {1.violations} violations.'.format(name, log))
        else:
            await ctx.send('{} has no violations yet.'.format(name))
    else:
        await ctx.send('No user found or i am a rubbish dev')


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(name=f'Suggestion Bot'))
        await bot.change_presence(activity=discord.Game(name=f'!help'))
        await bot.change_presence(activity=discord.Game(name=f'Playit.gg'))
        await asyncio.sleep(8)

bot.loop.create_task(background_task())

bot.run(TOKEN.strip())