import asyncio
from discord.ext import commands

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='start', help='(ie. !start 1): Starts a time for 1 minutes')
    async def start_timer(self, ctx, *, mins: float):
        await ctx.send("Timer started! Do good work!")
        await asyncio.sleep(mins * 60)
        await ctx.send(f'<@{ctx.author.id}> Good job! Hopefully you got a lot done!')

    @commands.command(name='end', help='(ie. !end): Ends the timer early')
    async def end_timer(self, ctx):
        await ctx.send("Why are you ending early :angry:")

def setup(bot):
    bot.add_cog(Timer(bot))