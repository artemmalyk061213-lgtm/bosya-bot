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
        
    markup = InlineKeyboardMarkup( ) 
    btn1 = InlineKeyboardButton("👤 Профиль", callback_data="profile")
    btn2 = InlineKeyboardButton("💰 Баланс", callback_data="balance")
    btn3 = InlineKeyboardButton("🎰 Лотерея (100 BC)", callback_data="lottery")
    btn4 = InlineKeyboardButton("📢 Канал", url="https://t.me/Bosyada1")
    btn5 = InlineKeyboardButton("👨‍💻 Тех.Поддержка", url="https://t.me/Bosyada")
    
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4, btn5)
    with open('1780200644977.png', 'rb') as photo:
    bot.send_photo(message.chat.id, photo, caption="👋 Добро пожаловать в бота!", reply_markup=markup)




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



