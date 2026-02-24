import os
import threading
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

msgs = []

@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(
        text="Открыть приложение",
        web_app=WebAppInfo(url="https://equatory.ddns.net:6767")
    )
    kb.add(btn1)
    bot.send_message(message.chat.id, "Hi :3", reply_markup=kb)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route("/")
def index():
    return "Hello, this is the Telegram bot webhook server."

def run_bot():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://equatory.ddns.net:6769/{TOKEN}")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 88)))