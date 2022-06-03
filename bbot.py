import telebot
import mp
from telebot import types
import random

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'go'])
def say_hi(message):
    chat_id = message.chat.id
    amount_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    button = types.KeyboardButton('Погнали')
    amount_markup.add(button)
    msg = bot.send_message(chat_id, 'Привет! Твоя задача найти существующую пословицу)', reply_markup=amount_markup)
    bot.register_next_step_handler(msg, quiz)

@bot.message_handler(content_types=['text'])
def quiz(message):
    chat_id = message.chat.id
    q = 'Какая пословица существует?'
    false1, false2, answer = mp.three_poslov()
    mix_variants = [false1, false2, answer]
    random.shuffle(mix_variants)
    amount_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    button = types.KeyboardButton('Давай еще')
    amount_markup.add(button)
    bot.send_poll(chat_id, question=q, options=mix_variants, correct_option_id=mix_variants.index(answer), type="quiz", reply_markup=amount_markup)

bot.polling(none_stop=True)

