import os
from datetime import datetime, timedelta
import asyncio
import discord
from jsonLoader import JsonLoader
from task import Task
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def chart(ctx, name):
    loader = JsonLoader(f"./data/{name}.json")
    burden = loader.load_burden()
    burden.create_chart()
    await ctx.send(file=discord.File(f'./burndown/{name}.png'))


@bot.command()
async def tasks(ctx, name):
    burden = JsonLoader(f"./data/{name}.json").load_burden()
    await ctx.send(burden.__str__())


@bot.command()
async def add(ctx, name, task, point):
    loader = JsonLoader(f"./data/{name}.json")
    burden = loader.load_burden()
    burden.listTask.add_task(Task(task=task, point=int(point)))
    await ctx.send("tâche ajouté")


@bot.command()
async def done(ctx, name, id):
    loader = JsonLoader(f"./data/{name}.json")
    burden = loader.load_burden()
    burden.listTask.set_task_done(int(id))
    await ctx.send(f"tache {id} mis à jour")


@bot.command()
async def remove(ctx, name, id):
    loader = JsonLoader(f"./data/{name}.json")
    burden = loader.load_burden()
    burden.listTask.remove_task((int(id)))
    await ctx.send(f"tache {id} retiré")


@bot.command()
async def progress(ctx, name):
    loader = JsonLoader(f"./data/{name}.json")
    burden = loader.load_burden()
    await ctx.send(burden.progression())



bot.run(TOKEN, bot=True)
