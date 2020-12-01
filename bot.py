import discord
import asyncio
from discord.ext.commands import has_permissions
from discord.ext import commands
import os
import random
import time
import json
from PIL import Image, ImageDraw, ImageFilter,ImageFont
from time import sleep
import requests
import shutil
from bs4 import BeautifulSoup
from igramscraper.instagram import Instagram


intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!!", intents = intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("bot online")

@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
            users = json.load(f)
    url = str(member.avatar_url)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    imagea = requests.get(url, headers=user_agent, stream=True)
    file = open('avatar.png', 'wb')
    imagea.raw.decode_content = True
    shutil.copyfileobj(imagea.raw, file)
    file.close()
    im1= Image.open("bg.png")
    im2= Image.open("avatar.png")
    newsize = (200, 200)
    im2 = im2.resize(newsize)
    welcome_pic = im1.copy()
    welcome_pic.paste(im2, (50, 50))
    draw = ImageDraw.Draw(welcome_pic)
    font = ImageFont.truetype("Sanlulus-Light.ttf", 60)
    draw.text((260, 125),"{} JUST JOINED!!!".format(member),(255,255,255),font=font)
    pic = welcome_pic.save('welcome_pic.png', quality=95)
    if users[str(member.guild.id)]["server"]["welcome_channel"] == "none":
        if users[str(member.guild.id)]["server"]["welcome_message"] == "none":
            await member.guild.system_channel.send("{} just joined {}!! Enjoy your stay! :heart:".format(member.mention, member.guild))
        else:
            await member.guild.system_channel.send(users[str(member.guild.id)]["server"]["welcome_message"])
        await member.guild.system_channel.send(file=discord.File('welcome_pic.png'))
    else:
        channel = bot.get_channel(int(users[str(member.guild.id)]["server"]["welcome_channel"]))
        if users[str(member.guild.id)]["server"]["welcome_message"] == "none":
            await channel.send("{} just joined {}!! Enjoy your stay! :heart:".format(member.mention, member.guild))
        else:
            await channel.send(users[str(member.guild.id)]["server"]["welcome_message"])
        await channel.send(file=discord.File('welcome_pic.png'))


@bot.event
async def on_member_remove(member):
    with open('users.json', 'r') as f:
            users = json.load(f)
    if users[str(member.guild.id)]["server"]["leave_channel"] == "none":
        if users[str(member.guild.id)]["server"]["leave_message"] == "none":
            await member.guild.system_channel.send("{} just left the server :broken_heart:".format(member.mention))
        else:
            await member.guild.system_channel.send(users[str(member.guild.id)]["server"]["leave_message"])
    else:
        channel = bot.get_channel(int(users[str(member.guild.id)]["server"]["leave_channel"]))
        if users[str(member.guild.id)]["server"]["leave_message"] == "none":
            await channel.send("{} just left the server :broken_heart:".format(member.mention))
        else:
            await channel.send(users[str(member.guild.id)]["server"]["leave_message"])


async def update_data(users, user, server_id):
    if str(user.id) in users[str(server_id)]["members"]:
        pass
    elif user.bot:
        pass
    else:
        users[str(server_id)]["members"][str(user.id)]={}
        users[str(server_id)]["members"][str(user.id)]["experience"] = 0
        users[str(server_id)]["members"][str(user.id)]["level"] = 1
        users[str(server_id)]["members"][str(user.id)]["messages"] = 0


async def add_stats(users, user, exp, message, server_id):
    if not user.bot :
    	users[str(server_id)]["members"][str(user.id)]["experience"] += exp
    	users[str(server_id)]["members"][str(user.id)]["messages"]  += message


async def level_up(users, user, channel, server_id):
    if user.bot:
        pass
    else :
        experience = users[str(server_id)]["members"][str(user.id)]["experience"]
        messages = users[str(server_id)]["members"][str(user.id)]["messages"]
        lvl_start = users[str(server_id)]["members"][str(user.id)]["level"]
        level = users[str(server_id)]["members"][str(user.id)]["level"]
        lvl_end = 500*level
        int(level)
        if experience >= lvl_end:
            level = level + 1
            print ("{} Leveled up {}".format(user.mention, level))
            users[str(server_id)]["members"][str(user.id)]["level"] = level

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)

    with open('users.json', 'r') as f:
        users = json.load(f)

    if str(ctx.guild.id) not in users:
        users[str(ctx.guild.id)] = {}
        users[str(ctx.guild.id)]["members"]={}
        users[str(ctx.guild.id)]["server"]={}
        users[str(ctx.guild.id)]["server"]["welcome_channel"]="none"
        users[str(ctx.guild.id)]["server"]["welcome_message"]="none"
        users[str(ctx.guild.id)]["server"]["leave_channel"]="none"
        users[str(ctx.guild.id)]["server"]["leave_message"]="none"

    try :
        test=users[str(ctx.guild.id)]["server"]["welcome_message"]
        test=users[str(ctx.guild.id)]["server"]["welcome_channel"]
        test=users[str(ctx.guild.id)]["server"]["leave_channel"]="none"
        test=users[str(ctx.guild.id)]["server"]["leave_message"]="none"
    except:
        users[str(ctx.guild.id)]["server"]["welcome_channel"]="none"
        users[str(ctx.guild.id)]["server"]["welcome_message"]="none"
        users[str(ctx.guild.id)]["server"]["leave_channel"]="none"
        users[str(ctx.guild.id)]["server"]["leave_message"]="none"

    await update_data(users, ctx.author, ctx.guild.id)
    await add_stats(users, ctx.author, random.randint(6,8), 1, ctx.guild.id)
    await level_up(users, ctx.author, ctx, ctx.guild.id)


    with open('users.json', 'w') as f:
        json.dump(users, f)

