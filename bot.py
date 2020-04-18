import discord
from discord.ext import commands
TOKEN = open("discord.key","r").readline()
bot = commands.Bot(command_prefix='!')

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

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')




bot.run(TOKEN.strip())
