# /backend/main.py
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv



import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware




#region --- BOT ---
load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))
print("Bot is running...")


@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(
        text="Открыть приложение",
        web_app=WebAppInfo(url="https://equatory.ddns.net:6767")
    )
    kb.add(btn1)
    bot.send_message(message.chat.id, "Hi :3", reply_markup=kb)

@bot.message_handler(commands=['key'])
def auth(msg):
    if msg.text == os.getenv("KEY"):
        bot.send_message(msg.chat.id, "Authorized")
#endregion


#region --- API ---
HOTELS_FILE = "hotels.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ensure_hotels_file():
    if not os.path.exists(HOTELS_FILE):
        default_hotels = [
            {
                "id": 1,
                "name": "Tokyo Stay",
                "city": "Tokyo",
                "price": 120,
                "rating": 4.5
            },
            {
                "id": 2,
                "name": "Osaka Inn",
                "city": "Osaka",
                "price": 90,
                "rating": 4.2
            },
            {
                "id": 3,
                "name": "Berlin Central",
                "city": "Berlin",
                "price": 110,
                "rating": 4.4
            }
        ]
        with open(HOTELS_FILE, "w") as f:
            json.dump(default_hotels, f, indent=4)


def load_hotels():
    ensure_hotels_file()
    with open(HOTELS_FILE, "r") as f:
        return json.load(f)


@app.get("/search")
def search_hotels(city: str = Query(...)):
    hotels = load_hotels()
    filtered = [
        h for h in hotels
        if h["city"].lower() == city.lower()
    ]
    return filtered
#endregion




# register(bot)
bot.remove_webhook()
bot.infinity_polling()