import discord
import asyncio
import ping3
import os
import dotenv
from dotenv import load_dotenv
from ping3 import ping, verbose_ping
from log import Log
from datetime import date, datetime, timedelta
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORDTOKEN")
reactioncheck = int(os.getenv("REACTIONCHECK"))
reaction = int(os.getenv("REACTIONCHANNEL"))
antispam = int(os.getenv("ANTISPAM"))
timeout = int(os.getenv("TIMEOUT"))
botprefix = os.getenv("BOTPREFIX")

bot = commands.Bot(command_prefix=botprefix)
bot.remove_command("help")

servers = [
    "fnk1.playit.gg",
    "sng1.playit.gg",
    "bng1.playit.gg",
    "ny1.playit.gg",
    "sf1.playit.gg",
    "syd1.playit.gg",
    "ams1.playit.gg"
]

logs = {}

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'Bot is ready')
    await bot.change_presence(activity=discord.Game(name=f'Suggestion Bot'))

@bot.event
async def on_member_join(member):
    await member.send("Welcome to Playit.gg! Hope you enjoy your stay")

@bot.event
async def on_message(message):
    if reactioncheck == 1:
        if message.channel.id == reaction:
            await message.add_reaction('✅')
            await message.add_reaction('❌')
    if antispam == 1:
        if message.author == bot.user:
            return
        if message.author.id in logs:
            delta = message.created_at-logs[message.author.id].lastMessage
            userid = message.author.id
            if delta.seconds < timeout:
                logs[message.author.id].violations += 1
                await message.delete()
                await(await message.channel.send(f'<@!{userid}> no spamming allowed!'.format(message.author))).delete(delay=5)
                await asyncio.sleep(4)
            logs[message.author.id].lastMessage = message.created_at
        else:
            logs[message.author.id] = Log(message.created_at)
    await bot.process_commands(message)


@bot.command(name="ping")
async def _ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

