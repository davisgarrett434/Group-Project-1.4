import discord
import asyncio
import random
import requests
from discord.ext import commands, tasks

TOKEN = "Discord token ADD LATER DO NOT FORGET"
TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"

bot = commands.Bot(command_prefix="!")
current_question = None
current_answer = None


def get_trivia_question():
    global current_question, current_answer
    response = requests.get(TRIVIA_API_URL).json()
    question_data = response["results"][0]
    current_question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    options = question_data["incorrect_answers"] + [correct_answer]
    random.shuffle(options)
    current_answer = correct_answer.lower()
    return current_question, options


tasks.loop(hours=24)
async def post_trivia():
    channel = discord.utils.get(bot.get_all_channels(), name="trivia")
    if channel:
        question, options = get_trivia_question()
        options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))
        await channel.send(f"Trivia Time!\n{question}\n{options_text}")

@bot.event
async def on_ready():
    post_trivia.start()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    global current_answer
    if current_answer and message.content.lower() == current_answer:
        await message.channel.send(f"Correct {message.author.mention}!")
        current_answer = None  # Reset after correct answer
    
    await bot.process_commands(message)

@bot.command()
async def hint(ctx):
    if current_answer:
        await ctx.send(f"Hint: The answer starts with {current_answer[0].upper()}...")
    else:
        await ctx.send("No active question!")

bot.run(TOKEN)
