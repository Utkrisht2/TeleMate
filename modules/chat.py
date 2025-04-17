import google.generativeai as genai
from telethon import events
from modules.database import chats_collection
import configparser
from datetime import datetime

# Load Configurations
config = configparser.ConfigParser()
config.read('config.ini')
GEMINI_API_KEY = config.get('default', 'gemini_api_key')

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)

async def handle_chat(event):
    user_input = event.text
    chat_id = event.chat_id

    # Generate AI response
    response = genai.GenerativeModel("gemini-pro").generate_content(user_input)

    # Store chat in MongoDB
    chats_collection.insert_one({
        "chat_id": chat_id,
        "user_message": user_input,
        "bot_response": response.text,
        "timestamp": datetime.utcnow()
    })

    await event.respond(response.text)