
from multiprocessing import context
from typing_extensions import Self
import discord
from discord.ext import commands
import random
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import tasks
from itertools import cycle
from discord.errors import Forbidden
from random import choice
import aiohttp
import json
import os
import datetime
import warnings
from datetime import datetime
from discord_slash import SlashCommand

from discord import message
client = commands.Bot(command_prefix=".")
client.remove_command("help")
slash = SlashCommand(client, )
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(' .help (creavite.co)'))
    print("The bot is ready.")

@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")

@client.command()
async def ping(ctx):
    await ctx.send(f'The bots ping is {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['certainly ' , 'maybe' , ' nope' , 'definitely' , 'sure' , 'not at all' , 'possibly' , 'likely to happen' , 'very unlikely' , '99% not happening']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
@has_permissions(manage_roles=True, kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
@has_permissions(manage_roles=True, ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command(pass_context = True)
async def mute(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator:
        role = discord.utils.get(member.server.roles, name='Muted')
        await ctx.add_roles(member, role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await ctx.send(embed=embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await ctx.send(embed=embed)

@client.command('role')
@commands.has_permissions(administrator=True) #permissions
async def role(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | That role is above your top role!**') 
  if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      await ctx.send(f"Removed {role} from {user.mention}")
  else:
      await user.add_roles(role) #adds role if not already has it
      await ctx.send(f"Added {role} to {user.mention}") 
@role.error
async def role_error(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.send('**:x: | You do not have permission to use this command!**')

@client.command()
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
  

@client.command()
async def help(ctx):
    embed=discord.Embed(title=".Help", description="Help command", color=0xd4ba9b)
    embed.add_field(name="🗡️ Moderation", value="Need moderation help? Do .modhelp", inline=False)
    embed.add_field(name="😂 Fun", value="Need help with fun? Do .funhelp", inline=False)
    embed.add_field(name="🚧 Host", value="auto.creavite.co", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.red()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value="Padds", inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)

@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command()
async def givenum(ctx):

    # checks the author is responding in the same channel
    # and the message is able to be converted to a positive int
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type a number")
    msg1 = await client.wait_for("message", check=check)
    await ctx.send("Type a second, larger number")
    msg2 = await client.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"You got {value}.")
    else:
        await ctx.send(":warning: Please ensure the first number is smaller than the second number.")
@client.command()
async def funhelp(ctx):
    embed=discord.Embed(title=".funhelp", description="Fun Help", color=0xd4ba9b)
    embed.add_field(name="🚀 8BALL", value=".8ball", inline=False)
    embed.add_field(name="🌌 Random Number Generator", value=".givenum", inline=False)
    embed.add_field(name="💀 Memes", value=".meme", inline=False)
    embed.add_field(name="🎮 Latency", value=".ping", inline=False)
    embed.add_field(name="🖥️ Server Info", value=".serverinfo", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def modhelp(ctx):
    embed=discord.Embed(title=".modhelp", description="Mod Help", color=0xd4ba9b)
    embed.add_field(name="🛡️ Ban", value=".ban @user", inline=False)
    embed.add_field(name="🪓 Kick", value=".kick @user", inline=False)
    embed.add_field(name="🔨 Purge", value=".clear amount", inline=False)
    embed.add_field(name="⏲️ Slowmode", value=".setdelay amount", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def startshift(ctx):
    embed=discord.Embed(title="ER:LC Server Shift", description="server name shift")
    embed.add_field(name="👨‍💼 You have now entered a staff shift!", value="Please join the staff team and get to work. ", inline=False)
    embed.add_field(name="❌ Remember ", value=f"{ctx.author.mention} Starting a shift without being online may lead to a staff strike or a demotion", inline=False)
    embed.add_field(name="🕴️ Reminder", value="You must stay professional at all times while being online!", inline=True)
    embed.add_field(name="🔨 Note", value="You are not invincible to warnings etc.", inline=True)
    await ctx.send(embed=embed)
    await ctx.send(("command used" f'<t:{int(datetime.now().timestamp())}:R>'))


@client.command()
async def endshift(ctx):
    embed=discord.Embed(title="ER:LC Server Shift", description="server name shift")
    embed.add_field(name="👨‍💼 You have now finsihed a shift!", value="Please join the staff team and get to work. ", inline=False)
    embed.add_field(name="❌ Remember ", value=f"{ctx.author.mention} Ending a shift while still being on staff team may lead to a strike or a demotion!", inline=False)
    embed.add_field(name="🕴️ Reminder", value="You cannot use commands while being on duty!", inline=True)
    embed.add_field(name="🔨 Note", value="You are not invincible to warnings etc.", inline=True)
    await ctx.send(embed=embed)
    await ctx.send (f'{ctx.author.mention} started a shift')
    await ctx.send(f'<t:{int(datetime.now().timestamp())}:R>')

token = "OTc5NDczMTExNjA5MTIyODc3.GFSXgQ.MMi1LQdLBvVkIPFKeOJsALVi4y3gCKWpV3BNDw"
client.run(token)

