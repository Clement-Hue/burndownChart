import os
from burndown import create_and_save, tasks_to_string, add_task, task_done

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def chart(ctx):
    create_and_save()
    await ctx.send(file=discord.File('burndown.png'))

@bot.command()
async def tasks(ctx):
    await ctx.send(tasks_to_string())

@bot.command()
async def add(ctx, task, point):
    add_task(task, int(point))

@bot.command()
async def done(ctx, id):
    task_done(int(id))


bot.run(TOKEN, bot=True)