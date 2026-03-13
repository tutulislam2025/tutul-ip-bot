import telebot
import requests
import socket

API_TOKEN = '8660590217:AAERFh_sGjsahuJaa5JtyR_l-DhD7kF4R74'
bot = telebot.TeleBot(API_TOKEN)

def get_max_data(ip):
    try:
        # IP-API এর প্রো ভার্সনের মতো সব ডাটা ফিল্ড রিকোয়েস্ট করছি
        fields = "status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=10).json()
        
        if r['status'] == 'success':
            return r
    except:
        pass
    return None

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🔥 *M - TUTUL FULL INTEL v4.5*\n──────────────────\nStatus: *ONLINE (Cloud Mode)*\nSend IP or Domain for *Maximum Intelligence Report*.", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def track(message):
    query = message.text.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        target_ip = socket.gethostbyname(query)
        data = get_max_data(target_ip)
        
        if data:
            # Proxy/VPN Detection Logic
            is_proxy = "🔴 YES" if data.get('proxy') else "🟢 NO"
            is_mobile = "📱 YES" if data.get('mobile') else "💻 NO"
            
            report = (
                f"🛰️ *MAX INTEL REPORT: {data.get('query')}*\n"
                f"────────────────────────\n"
                f"🌍 *Country:* {data.get('country')} ({data.get('countryCode')})\n"
                f"🏙️ *Region/City:* {data.get('regionName')}, {data.get('city')}\n"
                f"📮 *Zip Code:* {data.get('zip')}\n"
                f"🏢 *ISP:* {data.get('isp')}\n"
                f"🏢 *Organization:* {data.get('org')}\n"
                f"🆔 *ASN:* {data.get('as')}\n"
                f"📡 *AS Name:* {data.get('asname')}\n"
                f"🕒 *Timezone:* {data.get('timezone')}\n"
                f"💰 *Currency:* {data.get('currency')}\n"
                f"────────────────────────\n"
                f"🛡️ *Proxy/VPN:* {is_proxy}\n"
                f"📱 *Mobile Data:* {is_mobile}\n"
                f"🏠 *Hosting:* {'YES' if data.get('hosting') else 'NO'}\n"
                f"🔄 *Reverse DNS:* `{data.get('reverse')}`\n"
                f"────────────────────────\n"
                f"🎯 *Coordinates:* `{data.get('lat')}, {data.get('lon')}`\n"
                f"🔗 [Open in Google Maps](http://maps.google.com/maps?q={data.get('lat')},{data.get('lon')})"
            )
            bot.reply_to(message, report, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ *System Alert:* Target Data Blocked or Invalid.")
    except:
        bot.reply_to(message, "⚠️ *Invalid Target:* Domain resolution failed.")

bot.infinity_polling()
            