#member: Optional[discord.Member]=None IF I HAVE ANY FURTHER ARGUMENTS to help me in the future
@bot.command(pass_context=True)
async def checkspam(ctx, member : discord.Member= None):
    if antispam == 1:
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
    embed=discord.Embed(title="Playit.gg", url="https://playit.gg", color=0xff8000)
    embed.set_author(name="Playit Support Bot",icon_url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.add_field(name="```!help```", value="Shows this message", inline=False)
    embed.add_field(name="```!website```", value="Shows the Playit.gg website link", inline=False)
    embed.add_field(name="```!ping```", value="Shows the ping of the bot", inline=False)
    embed.add_field(name="```!checkspam```", value="Shows how many violations the user has on spam", inline=False)
    embed.add_field(name="```!status```", value="Shows the status of all Playit.gg servers", inline=False)
    embed.set_footer(text="If you need any help with commands contact the support team")
    await ctx.send(embed=embed)


@bot.command()
async def website(ctx):
    await ctx.send('https://playit.gg')

@bot.command()
async def status(ctx):
    serverpings=[]
    for x in servers:
        myping = round(ping(x) * 1000, 2)
        if myping > 0:
            myping = 'Online'
        else:
            myping = 'Offline'
        serverpings.append(myping)
    embed=discord.Embed(title="Playit.gg", url="https://playit.gg", description=" ", color=0xff8000)
    embed.set_author(name="Playit.gg Status",icon_url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
    embed.add_field(name="FNK1 - Germany", value=serverpings[0], inline=False)
    embed.add_field(name="SNG1 - Singapore", value=serverpings[1], inline=False)
    embed.add_field(name="BNG1 - Bangalore", value=serverpings[2], inline=False)
    embed.add_field(name="NY1 - New York", value=serverpings[3], inline=False)
    embed.add_field(name="SF1 - San Francisco", value=serverpings[4], inline=False)
    embed.add_field(name="SYD1 - Sydney", value=serverpings[5], inline=False)
    embed.add_field(name="AMS1 - Amsterdam", value=serverpings[6], inline=False)
    embed.set_footer(text="Playit.gg Status (THIS IS THE BOTS STATUS ON THE SERVERS NOT YOU)")
    startmsg = await ctx.send(embed=embed)
    await startmsg.add_reaction('🏠')
    await startmsg.add_reaction('📊')
    while True:
        onlineemoji = ['🏠']
        pingemoji = ['📊']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == startmsg.id and user.bot is not True:
            if str(reaction.emoji) in onlineemoji:
                await reaction.message.remove_reaction('🏠', user)
                await startmsg.add_reaction('📊')
                serverpings=[]
                for x in servers:
                    myping = round(ping(x) * 1000, 2)
                    if myping > 0:
                       myping = 'Online'
                    else:
                        myping = 'Offline'
                    serverpings.append(myping)
                embed=discord.Embed(title="Playit.gg", url="https://playit.gg", description=" ", color=0xff8000)
                embed.set_author(name="Playit.gg Status",icon_url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
                embed.add_field(name="FNK1 - Germany", value=serverpings[0], inline=False)
                embed.add_field(name="SNG1 - Singapore", value=serverpings[1], inline=False)
                embed.add_field(name="BNG1 - Bangalore", value=serverpings[2], inline=False)
                embed.add_field(name="NY1 - New York", value=serverpings[3], inline=False)
                embed.add_field(name="SF1 - San Francisco", value=serverpings[4], inline=False)
                embed.add_field(name="SYD1 - Sydney", value=serverpings[5], inline=False)
                embed.add_field(name="AMS1 - Amsterdam", value=serverpings[6], inline=False)
                embed.set_footer(text="Playit.gg Status (THIS IS THE BOTS STATUS ON THE SERVERS NOT YOU)")
                await startmsg.edit(embed=embed)
            if str(reaction.emoji) in pingemoji:
                await reaction.message.remove_reaction('📊', user)
                await startmsg.add_reaction('🏠')
                serverpings=[]
                for x in servers:
                    myping = round(ping(x) * 1000, 2)
                    serverpings.append(myping)
                embed=discord.Embed(title="Playit.gg", url="https://playit.gg", description="All values are in ms", color=0xff8000)
                embed.set_author(name="Playit.gg Status",icon_url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/686968015715172423/549bbcb96439ceb83ee39346f070e34c.png?size=128")
                embed.add_field(name="FNK1 - Germany", value=serverpings[0], inline=False)
                embed.add_field(name="SNG1 - Singapore", value=serverpings[1], inline=False)
                embed.add_field(name="BNG1 - Bangalore", value=serverpings[2], inline=False)
                embed.add_field(name="NY1 - New York", value=serverpings[3], inline=False)
                embed.add_field(name="SF1 - San Francisco", value=serverpings[4], inline=False)
                embed.add_field(name="SYD1 - Sydney", value=serverpings[5], inline=False)
                embed.add_field(name="AMS1 - Amsterdam", value=serverpings[6], inline=False)
                embed.set_footer(text="Playit.gg Status (THIS IS THE BOTS PING ON THE SERVERS NOT YOU)")
                await startmsg.edit(embed=embed)
                await startmsg.add_reaction('🏠')

#@bot.command()
#async def new(ctx, member: discord.Member = None):
#    await ctx.send('A ticket has been made!')
#    if member == None:
#        member = ctx.message.author
#    server = ctx.message.guild
#    createchannel = await server.create_text_channel(f"ticket-{member.display_name}")
#    embed = discord.Embed(title=f"New ticket created",
 #                         description=f"Hello {member.mention}, A support member will be with you soon.", color=0xff8000)
 ##   embed.set_footer(text=f"Ticket number: {createchannel.id}", icon_url=member.avatar_url)
#    staff = discord.utils.get(ctx.message.author.guild.roles, name="moderator")
#    contributor = discord.utils.get(ctx.message.author.guild.roles, name="contributor")
#    dev = discord.utils.get(ctx.message.author.guild.roles, name="code slinger")
#    everyone = ctx.message.author.guild.default_role
#    disallow = discord.PermissionOverwrite()
#    disallow.read_messages = False
#    disallow.send_messages = False
#    allow = discord.PermissionOverwrite()
#    allow.read_messages = True
#    allow.send_messages = True
#    await createchannel.set_permissions(everyone, overwrite=disallow)
#    await createchannel.set_permissions(ctx.message.author, overwrite=allow)
#    await createchannel.set_permissions(staff, overwrite=allow)
#    await createchannel.set_permissions(contributor, overwrite=allow)
#    await createchannel.set_permissions(dev, overwrite=allow)
#    await createchannel.send(embed=embed)

#@bot.command()
#async def close(ctx):
#    staff = discord.utils.get(ctx.message.author.guild.roles, name="moderator")
#    contributor = discord.utils.get(ctx.message.author.guild.roles, name="contributor")
#    dev = discord.utils.get(ctx.message.author.guild.roles, name="code slinger")
#    if staff in ctx.author.roles:
#        channel = ctx.message.channel
#        embed = discord.Embed(
#            title="Closing ticket", description="This ticket will be closed in 60 seconds", color=0xff8000)
#        await ctx.send(embed=embed)
#        await asyncio.sleep(60)
#        await channel.delete(reason="Ticket closed")
#    if contributor in ctx.author.roles:
#        channel = ctx.message.channel
#        embed = discord.Embed(
#            title="Closing ticket", description="This ticket will be closed in 60 seconds", color=0xff8000)
#        await ctx.send(embed=embed)
#        await asyncio.sleep(60)
#        await channel.delete(reason="Ticket closed")
#    if dev in ctx.author.roles:
#        channel = ctx.message.channel()
#        embed = discord.Embed(
#            title="Closing ticket", description="This ticket will be closed in 60 seconds", color=0xff8000)
#        await ctx.send(embed=embed)
#        await asyncio.sleep(60)
#        await channel.delete(reason="Ticket closed")
#    else:
#        await ctx.send(":x: You do not have permission to do that.")

async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(name=f'Suggestion Bot'))
        await bot.change_presence(activity=discord.Game(name=f'!help'))
        await bot.change_presence(activity=discord.Game(name=f'Playit.gg'))
        await asyncio.sleep(8)

bot.loop.create_task(background_task())

bot.run(TOKEN.strip())
