import telebot
from telebot import types
import random
import urllib.parse

TOKEN = '8598504605:AAE3xFxO58K0PK1gr-sm95-NKDW_WOgn05Q'
bot = telebot.TeleBot(TOKEN)

user_data = {}

def get_udata(uid):
    if uid not in user_data:
        user_data[uid] = {'ratio': '1:1', 'style': 'Cinematic', 'strength': 0.7, 'last_img': ''}
    return user_data[uid]

@bot.message_handler(commands=['start', 'settings'])
def cmd_settings(message):
    uid = message.from_user.id
    udata = get_udata(uid)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Tombol Atur Kemiripan
    btn_str = types.InlineKeyboardButton(f"🔥 Kemiripan: {int(udata['strength']*100)}%", callback_data="change_str")
    btn_ratio = types.InlineKeyboardButton(f"📐 Rasio: {udata['ratio']}", callback_data="c_ratio")
    markup.add(btn_str, btn_ratio)
    
    bot.send_message(message.chat.id, "⚙️ **Setting Bot Gacor**\n\nKirim foto buat diedit, atau `/draw` buat bikin baru.", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.from_user.id
    udata = get_udata(uid)
    
    if call.data == "change_str":
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("Mirip Banget (90%)", callback_data="s_0.9"),
              types.InlineKeyboardButton("Sedang (70%)", callback_data="s_0.7"),
              types.InlineKeyboardButton("Beda Jauh (40%)", callback_data="s_0.4"))
        bot.edit_message_text("Seberapa mirip hasil editannya nanti?", call.message.chat.id, call.message.message_id, reply_markup=m)
    
    elif call.data.startswith("s_"):
        udata['strength'] = float(call.data.replace("s_", ""))
        bot.answer_callback_query(call.id, "Kemiripan diatur!")
        cmd_settings(call.message)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    uid = message.from_user.id
    udata = get_udata(uid)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    # Ambil link foto asli
    udata['last_img'] = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    
    msg = bot.reply_to(message, "📸 **Foto Diterima!**\nSekarang ketik mau lu apain foto ini?\nContoh: *jadi anime spiderman*")
    bot.register_next_step_handler(msg, process_remix)

def process_remix(message):
    uid = message.from_user.id
    udata = get_udata(uid)
    prompt = message.text
    
    if not udata['last_img']:
        return bot.reply_to(message, "Kirim fotonya dulu kocak!")

    msg = bot.send_message(message.chat.id, "🪄 **Lagi ngerombak...**")
    
    # LOGIKA BIAR NYAMBUNG:
    # Menggunakan model Flux dengan referensi image URL di prompt
    # Menambahkan seed random agar tidak monoton
    seed = random.randint(1, 999999)
    # Parameter URL khusus Pollinations untuk image-to-image
    final_prompt = f"{prompt}, following this image structure: {udata['last_img']}, {udata['style']} style, masterpiece, high quality"
    encoded = urllib.parse.quote(final_prompt)
    
    # Link sakti biar nyambung
    url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&seed={seed}&model=flux"

    try:
        bot.send_photo(message.chat.id, url, caption="✅ **Gacor Ter-Remix!**")
        bot.delete_message(message.chat.id, msg.message_id)
    except:
        bot.send_message(message.chat.id, "❌ Waduh gagal, coba prompt lain.")

# Tetap pake Draw biasa
@bot.message_handler(commands=['draw'])
def draw_only(message):
    prompt = message.text.replace('/draw', '')
    # (Logika draw biasa lu yang lama di sini...)

bot.infinity_polling()
                               
