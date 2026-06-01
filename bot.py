import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
import random
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. ФЕЙКОВЫЙ СЕРВЕР ДЛЯ RENDER
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is alive')

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"Запуск фейк-сервера на порту {port}...")
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# НАСТРОЙКА БОТА
TOKEN = '8658300916:AAFxHpS6hggx-Pe3TkB_mnBysnY6'
bot = telebot.TeleBot(TOKEN)

# Хранилище данных
user_balances = {}
user_last_bonus = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("👤 Профиль", callback_data='profile'), InlineKeyboardButton("💰 Баланс", callback_data='balance'))
    markup.row(InlineKeyboardButton("🎰 Лотерея (100 BC)", callback_data='lottery'))
    markup.row(InlineKeyboardButton("🎁 Ежедневный Бонус", callback_data='get_bonus')) 
    markup.row(InlineKeyboardButton("📢 Канал", url='https://t.me/Bosyada1'), InlineKeyboardButton("👨‍💻 Тех.Поддержка", url='https://t.me/Bosyada'))

    bot.send_message(message.chat.id, "👋 Привет! Добро пожаловать в главное меню бота.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'profile')
def profile_callback(call):
    user_id = call.from_user.id
    balance = user_balances.get(user_id, 1000)
    bot.send_message(call.message.chat.id, f"👤 *Твой профиль:*\n\n🆔 Твой ID: `{user_id}`\n💰 Баланс: {balance} BC", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'balance')
def balance_callback(call):
    user_id = call.from_user.id
    balance = user_balances.get(user_id, 1000)
    bot.send_message(call.message.chat.id, f"💰 Твой текущий баланс: *{balance} BC*", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'lottery')
def lottery_callback(call):
    user_id = call.from_user.id
    balance = user_balances.get(user_id, 1000)

    if balance < 100:
        bot.answer_callback_query(call.id, "❌ Недостаточно средств для игры!", show_alert=True)
        return

    user_balances[user_id] -= 100
    if random.choice([True, False]):
        user_balances[user_id] += 200
        text = f"🎰 *Лотерея:*\n\nВыигрыш: +200 BC! 🔥\nБаланс: {user_balances[user_id]} BC"
    else:
        text = f"🎰 *Лотерея:*\n\nПроигрыш... 😰\nБаланс: {user_balances[user_id]} BC"

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'get_bonus')
def daily_bonus_callback(call):
    user_id = call.from_user.id
    current_time = datetime.now()

    if user_id in user_last_bonus:
        last_time = user_last_bonus[user_id]
        time_passed = current_time - last_time
        
        if time_passed < timedelta(days=1):
            time_left = timedelta(days=1) - time_passed
            hours = int(time_left.seconds // 3600)
            minutes = int((time_left.seconds % 3600) // 60)
            bot.answer_callback_query(call.id, f"❌ Бонус уже получен!\nПриходи через {hours}ч. {minutes}мин.", show_alert=True)
            return

    if user_id not in user_balances:
        user_balances[user_id] = 1000

    user_balances[user_id] += 2000
    user_last_bonus[user_id] = current_time
    bot.answer_callback_query(call.id, "🎁 Вам успешно начислено 2000 BC!", show_alert=True)

# ФУНКЦИЯ ДЛЯ ЗАПУСКА ПОЛЛИНГА БОТА
def run_bot():
    print("Бот успешно запущен...")
    bot.infinity_polling()

# ЗАПУСКАЕМ ВСЁ ОДНОВРЕМЕННО
if __name__ == '__main__':
    # Включаем фейковый сервер, чтобы Рендер видел открытый порт
    threading.Thread(target=run_fake_server, daemon=True).start()
    # Запускаем самого бота
    run_bot()
