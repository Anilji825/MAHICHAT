from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.enums import ChatAction
from pymongo import MongoClient
from flask import Flask
import threading
import random
import os
import time
from datetime import datetime

API_ID = os.environ.get("API_ID", "16457832")
API_HASH = os.environ.get("API_HASH", "3030874d0befdb5d05597deacc3e83ab")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7242058454:AAH24Hp_LNk-QO422ERYmySTnrUn3rYn5A8")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://TEAMBABY01:UTTAMRATHORE09@cluster0.vmjl9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# MongoDB connection - Reuse the same client for all operations
client = MongoClient(MONGO_URL, connectTimeoutMS=30000, serverSelectionTimeoutMS=30000)
db = client["Word"]
chatai = db["WordDb"]

BOT_USERNAME = os.environ.get("BOT_USERNAME", "RADHIKA_CHAT_RROBOT")
UPDATE_CHNL = os.environ.get("UPDATE_CHNL", "BABY09_WORLD")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "UTTAM470")
SUPPORT_GRP = os.environ.get("SUPPORT_GRP", "+OL6jdTL7JAJjYzVl")
BOT_NAME = os.environ.get("BOT_NAME", "🐰⃟⃞⍣Rᴀᴅʜɪᴋᴀ❥")
START_IMG = os.environ.get("START_IMG", "https://files.catbox.moe/5dp75k.jpg")
CHANNEL_IMG = os.environ.get("CHANNEL_IMG", "https://files.catbox.moe/3ni0t3.jpg")
STKR = os.environ.get("STKR", "CAACAgEAAx0Cd5L74gAClqVmhNlbqSgKMe5TIswcgft9l6uSpgACEQMAAlEpDTnGkK-OP8PZpzUE")

# Initialize bot client
RADHIKA = Client(
    "chat-gpt",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start command handler for private chats
@RADHIKA.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    # Send message with a button
    keyboard = [
        [
            InlineKeyboardButton("Join 🤒", url="https://t.me/BABY09_WORLD")
        ]
    ]
    await message.reply(
        "Hii, I am Radhika Baby, How are you?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handler for non-private chats (both text and stickers)
@RADHIKA.on_message((filters.text | filters.sticker) & ~filters.private & ~filters.bot)
async def vickai(client: Client, message: Message):
    if not message.reply_to_message:
        # MongoDB ka ek hi connection reuse kar rahe hain
        vick = db["VickDb"]["Vick"]
        is_vick = vick.find_one({"chat_id": message.chat.id})

        if not is_vick:
            await RADHIKA.send_chat_action(message.chat.id, ChatAction.TYPING)

            # MongoDB query ko optimize kiya hai
            result = chatai.find_one({"word": message.text})

            if result:
                if result.get('check') == "sticker":
                    await message.reply_sticker(result['text'])
                else:
                    await message.reply_text(result['text'])
            else:


    # Agar message reply hai
    elif message.reply_to_message:
        getme = await RADHIKA.get_me()
        bot_id = getme.id

        if message.reply_to_message.from_user.id == bot_id:
            await RADHIKA.send_chat_action(message.chat.id, ChatAction.TYPING)

            # MongoDB query ko optimize kiya hai
            result = chatai.find_one({"word": message.text})

            if result:
                if result.get('check') == "sticker":
                    await message.reply_sticker(result['text'])
                else:
                    await message.reply_text(result['text'])
            else:


# Handler for private chats (both text and stickers)
@RADHIKA.on_message((filters.text | filters.sticker) & filters.private & ~filters.bot)
async def vickprivate(client: Client, message: Message):
    if not message.reply_to_message:
        await RADHIKA.send_chat_action(message.chat.id, ChatAction.TYPING)

        # MongoDB query ko optimize kiya hai
        result = chatai.find_one({"word": message.text})

        if result:
            if result.get('check') == "sticker":
                await message.reply_sticker(result['text'])
            else:
                await message.reply_text(result['text'])
        else:


    elif message.reply_to_message:
        getme = await RADHIKA.get_me()
        bot_id = getme.id

        if message.reply_to_message.from_user.id == bot_id:
            await RADHIKA.send_chat_action(message.chat.id, ChatAction.TYPING)

            # MongoDB query ko optimize kiya hai
            result = chatai.find_one({"word": message.text})

            if result:
                if result.get('check') == "sticker":
                    await message.reply_sticker(result['text'])
                else:
                    await message.reply_text(result['text'])
            else:


# Flask web server (Yeh functionality server ko run karne ke liye hai, isse koi direct effect nahi padega bot ki speed pe)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

def run_bot():
    print(f"{BOT_NAME} ɪs ᴀʟɪᴠᴇ!")
    RADHIKA.run()

if __name__ == "__main__":
    # Create a thread for Flask server
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Run the bot in the main thread
    run_bot()
    
