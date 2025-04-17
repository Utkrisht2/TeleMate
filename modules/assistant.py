import requests
import configparser
from datetime import datetime, timezone, timedelta
from modules.database import reminders_collection, todos_collection
import asyncio

# Load configurations
config = configparser.ConfigParser()
config.read('config.ini')
OPENWEATHERMAP_API_KEY = config.get('default', 'openweathermap_api_key')
NEWSAPI_KEY = config.get('default', 'newsapi_key')

# Helper function to validate time format
def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Set a reminder
async def set_reminder(event, time_str, message):
    if not validate_time(time_str):
        await event.respond("❌ Invalid time format. Please use HH:MM.")
        return

    # Get the current time in the user's local time
    now = datetime.now(timezone.utc).astimezone()
    reminder_time = now.replace(hour=int(time_str[:2]), minute=int(time_str[3:]), second=0, microsecond=0)

    # If the reminder time is in the past, schedule it for the next day
    if reminder_time < now:
        reminder_time += timedelta(days=1)

    # Store the reminder in UTC
    reminders_collection.insert_one({
        "chat_id": event.chat_id,
        "time": reminder_time.astimezone(timezone.utc).isoformat(),  # Store in UTC
        "message": message,
        "timestamp": datetime.now(timezone.utc)
    })
    await event.respond(f"⏰ Reminder set for {time_str}: {message}")

# Background task to check reminders
async def check_reminders(client):
    while True:
        now = datetime.now(timezone.utc)
        reminders = reminders_collection.find({"time": {"$lte": now.isoformat()}})

        for reminder in reminders:
            # Send a GIF with the reminder message
            await client.send_message(reminder["chat_id"], file="data/gifs/reminder_triggered.gif", message=f"⏰ Reminder: {reminder['message']}")
            reminders_collection.delete_one({"_id": reminder["_id"]})

        await asyncio.sleep(60)  # Check every minute

# Add a to-do task
async def add_todo(event, task):
    todos_collection.insert_one({
        "chat_id": event.chat_id,
        "task": task,
        "status": "pending"
    })
    await event.respond(file="data/gifs/task_added.gif", message=f"✅ Task added: {task}")

# List to-do tasks
async def list_todos(event):
    tasks = list(todos_collection.find({"chat_id": event.chat_id, "status": "pending"}))
    if not tasks:
        await event.respond("📜 No pending tasks.")
        return

    task_list = "\n".join([f"{idx + 1}. {task['task']}" for idx, task in enumerate(tasks)])
    await event.respond(f"📜 Your to-do list:\n{task_list}")

# Complete a to-do task
async def complete_todo(event, task_number):
    tasks = list(todos_collection.find({"chat_id": event.chat_id, "status": "pending"}))
    if not tasks:
        await event.respond("❌ No pending tasks.")
        return

    if task_number < 1 or task_number > len(tasks):
        await event.respond("❌ Invalid task number.")
        return

    task = tasks[task_number - 1]
    todos_collection.update_one({"_id": task["_id"]}, {"$set": {"status": "completed"}})
    await event.respond(file="data/gifs/celebration.gif", message="🎉 Task completed! Great job!")

# Get weather updates
async def get_weather(event, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ Could not fetch weather data. Please try again."

    data = response.json()
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"🌤️ Weather in {location}: {weather}, {temp}°C"

# Get news headlines
async def get_news(event):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ Could not fetch news. Please try again."

    articles = response.json().get("articles", [])[:5]  # Get top 5 headlines
    if not articles:
        return "❌ No news found."

    news_list = "\n".join([f"📰 {article['title']}" for article in articles])
    return f"📰 Top News Headlines:\n{news_list}"