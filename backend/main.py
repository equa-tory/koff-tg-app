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


@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    data = json.loads(message.web_app_data.data)
    # bot.send_message(message.chat.id, f"Booking received:\n{data}")
    bot.send_message(message.chat.id, f"Hotel booked: {data['hotel']}\nPrice: ${data['price']}")




# register(bot)
bot.remove_webhook()
bot.infinity_polling()



# /backend/main.py
