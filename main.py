import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, CommandHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from handlers_lojas import menu_lojas, listar_lojas
from handlers_receitas import menu_receitas, listar_receitas
from flask import Flask, request

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "misso-karai-token")
APP_URL = os.getenv("APP_URL")  # ex: https://seuapp.onrender.com

app_flask = Flask(__name__)  # para receber requisições HTTP
application = None  # será atribuído após inicialização

# Telegram setup
async def menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("📍 Localizar Lojas", callback_data="menu_lojas")],
        [InlineKeyboardButton("🍳 Receitas", callback_data="menu_receitas")]
    ]
    await update.message.reply_text("Escolha uma opção:", reply_markup=InlineKeyboardMarkup(botoes))

async def router(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "menu_lojas":
        await menu_lojas(update, context)
    elif data.startswith("regiao_"):
        await listar_lojas(update, context)
    elif data == "menu_receitas":
        await menu_receitas(update, context)
    elif data.startswith("categoria_"):
        await listar_receitas(update, context)

@app_flask.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        return "Unauthorized", 403
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK"

async def setup():
    global application
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT, menu_principal))
    application.add_handler(CallbackQueryHandler(router))

    await application.bot.set_webhook(
        url=f"{APP_URL}/webhook",
        secret_token=WEBHOOK_SECRET,
    )

    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # necessário para processar a fila de updates

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup())
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
