import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.todo import Todo
from cogs.timer import Timer

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.wait_until_ready()
    await bot.add_cog(Todo(bot))
    await bot.add_cog(Timer(bot))

bot.run(os.getenv('TOKEN'))