import discord
import asyncio
from log import Log
from datetime import date, datetime, timedelta
from discord.ext import commands
TOKEN = open("discord.key","r").readline()
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")
timeout = 1
logs = {}

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'Bot is ready')
    await bot.change_presence(activity=discord.Game(name=f'Suggestion Bot'))

@bot.event
async def on_message(message):
    reaction = open("reaction.txt","r").readline()
    newreaction = int(reaction)
    if message.channel.id == newreaction:
        await message.add_reaction('✅')
        await message.add_reaction('❌')
    if message.author == bot.user:
        return
    if message.author.id in logs:
        delta = message.created_at-logs[message.author.id].lastMessage
        userid = message.author.id
        if(delta.seconds < timeout):
            logs[message.author.id].violations += 1
            await message.delete()
            await(await message.channel.send(f'<@!{userid}> no spamming allowed!'.format(message.author))).delete(delay=5)
            await asyncio.sleep(4)
        logs[message.author.id].lastMessage = message.created_at
    else:
        logs[message.author.id] = Log(message.created_at)
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def timeoutset(ctx, span : int):
    timeout = span
    await ctx.send('Updated spam timeout to {0} seconds.'.format(timeout))
#member: Optional[discord.Member]=None IF I HAVE ANY FURTHER ARGUMENTS to help me in the future
@bot.command(pass_context=True)
async def checkspam(ctx, member : discord.Member= None):
    name = ctx.author.id if not member else member.id
    if name in logs:
        log = logs[name]
        if log.violations > 0:
            await ctx.send(f'<@!{name}> ''has {1.violations} violations.'.format(name, log))
        else:
            await ctx.send(f'<@!{name}> ''has no violations yet.'.format(name))
    else:
        await ctx.send('No user found or Alienwarez#0711 is a rubbish dev')


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="PlayIt.gg", url="https://playit.gg", color=0xff8000)
    embed.set_author(name="PlayIt Support Bot",icon_url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.add_field(name="!help", value="Shows this message", inline=False)
    embed.add_field(name="!website", value="Shows the Playit.gg website link", inline=False)
    embed.add_field(name="!ping", value="Shows the ping of the bot", inline=False)
    embed.add_field(name="!checkspam", value="Shows how many violations the user has on spam", inline=False)
    embed.set_footer(text="If you need any help with commands contact the support team")
    await ctx.send(embed=embed)

@bot.command()
async def helpadmin(ctx):
    embed=discord.Embed(title="PlayIt.gg", url="https://playit.gg", color=0xff8000)
    embed.set_author(name="PlayIt Support Bot",icon_url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.add_field(name="!help", value="Shows this message", inline=False)
    embed.add_field(name="!website", value="Shows the Playit.gg website link", inline=False)
    embed.add_field(name="!ping", value="Shows the ping of the bot", inline=False)
    embed.add_field(name="!checkspam", value="Shows how many violations the user has on spam", inline=False)
    embed.add_field(name="!timeoutset", value="Sets how many seconds a user can send a message until its considerd spam" , inline=False)
    embed.add_field(name="!setreactionchannel", value="Sets the reaction channel for the bot", inline=False)
    embed.add_field(name="!shutdown", value="Shuts the bot down (Owner Only)", inline=False)
    embed.set_footer(text="If you need any help with commands contact the support team")
    await ctx.send(embed=embed)

@bot.command()
async def setreactionchannel(ctx):
    reactionchannel = ctx.channel.id
    reactionchannelstr = str(reactionchannel)
    w = open('reaction.txt', 'w')
    w.write(reactionchannelstr)
    w.close()
    print(reactionchannel)
    await ctx.send(f"The channel has been set to {ctx.channel}")

@bot.command()
async def website(ctx):
    await ctx.send('https://playit.gg')


async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(name=f'Suggestion Bot'))
        await bot.change_presence(activity=discord.Game(name=f'!help'))
        await bot.change_presence(activity=discord.Game(name=f'Playit.gg'))
        await asyncio.sleep(8)

bot.loop.create_task(background_task())

bot.run(TOKEN.strip())