async def show_xp(ctx, users, user, channel, server_id):

        experience = users[str(server_id)]["members"][str(user.id)]["experience"]
        level = users[str(server_id)]["members"][str(user.id)]["level"]
        messages = users[str(server_id)]["members"][str(user.id)]["messages"]
        username = ctx.message.author.name
        xp_next_level = int(500*level)
        xp_last_level = int(500*(level-1))
        xp_needed = xp_next_level - experience

        if level == 1:
            xp_last_level=0
            xp_next_level=500
            xp_needed=500-experience
        else:
            xp_next_level = int(500*level)
            xp_last_level = int(500*(level-1))


        if level == 1:
            pourcent = int((100*(xp_last_level + xp_needed))/(500))
        else:
            pourcent = int((100*(xp_last_level + xp_needed))/(500))

        pourcent = pourcent-(level*100)
        pourcent = pourcent+100
        pourcent_real = 100 - pourcent
        pourcent_bar_diff = int((100-pourcent)/3.6)
        pourcent_bar = int(pourcent/3.6)
        complete = "█"*pourcent_bar_diff
        not_complete = " -"*pourcent_bar
        Embed = discord.Embed(colour = discord.Colour.blue())
        Embed.set_author(name="{}'S RANK".format(user[:-5]))
        Embed.add_field(name='LEVEL :', value='{}'.format(level), inline=True)
        Embed.add_field(name='TOTAL XP :', value='{}'.format(experience), inline=True)
        Embed.add_field(name='MESSAGES SENT :',value='{}'.format(messages),inline=True)
        Embed.add_field(name='PROGRESSION :', value='| {}{} | {} %'.format(complete, not_complete, pourcent_real), inline=False)
        Embed.add_field(name='XP NEEDED :', value='{} % ({}xp) Left | {}xp/{}xp'.format(pourcent, xp_needed, experience, xp_next_level), inline=False)
        Embed.set_footer(text="To earn XP, you need to chat. When a message is sent, you can earn between 6 and 8 XP. You need 500 XP to level up.")
        await channel.send(embed=Embed)
        print ("LEVEL : {} ; XP : {}".format(level,experience))


@bot.command(pass_context = True)
async def rank(ctx, user: discord.Member=None):
    if user is None :
    	with open('users.json', 'r') as f:
            	users = json.load(f)
    	await show_xp(ctx, users, ctx.author,ctx.channel, ctx.guild.id)
    else:
        with open('users.json', 'r') as f:
            	users = json.load(f)
        await show_xp(ctx, users, user,ctx.channel,ctx.guild.id)

#@bot.command(pass_context=True)
#async def leaderboards(ctx):
    #with open('users.json', 'r') as fp:
        #users = json.load(fp)
    #embed = discord.Embed(title='Server leaderboard', color=random.randint(0,16777215))
    #sorted(users, key=lambda x : users[x].get('experience', 0), reverse=True)
    #high_score_list = sorted(users, key=lambda x : users[x].get('experience', 0), reverse=True)
    #message = ''
    #for number, user in enumerate(high_score_list):
        #user_object =  bot.get_user(user)
        #embed.add_field(name='{}, {}'.format(number + 1,user_object.name), value='{}'.format(str(users[user].get('experience', 0))+'xp'), inline=True)
    #await ctx.send(embed=embed)

@bot.command(aliases=['lb','leaderboard'])
async def leaderboards(ctx):
    x = 0
    y = 0
    with open('users.json', 'r') as fp:
        users = json.load(fp)
    img = Image.open(r'backgtudn imge')
    font = ImageFont.truetype(r'font', 100)
    d = ImageDraw.Draw(img)
    sorted(users, key=lambda x : users[x].get('experience', 0), reverse=True)
    high_score_list = sorted(users, key=lambda x : users[x].get('experience', 0), reverse=True)
    for number, user in enumerate(high_score_list):
        if number == 10:
            break
        else:
            print(user)
            user_object = bot.get_user(int(user))
            if user_object == None:
                pass
            else:
                name = user_object.name
                d.text((x,y), "{}. {} {}xp".format(number+1,name, str(users[user].get('experience', 0)), font = font, fill=(255,255,255)),font=font,align ='center')
                y = y + 100
    img.save('okay.png')
    await ctx.send(file=discord.File('okay.png'))


