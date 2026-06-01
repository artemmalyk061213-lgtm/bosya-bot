# Не забудь в самый верх файла, где импорты, добавить: from datetime import datetime, timedelta
from datetime import datetime, timedelta


user_last_bonus = {}

@bot.callback_query_handler(func=lambda call: call.data == 'get_bonus')
def daily_bonus_callback(call):
    user_id = call.from_user.id
    current_time = datetime.now()

    # Проверяем время (24 часа)
    if user_id in user_last_bonus:
        last_time = user_last_bonus[user_id]
        time_passed = current_time - last_time
        
        if time_passed < timedelta(days=1):
            time_left = timedelta(days=1) - time_passed
            hours = int(time_left.seconds // 3600)
            minutes = int((time_left.seconds % 3600) // 60)
            
            # Всплывающее окно-предупреждение
            bot.answer_callback_query(call.id, f"❌ Бонус уже получен!\nПриходи через {hours}ч. {minutes}мин.", show_alert=True)
            return

    # Если пользователя нет в балансах
    if user_id not in user_balances:
        user_balances[user_id] = 1000

    # Начисляем 2000 BC
    user_balances[user_id] += 2000
    
    # Запоминаем время
    user_last_bonus[user_id] = current_time
    
    # Красивое всплывающее окошко с победой
    bot.answer_callback_query(call.id, "🎁 Вам успешно начислено 2000 BC!", show_alert=True)

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is alive')

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()
import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,WebAppInfo

TOKEN = '8658300916:AAFxHpS6hggx-Pe3TkB_mnBysnY6F5yrS9g'
bot = telebot.TeleBot(TOKEN)

user_balances = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000

    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("👤 Профиль", callback_data='profile')
    btn2 = InlineKeyboardButton("💰 Баланс", callback_data='balance')
    btn3 = InlineKeyboardButton("🎰 Лотерея (100 BC)", callback_data='lottery')
    
    # НАША НОВАЯ КНОПКА (текст русский, дата — английская):
    btn6 = InlineKeyboardButton("🎁 Бонус (2000 BC)", callback_data='get_bonus')
    
    btn4 = InlineKeyboardButton("📢 Канал", url="ТВОЯ_ССЫЛКА")
    btn5 = InlineKeyboardButton("👨‍💻 Тех.Поддержка", url="ТВОЯ_ССЫЛКА")

    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn6)
    markup.add(btn4, btn5)






@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000

    if call.data == "profile":
        text = f"👤 *Твой профиль:*\n\n🆔 Твой ID: `{user_id}`\n💰 Баланс: {user_balances[user_id]} BC"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif call.data == "balance":
        text = f"💰 Твой текущий баланс: *{user_balances[user_id]} BC*"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif call.data == "lottery":
        if user_balances[user_id] < 100:
            bot.answer_callback_query(call.id, text="❌ У тебя недостаточно Bosya Coins! Нужно хотя бы 100 BC.", show_alert=True)
            return
            
        user_balances[user_id] -= 100
        is_winner = random.choice([True, False])
        
        if is_winner:
            user_balances[user_id] += 200
            bot.answer_callback_query(call.id, text="🎉 Ты выиграл 200 BC!")
            bot.send_message(call.message.chat.id, f"🎰 *Лотерея:*\n\nСписание: -100 BC\nВыигрыш: **+200 BC**! 🔥\n\nТвой баланс: {user_balances[user_id]} BC", parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, text="😢 Пустой билет...")
            bot.send_message(call.message.chat.id, f"🎰 *Лотерея:*\n\nСписание: -100 BC\nБилет оказался пустым. 💔\n\nТвой баланс: {user_balances[user_id]} BC", parse_mode="Markdown")

print("Бот успешно запущен!")
import os
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web_server).start()

bot.polling(none_stop=True)



