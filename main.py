import telebot
from gtts import gTTS
import os
from flask import Flask
import threading

BOT_TOKEN = "новый_токен_от_BotFather"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Сказать доброе слово", "Спросить, как дела")
    bot.send_message(message.chat.id, "Привет! Я твой MetaPelet 😊", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def reply_with_voice(message):
    if message.text == "Сказать доброе слово":
        text = "Ты замечательная. Я всегда рядом."
    elif message.text == "Спросить, как дела":
        text = "Соня, как ты себя чувствуешь сегодня?"
    else:
        text = "Я тебя слушаю."

    tts = gTTS(text, lang='ru')
    tts.save("voice.ogg")

    with open("voice.ogg", "rb") as voice:
        bot.send_voice(message.chat.id, voice)

    os.remove("voice.ogg")

app = Flask(__name__)

@app.route('/')
def home():
    return 'MetaPelet работает!'

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask).start()

bot.infinity_polling()
