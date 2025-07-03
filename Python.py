import telebot
import openai
import random
import pickle
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OWNER_ID = 7833356315

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_KEY

bad_words = ['madarchod', 'chutiya', 'fuck', 'bc', 'mc', 'bsdk', 'bhosdi', 'lund']
flirty_lines = [
    "Tum toh dil le gaye 😘",
    "Aaj tum bahut cute lag rahe ho 😍",
    "Tere bina dil udaas hai 🥺",
    "Tumhara naam hi smile de deta hai 💖",
    "Tera message padke blush kar rahi hoon 😳"
]

MEMORY_FILE = "chat_memory.pkl"
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "rb") as f:
        memory = pickle.load(f)
else:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "wb") as f:
        pickle.dump(memory, f)

def get_ai_reply(user_id, message):
    user_history = memory.get(user_id, [])
    user_history.append({"role": "user", "content": message})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user_history,
            max_tokens=100
        )
        reply = response.choices[0].message['content']
        user_history.append({"role": "assistant", "content": reply})
        memory[user_id] = user_history[-10:]
        save_memory()
        return reply
    except Exception as e:
        print("OpenAI Error:", e)
        return "Mujhe kuch samajh nahi aaya 😔"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, f"Heyy {message.from_user.first_name} ❤️\nMain ArishuJaan hoon 💋\nFlirt, baat aur fun ke liye ready ho jao!")

@bot.message_handler(func=lambda msg: True)
def handle_all(msg):
    user_id = msg.from_user.id
    text = msg.text.lower()

    print("📩", msg.text)

    if any(bad in text for bad in bad_words):
        bot.reply_to(msg, "⚠️ Gaali mat do na cutie 😥")
        bot.send_message(OWNER_ID, f"🚨 @{msg.from_user.username or msg.from_user.first_name} ne yeh bola:\n`{msg.text}`", parse_mode="Markdown")
        return

    if any(word in text for
