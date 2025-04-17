from googletrans import Translator
from modules.database import chats_collection
from datetime import datetime

# Disable googletrans logging
import logging
logging.getLogger("googletrans").setLevel(logging.WARNING)

# Initialize Translator
translator = Translator()

# Helper function to map language names to codes
def get_language_code(language_name):
    """
    Maps a language name (e.g., "Spanish") to its corresponding language code (e.g., "es").
    Defaults to English ("en") if the language is not found.
    """
    language_map = {
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "chinese": "zh-cn",
        "japanese": "ja",
        "korean": "ko",
        "hindi": "hi",
        "arabic": "ar",
        "russian": "ru",
        "portuguese": "pt",
        "italian": "it",
        # Add more languages as needed
    }
    return language_map.get(language_name.lower(), "en")  # Default to English if not found

def translate_text(text, target_language="en"):
    """
    Translates the given text to the target language using googletrans.
    Returns the translated text or None if translation fails.
    """
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return None

async def handle_translation(event, text, target_language="en"):
    """
    Handles the translation process:
    1. Translates the given text to the target language.
    2. Stores the translation in MongoDB.
    3. Sends the translated text back to the user.
    """
    # Convert language name to code (e.g., "Spanish" -> "es")
    target_language = get_language_code(target_language)
    chat_id = event.chat_id

    # Translate the user's message
    translated_text = translate_text(text, target_language)

    if translated_text:
        # Store translated chat in MongoDB
        chats_collection.insert_one({
            "chat_id": chat_id,
            "user_message": text,
            "translated_message": translated_text,
            "timestamp": datetime.now()
        })

        await event.respond(f"🈹 Translated: {translated_text}")
    else:
        await event.respond("❌ Translation failed. Please try again.")