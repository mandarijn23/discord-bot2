import discord
from discord.ext import tasks
import datetime
import pytz
import random

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
CHANNEL_ID = 123456789012345678  # Replace with your channel ID

# Central Time zone
CENTRAL = pytz.timezone("US/Central")

# Image list (replace if you want different ones)
IMAGE_URLS = [
    "https://upload.wikimedia.org/wikipedia/commons/3/35/Benjamin_Netanyahu_2018.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/0d/Benjamin_Netanyahu_2021.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/5d/Netanyahu_2012.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Benjamin_Netanyahu_2015.jpg"
]

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not daily_post.is_running():
        daily_post.start()

@tasks.loop(minutes=1)
async def daily_post():
    now = datetime.datetime.now(CENTRAL)

    if now.hour == 6 and now.minute == 13:
        channel = bot.get_channel(CHANNEL_ID)

        if channel:
            image_url = random.choice(IMAGE_URLS)

            embed = discord.Embed(
                title="Daily Netanyahu Drop",
                description="12:00 PM Central Time"
            )
            embed.set_image(url=image_url)

            await channel.send(embed=embed)

            # Prevent double posting within the same minute
            await discord.utils.sleep_until(
                now.replace(minute=1, second=0) + datetime.timedelta(minutes=1)
            )

bot.run(TOKEN)


