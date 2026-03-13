import telebot
import requests
import socket
import time

# M - TUTUL'S PRIVATE TOKEN
API_TOKEN = '8660590217:AAERFh_sGjsahuJaa5JtyR_l-DhD7kF4R74'
bot = telebot.TeleBot(API_TOKEN)

def get_full_intel(ip):
    try:
        # IP-API থেকে সব ডাটা ফিল্ড কল করা হচ্ছে
        fields = "status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        url = f"http://ip-api.com/json/{ip}?fields={fields}"
        
        # Timeout বাড়িয়ে ১৫ সেকেন্ড করা হয়েছে যাতে কানেকশন এরর না আসে
        response = requests.get(url, timeout=15)
        r = response.json()
        
        if r.get('status') == 'success':
            return r
    except Exception as e:
        print(f"Data Fetch Error: {e}")
    return None

@bot.message_handler(commands=['start'])
def welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"👑 *WELCOME OFFICER {user_name.upper()}!*\n"
        "────────────────────────\n"
        "🛰️ *Unit:* M - TUTUL FULL INTEL v5.5\n"
        "📡 *Status:* 24/7 Cloud Active\n"
        "🛡️ *Protocol:* Deep Data Extraction\n"
        "────────────────────────\n"
        "Send an *IP Address* or *Website URL* to begin."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def track_logic(message):
    query = message.text.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # Domain to IP Resolution
        target_ip = socket.gethostbyname(query)
        data = get_full_intel(target_ip)
        
        if data:
            # Formatting the Deep Intel Report
            report = (
                f"🛰️ *DEEP INTEL REPORT: {data.get('query')}*\n"
                f"────────────────────────\n"
                f"🌍 *Country:* {data.get('country')} ({data.get('countryCode')})\n"
                f"🏙️ *Region/City:* {data.get('regionName')}, {data.get('city')}\n"
                f"📮 *Zip Code:* {data.get('zip')}\n"
                f"🏢 *ISP:* {data.get('isp')}\n"
                f"🏢 *Organization:* {data.get('org')}\n"
                f"🆔 *ASN:* {data.get('as')}\n"
                f"🕒 *Timezone:* {data.get('timezone')}\n"
                f"💰 *Currency:* {data.get('currency')}\n"
                f"────────────────────────\n"
                f"🛡️ *Proxy/VPN:* {'🔴 YES' if data.get('proxy') else '🟢 NO'}\n"
                f"📱 *Mobile Data:* {'✅ YES' if data.get('mobile') else '❌ NO'}\n"
                f"🏠 *Hosting:* {'💎 YES' if data.get('hosting') else '❌ NO'}\n"
                f"🔄 *Reverse DNS:* `{data.get('reverse')}`\n"
                f"────────────────────────\n"
                f"🎯 *Coordinates:* `{data.get('lat')}, {data.get('lon')}`\n"
                f"🔗 [Open in Google Maps](https://www.google.com/maps?q={data.get('lat')},{data.get('lon')})"
            )
            bot.reply_to(message, report, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ *Error:* API could not retrieve data for this target.")
            
    except socket.gaierror:
        bot.reply_to(message, "⚠️ *Invalid Target:* URL or IP address is incorrect.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ *System Error:* {str(e)[:50]}")

# --- Pro Connection Stabilizer ---
if __name__ == "__main__":
    print("[+] M - TUTUL SYSTEM STARTING...")
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=15)
        except Exception as e:
            print(f"Connection Lost: {e}. Reconnecting in 5s...")
            time.sleep(5)
        
