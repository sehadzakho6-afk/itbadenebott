import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# لیستا پرسیار و بەرسڤێن بوتێ تە
QUESTIONS_ANSWERS = {
    "پرسیارا ١: ئایتی (IT) چییە؟": "ئایتی کورتکرنا Information Technology یە، واتە تەکنەلۆژیا زانیاریان کو گرنگیێ ددەتە پۆلێنکرنا کۆمپیوتەری، تۆڕان و پاراستنا داتایان.",
    "پرسیارا ٢: جیاوازی د ناڤبەرا سۆفتوێر و هاردوێر دا چییە؟": "هاردوێر ئەو بەشێن فیزیکی نە کو دەست لێ ددەت وەک ماوس و شاشێ. سۆفتوێر ئەو بەرنامە و کۆدەنە کو کۆمپیوتەری بگەڕ دکەن.",
    "پرسیارا ٣: ئەزموون دێ ب چ ڕەنگ بن؟": "ئەزموون دێ ب شێوازێ تیۆری و پراکتیکی بن، لەوما یا فەرە پێشوەختە ڕاهێنانێ ل سەر پڕۆژە و کۆدان بکەن.",
}

buttons = [[key] for key in QUESTIONS_ANSWERS.keys()]
keyboard_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "سڵاو و ڕێز پۆل پۆل بۆ هەوە! 🌹 ب خێر هاتی بۆ بوتێ پرسیار و بەرسڤان بۆ هاوکاریا قوتابییان.\n\n"
        "هیڤییە ل خوارێ کلیکێ ل سەر هەر پرسیارەکێ بکەی ئەوا تە دڤێت بەرسڤا وێ بزانی:"
    )
    await update.message.reply_text(welcome_text, reply_markup=keyboard_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if user_message in QUESTIONS_ANSWERS:
        reply_text = QUESTIONS_ANSWERS[user_message]
    else:
        reply_text = "ببوورە، بەرسڤا ڤێ پرسیارێ ل دەف من نینە. تکایە ئێک ژ پرسیارێن سەر شاشێ دەستنیشان بکە."
    await update.message.reply_text(reply_text, reply_markup=keyboard_markup)

def main():
    # ل ڤێرە دێ تۆکنا بوتێ خۆ دابنێی
    TOKEN = os.environ.get("TELEGRAM_TOKEN", "تۆکنا_خۆ_ل_ڤێرە_دابنێ")
    
    threading.Thread(target=run_web, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
