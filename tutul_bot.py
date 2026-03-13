import telebot
import requests
import socket

# Your Token
API_TOKEN = '8660590217:AAERFh_sGjsahuJaa5JtyR_l-DhD7kF4R74'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🚀 *M - TUTUL CLOUD BOT v3.8*\nStatus: *24/7 Online*\nSend IP or Domain to trace.", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def track(message):
    query = message.text.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    try:
        target_ip = socket.gethostbyname(query)
        res = requests.get(f"https://ipapi.co/{target_ip}/json/", timeout=10).json()
        if 'ip' in res:
            report = (
                f"🛰️ *INTEL ACQUIRED: {res['ip']}*\n"
                f"🌍 *Country:* {res['country_name']}\n"
                f"🏢 *ISP:* {res['org']}\n"
                f"📍 *Maps:* [Click Here](https://www.google.com/maps?q={res['latitude']},{res['longitude']})"
            )
            bot.reply_to(message, report, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Invalid Target.")
    except:
        bot.reply_to(message, "⚠️ System Error.")

if __name__ == "__main__":
    bot.infinity_polling()
