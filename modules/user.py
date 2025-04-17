from modules.database import users_collection

async def start(event):
    """Handles the /start command and registers the user."""
    user_id = event.sender_id
    user_data = await event.client.get_entity(user_id)

    user = {
        "chat_id": user_id,
        "first_name": user_data.first_name,
        "username": user_data.username,
    }

    # Check if user already exists
    existing_user = users_collection.find_one({"chat_id": user_id})
    if not existing_user:
        users_collection.insert_one(user)
        await event.respond(f"👋 Hello {user_data.first_name}! You are now registered.")
    else:
        await event.respond(f"👋 Welcome back, {user_data.first_name}!")

async def save_contact(event):
    """Saves user's phone number when they share their contact."""
    if event.contact:
        user_id = event.sender_id
        phone_number = event.contact.phone_number

        # Update user entry with phone number
        users_collection.update_one(
            {"chat_id": user_id}, 
            {"$set": {"phone_number": phone_number}}, 
            upsert=True
        )

        await event.respond("📞 Your phone number has been saved successfully!")