import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flask import Flask, request
from handlers_lojas import menu_lojas, listar_lojas
from handlers_receitas import menu_receitas, listar_receitas

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "misso-karai-token")
APP_URL = os.getenv("APP_URL")

app_flask = Flask(__name__)
application = None

async def menu_principal(update: Update, context):
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

async def start_bot():
    global application
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT, menu_principal))
    application.add_handler(CallbackQueryHandler(router))

    # Seta o webhook para o Telegram
    await application.bot.set_webhook(
        url=f"{APP_URL}/webhook",
        secret_token=WEBHOOK_SECRET,
    )

    await application.initialize()
    await application.start()
    print("✅ Bot Telegram pronto para receber Webhook!")

# Rodar o Flask normalmente
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())  # INICIA o bot sem travar
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
