import discord
import asyncio
from discord.ext import commands
import os
import random
import time
import json
from PIL import Image, ImageDraw, ImageFilter,ImageFont, ImageOps
from time import sleep
import requests
import shutil




bot = commands.Bot(command_prefix='!!')



@bot.event
async def on_ready():
    print("bot online")



@bot.event
async def on_member_join(member):
    size_img=(1000,300)
    channel = bot.get_channel(747925331243171970)
    channel.send('Welcome to the server {}'.format(member.name))
    img = Image.open(r'Directory to background image') #1000x300
    font = ImageFont.truetype(r'Directory to font', 100)
    d = ImageDraw.draw(img)
    d.text((0,0), '{}', font = font, fill=(255,255,255))
    img.thumbnail(size_img)
    img.save('welcome_img.png')
    channel.send(file=discord.File('welcome_img.png'))



@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(747925331243171970)
    channel.send('{} left okay'.format(member.name))
    img = Image.open(r'Directory to background image')  #1080p
    font = ImageFont.truetype(r'Directory to font', 100)
    d = ImageDraw.draw(img)
    d.text((0,0), '{} left okauy7', font = font, fill=(255,255,255))
    img.save('okay.png')
    channel.send(file=discord.File('okay.png'))



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


    await update_data(users, ctx.author, ctx.guild.id)
    await add_stats(users, ctx.author, random.randint(6,8), 1, ctx.guild.id)
    await level_up(users, ctx.author, ctx, ctx.guild.id)

    with open('users.json', 'w') as f:
        json.dump(users, f)

#lol

async def show_xp(ctx, users, user, channel):
        server_id = ctx.guild.id
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
        Embed.set_author(name="{}'S RANK".format(user))
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
    	await show_xp(ctx, users, ctx.author,ctx.channel)
    else:
        with open('users.json', 'r') as f:
            	users = json.load(f)
        await show_xp(ctx, users, user,ctx.channel)

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
    im1= Image.open("C:/Users/GW Andrew/Documents/Place Bot/bg.png")#change dir
    im2= Image.open("C:/Users/GW Andrew/Documents/Place Bot/avatar.png")
    newsize = (200, 200) 
    im2 = im2.resize(newsize) 
    welcome_pic = im1.copy()
    welcome_pic.paste(im2, (50, 50))
    pic = welcome_pic.save('C:/Users/GW Andrew/Documents/Place Bot/welcome_pic.png', quality=95)
    await ctx.send(file=discord.File('C:/Users/GW Andrew/Documents/Place Bot/welcome_pic.png'))



bot.run("NzQ3ODIzNDgyMDk5OTkwNzA5.X0Ue5A.mtB1y7V4AAR1y49I19oXYyc66MA")
