import telebot
import requests
import urllib.parse
import io
import random
from telebot import types

# MASUKIN TOKEN LU DI SINI
TOKEN = '8598504605:AAE3xFxO58K0PK1gr-sm95-NKDW_WOgn05Q'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "🔥 **Bot Gacor Ready!**\n\n"
        "🎨 **Fitur:**\n"
        "1. `/draw [teks]` - Generate gambar AI\n"
        "2. `/brat [teks]` - Bikin stiker Brat viral\n\n"
        "Kirim foto juga bisa buat di-remix!"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# --- FITUR GENERATE IMAGE ---
@bot.message_handler(commands=['draw'])
def handle_draw(message):
    prompt = message.text.replace('/draw', '').strip()
    if not prompt:
        return bot.reply_to(message, "Kasih teks dong, contoh: `/draw naga api`")
    
    msg = bot.reply_to(message, "⏳ Bentar, lagi digambar...")
    seed = random.randint(1, 999999)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&model=flux"
    
    try:
        bot.send_photo(message.chat.id, url, caption=f"✅ Hasil: {prompt}")
        bot.delete_message(message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ Gagal generate gambar.", message.chat.id, msg.message_id)

# --- FITUR STIKER BRAT ---
@bot.message_handler(commands=['brat'])
def handle_brat(message):
    text = message.text.replace('/brat', '').strip()
    if not text:
        return bot.reply_to(message, "Kasih teks buat stikernya, contoh: `/brat kangen`")
    
    msg = bot.reply_to(message, "⏳ Lagi bikin stiker...")
    
    # Menggunakan API eksternal buat bikin style brat
    encoded_text = urllib.parse.quote(text)
    brat_url = f"https://brat.caliphdev.com/api/brat?text={encoded_text}"
    
    try:
        response = requests.get(brat_url)
        if response.status_code == 200:
            # Kirim sebagai stiker (WebP)
            bot.send_sticker(message.chat.id, response.content)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ API Brat lagi error.", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ Gagal bikin stiker.", message.chat.id, msg.message_id)

# --- AUTO RECONNECT ---
print("Bot lagi narik... (Polling)")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
  
