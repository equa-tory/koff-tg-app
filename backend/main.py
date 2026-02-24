# /backend/main.py
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))
print("Bot is running...")



msgs=[]


@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(
        text="Открыть приложение",
        web_app=WebAppInfo(url="https://equatory.ddns.net:6767")
    )
    kb.add(btn1)
    bot.send_message(message.chat.id, "Hi :3", reply_markup=kb)

# register(bot)
bot.remove_webhook()
bot.infinity_polling()