@bot.command(pass_context=True)
async def test(ctx):
    url = str(ctx.author.avatar_url)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    imagea = requests.get(url, headers=user_agent, stream=True)
    file = open('avatar.png', 'wb')
    imagea.raw.decode_content = True
    shutil.copyfileobj(imagea.raw, file)
    file.close()
    im1= Image.open("bg.png")#change dir
    im2= Image.open("avatar.png")
    newsize = (200, 200)
    im2 = im2.resize(newsize)
    welcome_pic = im1.copy()
    welcome_pic.paste(im2, (50, 50))
    draw = ImageDraw.Draw(welcome_pic)
    font = ImageFont.truetype("Sanlulus-Light.ttf", 60)
    draw.text((260, 125),"{} JUST JOINED!!!".format(ctx.author),(255,255,255),font=font)
    pic = welcome_pic.save('welcome_pic.png', quality=95)
    await ctx.send(file=discord.File('welcome_pic.png'))


@bot.command(pass_context=True)
async def help(ctx):
    await ctx.send("help")


#server admins
@bot.command(pass_context=True)
@has_permissions(manage_channels=True)
async def set(ctx, arg1, arg2):
        with open('users.json', 'r') as f:
                users = json.load(f)

        #WELCOME
        if arg1.upper() == "WELCOME_CHANNEL":
            if arg2.upper()=="DEFAULT":
                users[str(ctx.guild.id)]["server"]["welcome_channel"]="none"
                await ctx.send("The welcome channel was successfully been set to default")
            else:
                await ctx.send("The welcome channel was successfully changed")
                users[str(ctx.guild.id)]["server"]["welcome_channel"]=arg2

        if arg1.upper() == "WELCOME_MESSAGE":
            if arg2.upper()=="DEFAULT":
                users[str(ctx.guild.id)]["server"]["welcome_message"]="none"
                await ctx.send("The welcome message was successfully been set to default")
            else:
                users[str(ctx.guild.id)]["server"]["welcome_message"]=arg2
                await ctx.send("The welcome message was successfully changed")

        #LEAVE
        if arg1.upper() == "LEAVE_CHANNEL":
            if arg2.upper()=="DEFAULT":
                users[str(ctx.guild.id)]["server"]["leave_channel"]="none"
                await ctx.send("The leave channel was successfully been set to default")
            else:
                users[str(ctx.guild.id)]["server"]["leave_channel"]=arg2
                await ctx.send("The leave channel was successfully changed")

        if arg1.upper() == "LEAVE_MESSAGE":
            if arg2.upper()=="DEFAULT":
                users[str(ctx.guild.id)]["server"]["leave_message"]="none"
                await ctx.send("The leave message was successfully been set to default")
            else:
                users[str(ctx.guild.id)]["server"]["leave_message"]=arg2
                await ctx.send("The leave message was successfully changed")

        with open('users.json', 'w') as f:
            json.dump(users, f)


@bot.command(pass_context=True)
async def kick(ctx, user:discord.Member, *, reason=None):
    try :
        if discord.Permissions.kick_members:
            await user.kick(reason=reason)
            embed=discord.Embed(title="Kick", description="{} Just got kicked by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
            embed.set_footer(text="Reason : {}".format(reason))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Kick", description="You do not have permissions to kick members", color=0x0a0a0a)
            await ctx.send(embed=embed)
    except :
        embed=discord.Embed(title="Kick", description="You cannot kick a staff member", color=0x0a0a0a)
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def ban(ctx, user:discord.Member, *, reason=None):
    try :
        if discord.Permissions.ban_members:
            await user.ban(reason=reason)
            embed=discord.Embed(title="Ban", description="{} Just got banned by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
            embed.set_footer(text="Reason : {}".format(reason))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Ban", description="You do not have permissions to ban members", color=0x0a0a0a)
            await ctx.send(embed=embed)
    except :
        embed=discord.Embed(title="Ban", description="You cannot ban a staff member", color=0x0a0a0a)
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def unban(ctx, id: int):
    if discord.Permissions.ban_members:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed=discord.Embed(title="Unban", description="{} Just got unbanned by {}".format(user.mention, ctx.author.mention), color=0x0a0a0a)
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def instagram(ctx, arg):
    instagram = Instagram()
    instagram.with_credentials("place_bot_", "20040322")
    instagram.login()

    account = instagram.get_account(arg)


    private="No"
    verified="No"

    if account.is_private:
        private="Yes"
    if account.is_verified:
        verified="Yes"

    embed=discord.Embed(title=f"{account.full_name}", url=f"https://www.instagram.com/{account.username}/", description=f"{account.biography}", color=0xea1084)
    embed.set_author(name=f"{account.username}'s Instagram")
    embed.set_thumbnail(url=f"{account.get_profile_picture_url()}")
    embed.add_field(name="Posts", value=f"{account.media_count}", inline=True)
    embed.add_field(name="Followers", value=f"{account.followed_by_count}", inline=True)
    embed.add_field(name="Following", value=f"{account.follows_count}", inline=True)
    embed.add_field(name="Private", value=f"{private}", inline=True)
    embed.add_field(name="Verified", value=f"{verified}", inline=True)
    embed.set_footer(text=f"Command requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def steam(ctx, arg):
    pass


token = open("token.txt", "r")

bot.run(token.read())
