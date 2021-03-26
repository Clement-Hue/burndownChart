import os
import discord
from jsonLoader import JsonLoader
from task import Task
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
    loader = JsonLoader("./data/tasks.json")
    burden = loader.load_burden()
    burden.create_chart("ptrans")
    await ctx.send(file=discord.File('./burndown/ptrans.png'))

@bot.command()
async def tasks(ctx):
    burden = JsonLoader("./data/tasks.json").load_burden()
    await ctx.send(burden.listTask.__str__())

@bot.command()
async def add(ctx, task, point):
    loader = JsonLoader("./data/tasks.json")
    burden = loader.load_burden()
    burden.listTask.add_task(Task(task=task, point=int(point)))
    await ctx.send("tâche ajouté")

@bot.command()
async def done(ctx, id,date = None):
    loader = JsonLoader("./data/tasks.json")
    burden = loader.load_burden()
    burden.listTask.set_task_done(int(id), date)
    await ctx.send(f"tache {id} mis à jour")

@bot.command()
async def remove(ctx, id):
    loader = JsonLoader("./data/tasks.json")
    burden = loader.load_burden()
    burden.listTask.remove_task((int(id)))
    await ctx.send(f"tache {id} retiré")

@bot.command()
async def progress(ctx ):
    loader = JsonLoader("./data/tasks.json")
    burden = loader.load_burden()
    await ctx.send(burden.progression())


bot.run(TOKEN, bot=True)