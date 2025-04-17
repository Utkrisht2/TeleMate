import os
from telethon import TelegramClient, events
import configparser
import asyncio
from telethon import events

# Ensure the sessions folder exists
os.makedirs("sessions", exist_ok=True)

# Import modules
from modules.user import start, save_contact
from modules.database import users_collection  # Import the users collection
from modules.chat import handle_chat
from modules.file_analysis import analyze_file
from modules.web_search import fetch_results
from modules.assistant import (
    set_reminder, add_todo, list_todos, complete_todo, get_weather, get_news, check_reminders
)
from modules.translation import handle_translation  # Import the translation handler

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('default', 'api_id')
API_HASH = config.get('default', 'api_hash')
BOT_TOKEN = config.get('default', 'bot_token')

# Start Telegram Client
client = TelegramClient("sessions/Bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Welcome message with commands
WELCOME_MESSAGE = """
🌟 **Welcome to the AI-Powered Personal Assistant Bot!** 🌟

Here’s what I can do for you:

🖼️ **Image Analysis**:
   - Upload an image, and I'll describe its content.

📄 **PDF Analysis**:
   - Upload a PDF, and I'll extract and summarize its text.

🔍 **Web Search**:
   - Use `/search <query>` to search the web and get a summary.

⏰ **Reminders**:
   - Set reminders with `/remind <time> <message>`.
   - Example: `/remind 18:00 Buy groceries`.

📜 **To-Do List**:
   - Add tasks with `/addtask <task>`.
   - View tasks with `/tasks`.
   - Complete tasks with `/completetask <task_number>`.

🌤️ **Weather Updates**:
   - Get weather updates with `/weather <location>`.
   - Example: `/weather New York`.

📰 **News Headlines**:
   - Fetch the latest news with `/news`.

💬 **Chat with AI**:
   - Send me a message, and I'll respond using Gemini AI.

🌐 **Translation**:
   - Use `/translate <text>` to translate text to English.
   - Use `/translate <text> <language_code>` to translate text to a specific language.

For a list of commands, type `/help`.

Feel free to explore! 😊
"""

# Compact commands list for /help
COMMANDS_MESSAGE = """
📜 **Commands**:
   - `/start`: Show this welcome message.
   - `/search <query>`: Perform a web search.
   - `/remind <time> <message>`: Set a reminder.
   - `/addtask <task>`: Add a task.
   - `/tasks`: View your to-do list.
   - `/completetask <task_number>`: Complete a task.
   - `/weather <location>`: Get weather updates.
   - `/news`: Fetch the latest news.
   - `/translate <text>`: Translate text to English.
   - `/translate <text> <language_code>`: Translate text to a specific language.
   - `/help`: Show this message again.
"""

# 🟢 Handle /start command
@client.on(events.NewMessage(pattern="/start"))
async def handle_start(event):
    user_id = event.sender_id
    user = users_collection.find_one({"user_id": user_id})

    if not user:
        # Create a new user document
        user_data = {
            "user_id": user_id,
            "username": event.sender.username,
            "first_name": event.sender.first_name,
            "last_name": event.sender.last_name,
            "date_joined": event.date
        }
        users_collection.insert_one(user_data)

    # Send welcome GIF with caption
    await event.respond(file="data/gifs/welcome.gif", message=WELCOME_MESSAGE, parse_mode='markdown')

# 🟢 Handle /help command
@client.on(events.NewMessage(pattern="/help"))
async def handle_help(event):
    await event.respond(COMMANDS_MESSAGE, parse_mode='markdown')

# 🟢 Handle contact sharing
@client.on(events.NewMessage(func=lambda e: e.contact))
async def handle_contact(event):
    await save_contact(event)

# 🟢 Handle web searches
@client.on(events.NewMessage(pattern=r"/search (.+)"))
async def handle_websearch(event):
    query = event.pattern_match.group(1)
    await fetch_results(event, query)

# 🟢 Handle file uploads
@client.on(events.NewMessage(func=lambda e: e.document or e.photo))
async def handle_file_upload(event):
    await analyze_file(event)

# 🟢 Handle AI chat for regular messages
@client.on(events.NewMessage)
async def handle_user_chat(event):
    if event.text.startswith("/") or event.document or event.photo:
        return  # Ignore commands and files
    await handle_chat(event)

# 🟢 Handle reminders
@client.on(events.NewMessage(pattern=r"/remind (\d{2}:\d{2}) (.+)"))
async def handle_reminder(event):
    time_str = event.pattern_match.group(1)
    message = event.pattern_match.group(2)

    # Send a GIF with caption for setting a reminder
    await event.respond(file="data/gifs/reminder_set.gif", message=f"⏰ Reminder set for {time_str}: {message}")

# 🟢 Handle to-do tasks
@client.on(events.NewMessage(pattern=r"/addtask (.+)"))
async def handle_todo_add(event):
    task = event.pattern_match.group(1)
    await add_todo(event, task)

    # Send a GIF with caption for adding a task
    await event.respond(file="data/gifs/task_added.gif", message=f"✅ Task added: {task}")

@client.on(events.NewMessage(pattern="/tasks"))
async def handle_todo_list(event):
    tasks = await list_todos(event)
    await event.respond(tasks)

@client.on(events.NewMessage(pattern=r"/completetask (\d+)"))
async def handle_todo_complete(event):
    task_number = int(event.pattern_match.group(1))
    await complete_todo(event, task_number)

    # Send a celebratory GIF with caption for completing a task
    await event.respond(file="data/gifs/celebration.gif", message="🎉 Task completed! Great job!")

# 🟢 Handle weather updates
@client.on(events.NewMessage(pattern=r"/weather (.+)"))
async def handle_weather(event):
    location = event.pattern_match.group(1)
    weather_response = await get_weather(event, location)

    # Send a weather-related GIF with caption
    await event.respond(file="data/gifs/weather.gif", message=weather_response)

# 🟢 Handle news headlines
@client.on(events.NewMessage(pattern="/news"))
async def handle_news(event):
    # Await the get_news coroutine to get the news response
    news_response = await get_news(event)

    # Send a news-related GIF with caption
    await event.respond(file="data/gifs/news.gif", message=news_response)

# 🟢 Handle translation to English (default)
@client.on(events.NewMessage(pattern=r"/translate (.+)"))
async def handle_translation_command(event):
    text = event.pattern_match.group(1).strip()
    if " " in text:
        return  # Ignore commands that contain a space (they will be handled by handle_translation_to_language)
    await handle_translation(event, text, "en")

# 🟢 Handle translation to a specific language
@client.on(events.NewMessage(pattern=r"/translate (.+) (.+)"))
async def handle_translation_to_language(event):
    text_to_translate = event.pattern_match.group(1).strip()
    target_language = event.pattern_match.group(2).strip()
    await handle_translation(event, text_to_translate, target_language)

# Start the reminder checker task
async def start_reminder_checker():
    await client.start(bot_token=BOT_TOKEN)
    client.loop.create_task(check_reminders(client))

# Run the bot
print("✅ Bot is running...", flush=True)
client.loop.run_until_complete(start_reminder_checker())
client.run_until_disconnected()