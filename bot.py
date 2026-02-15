import discord
from discord.ext import tasks
from discord import app_commands
import datetime
import pytz
import random
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 123456789012345678  # Your server ID
CHANNEL_ID = 123456789012345678  # Channel where pics get sent
AUTHORIZED_ROLE_NAME = "Inner Circle"  # Role that can use command

CENTRAL = pytz.timezone("US/Central")

IMAGE_URLS = [
    "https://upload.wikimedia.org/wikipedia/commons/3/35/Benjamin_Netanyahu_2018.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/0d/Benjamin_Netanyahu_2021.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/5d/Netanyahu_2012.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Benjamin_Netanyahu_2015.jpg"
]

intents = discord.Intents.default()
intents.members = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

bot = MyBot()

# ---- DAILY AUTO POST ----

@tasks.loop(minutes=1)
async def daily_post():
    now = datetime.datetime.now(CENTRAL)

    if now.hour == 12 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            image_url = random.choice(IMAGE_URLS)

            embed = discord.Embed(
                title="Daily Netanyahu Drop",
                description="12:00 PM Central Time"
            )
            embed.set_image(url=image_url)

            await channel.send(embed=embed)

# ---- SLASH COMMAND ----

@bot.tree.command(name="sendpic", description="Send a Netanyahu picture", guild=discord.Object(id=GUILD_ID))
async def sendpic(interaction: discord.Interaction):
    user_roles = [role.name for role in interaction.user.roles]

    if AUTHORIZED_ROLE_NAME not in user_roles:
        await interaction.response.send_message(
            "You do not have permission to use this command.",
            ephemeral=True
        )
        return

    image_url = random.choice(IMAGE_URLS)

    embed = discord.Embed(title="Manual Netanyahu Drop")
    embed.set_image(url=image_url)

    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not daily_post.is_running():
        daily_post.start()

bot.run(TOKEN)
