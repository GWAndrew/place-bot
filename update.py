import os

os.system("git pull origin master")
os.system("pkill -f bot.py")
os.system("python3 bot.py")

print("BOT RESTARTED SUCCESSFULLY")
