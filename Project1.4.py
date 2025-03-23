import discord
import asyncio
import random
import requests
from discord.ext import commands, tasks
import re
import html


TOKEN = "MTM1MzI5MTM0NTU5NDE1OTIzOA.GGdnLF.vDsFbVHErAlklSRlTQGgjwwR_PdCJjB7fhmdJ8"
TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

current_question = None
current_answer = None

def get_trivia_question():
    global current_question, current_answer
    response = requests.get(TRIVIA_API_URL).json()
    question_data = response["results"][0]

    
    current_question = html.unescape(question_data["question"])
    correct_answer = html.unescape(question_data["correct_answer"])
    options = [html.unescape(opt) for opt in question_data["incorrect_answers"]] + [correct_answer]

    random.shuffle(options)
    current_answer = correct_answer.lower()

    return current_question, options


@tasks.loop(hours=24)
async def post_trivia():
    channel = discord.utils.get(bot.get_all_channels(), name="trivia")
    if channel:
        question, options = get_trivia_question()
        options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))
        await channel.send(f"Trivia Time!\n{question}\n{options_text}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not post_trivia.is_running():
        post_trivia.start()

def normalize_answer(answer):
    return re.sub(r'[^a-zA-Z0-9]', '', answer).lower()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    global current_answer

    
    print(f"User message: {message.content}")
    print(f"Expected answer: {current_answer}")
    print(f"Normalized user answer: {normalize_answer(message.content)}")
    print(f"Normalized correct answer: {normalize_answer(current_answer) if current_answer else None}")

    
    if current_answer and normalize_answer(message.content) == normalize_answer(current_answer):
        await message.channel.send(f"✅ Correct, {message.author.mention}!")
        current_answer = None  # Reset after a correct answer
    else:
        print("Answer did not match.")  # More debugging info

    await bot.process_commands(message)


@bot.command()
async def hint(ctx):
    global current_answer
    if current_answer:
        await ctx.send(f"Hint: The answer starts with {current_answer[0].upper()}...")
    else:
        await ctx.send("No active question!")

@bot.command()
async def trivia(ctx):
    global current_question, current_answer
    question, options = get_trivia_question()
    options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))
    await ctx.send(f"Trivia Time!\n{question}\n{options_text}")


bot.run("MTM1MzI5MTM0NTU5NDE1OTIzOA.Go5N2j.D7BWrDUPy_4HHH7-KcdlBSJSmuHYHsGNnJKNME")

