# TeleMate 🤖✨ : An AI-powered Telegram Bot
Designed to make your life easier by providing a wide range of features, including reminders, to-do lists, web searches, weather updates, news headlines, file analysis, and more.<br>Built with Python and integrated with powerful APIs like Gemini AI, SerpAPI, OpenWeatherMap, and NewsAPI, TeleMate is your ultimate personal assistant on Telegram.

## Features 🌟
### ✅ **Reminders & To-Do Lists**
- Set reminders with `/remind <time> <message>`.
- Add tasks with `/addtask <task>`.
- View tasks with `/tasks`.
- Mark tasks as completed with `/completetask <task_number>`.

### 🌍 **Web Search & News**
- Perform web searches with `/search <query>`.
- Get the latest news headlines with `/news`.

### ⏳ **Weather Updates**
- Check real-time weather forecasts with `/weather <location>`.

### 🗣 **AI Chat & Translation**
- Chat with the AI using natural language.
- Translate text to English or any other language with `/translate <text> <language_code>`.

### 📄 **PDF & Image Analysis**
- Upload PDFs or images, and TeleMate will summarize or analyze their content.

## Screenshots 📸

Here are some screenshots of **TeleMate** in action:
### 1. **Welcome Message**
![Welcome Message](https://github.com/user-attachments/assets/8bf3910f-cc13-40d6-9c71-9f09b968524f)
![Start Message](https://github.com/user-attachments/assets/9ee57966-3749-4298-9b40-51e707bff863)
*The welcome message users see when they start the bot.*

### 2. **Help Message**
![Help Message](https://github.com/user-attachments/assets/cbbd0f4e-86e2-4853-bb22-aeec184da44b)
*The help message on using `/help`*

### 3. **Reminder Setup**
![Reminder Setup](https://github.com/user-attachments/assets/07a8d852-3071-48c1-8f88-40e4bbd539f2)
*Setting a reminder with `/remind` and then receiving a reminder message.*

### 4. **To-Do List Management**
![Add Task](https://github.com/user-attachments/assets/5362c6ec-20a4-4a1a-a906-cec7d7003097)
![Tasks Completed](https://github.com/user-attachments/assets/37f19785-4231-4b12-901a-06c526bbf828)
*Adding, viewing, and completing tasks with `/addtask`, `/tasks`, and `/completetask`.*

### 5. **Web Search Results**
![Web Search](https://github.com/user-attachments/assets/582ed575-b441-4683-9556-9303b1a0b625)
*Performing a web search with `/search`.*

### 6. **Weather Updates**
![Weather Updates](https://github.com/user-attachments/assets/f32b31d9-9758-43cb-9393-768644b85a66)
*Getting weather updates with `/weather <location>`.*

### 7. **News Headlines**
![News Headlines](https://github.com/user-attachments/assets/bd3d75e4-f85d-401f-9c1f-769e31eda84e)
*Fetching the latest or top 5 news with `/news`.*

### 8. **Translation**
![Translation](https://github.com/user-attachments/assets/c475922f-fca4-4c7f-ba3a-3bd216b8e9a3)
*Translating text with `translate <language1> to <language2>` and `/translate` (English by default).*

### 9. **Image Analysis**
![Image Analysis](https://github.com/user-attachments/assets/32a4cbfd-e430-44d6-a40c-447499417aa6)
![Image Analysis](https://github.com/user-attachments/assets/e3b62e23-0cfe-45b7-ad77-e0cc534419b5)
*Performing an analysis of an image, with wait message as "Analyzing your image...".*

### 10. **PDF Analysis**
![PDF Analysis](https://github.com/user-attachments/assets/80c88ba0-3add-4faa-9bf3-229ad5162cdd)
![PDF Analysis](https://github.com/user-attachments/assets/fd91e11b-a89d-4640-a7cc-075fb3aa9ac2)
*Performing an analysis of an pdf, with wait message as "Analyzing your pdf...".*

## MongoDB Collections 🌿
Here’s how data is stored in **MongoDB**:

### 1. **Users Collection**
![Initial Database](https://github.com/user-attachments/assets/881e112c-607d-4c80-83bb-2ed3ab0e262b)
*The initial database before the user starts the bot or uses `/start` command.*
![image](https://github.com/user-attachments/assets/c4a1ce51-1b95-4781-975a-c2c65c6f6e54)
*After using `/start`, It stores user details like `user_id`, `username`, `first_name`, `last_name` and `date_joined`.*

### 2. **Chats Collection**
![Chat Collection](https://github.com/user-attachments/assets/6206493e-126c-4de4-9ea5-3e66598dd3cf)
*Stores chat history, including `user_message`, `bot_response`, and `timestamp`.*

### 3. **Files Collection**
![Files Collection](https://github.com/user-attachments/assets/1e0589b4-3c52-4e8e-8529-16fb77388cb4)
*Stores metadata for uploaded files, including `filename`, `description`, and `timestamp`.*

### 4. **Reminders Collection**
![Reminders Collection](https://github.com/user-attachments/assets/09da134e-fca2-4c23-a9d1-50b12586840c)
*Stores reminders with `chat_id`, `time`, `message`, and `timestamp`.*

### 5. **To-Do Collection**
![image](https://github.com/user-attachments/assets/5cd46631-b177-43f0-baf6-e5d08cec7479)
*Stores to-do tasks with `chat_id`, `task`, and `status`.*

### 6. **Web Searches Collection**
![Web Searches Collection](https://github.com/user-attachments/assets/a2592a5f-c972-4f3b-b8d7-afdf365aeb3e)
*Stores web search queries and results, including `query`, `results`, and `timestamp`.*

## Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)
- API keys for:
  - [Gemini AI](https://ai.google.dev/)
  - [SerpAPI](https://serpapi.com/)
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [NewsAPI](https://newsapi.org/)

### Steps
1. Clone the repository:
  ```bash
  git clone https://github.com/your-username/TeleMate.git
  cd TeleMate
  ```

2. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Set up the config.ini file:
- Create a `config.ini` file in root directory.
- Fill in the required API keys and credentials.

4. Run the bot:
  ```bash
  python script.py
  ```

## Configuration ⚙️
Edit the `config.ini` file to include your API keys and credentials:

```bash
[default]

# Telegram API credentials
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
bot_token = YOUR_BOT_TOKEN

# MongoDB credentials
username = YOUR_MONGODB_USERNAME
password = YOUR_MONGODB_PASSWORD
db_name = YOUR_DATABASE_NAME

# API keys
serpapi_key = YOUR_SERPAPI_KEY
gemini_api_key = YOUR_GEMINI_API_KEY
openweathermap_api_key = YOUR_OPENWEATHERMAP_API_KEY
newsapi_key = YOUR_NEWSAPI_KEY

# Define collections
users_collection = db["users"]   # Stores user details
chats_collection = db["chats"]   # Stores chat history
files_collection = db["files"]   # Stores image/file metadata
```

## Folder Structure 📂
```
TeleMate/
├── data/                  # Stores uploaded files (images and PDFs)
│   ├── gifs/
│   │   ├── welcome.gif
│   │   ├── reminder_set.gif
│   │   ├── reminder_triggered.gif
│   │   ├── task_added.gif
│   │   ├── celebration.gif
│   │   ├── weather.gif
│   │   ├── news.gif
│   │   ├── file_analysis.gif
│   ├── images/            # Uploaded images
│   └── pdfs/              # Uploaded PDFs
├── modules/               # Contains all bot modules
│   ├── assistant.py       # Handles reminders, to-do lists, weather, and news
│   ├── chat.py            # Handles AI chat
│   ├── database.py        # Manages MongoDB connections
│   ├── file_analysis.py   # Handles file analysis (PDFs and images)
│   ├── translation.py     # Handles text translation
│   ├── user.py            # Manages user registration and contact saving
│   └── web_search.py      # Handles web searches
├── script.py              # Main bot script
├── config.ini             # Configuration file for API keys
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

## Contributing 🤝
Contributions are welcome! If you'd like to contribute to TeleMate, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

## License 📜
This project is licensed under the MIT License. See the LICENSE file for details.

## Support 💬
If you encounter any issues or have questions, feel free to open an issue on GitHub or contact me directly. Enjoy!! 
