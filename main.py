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

# --------------------- HANDLERS TELEGRAM --------------------

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

# --------------------- FLASK WEBHOOK --------------------
@app_flask.route("/webhook", methods=["POST"])
def webhook():
    try:
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
            print("🔒 Token inválido no header!")
            return "Unauthorized", 403

        data = request.get_json(force=True)
        print(f"🔔 Webhook RECEBIDO: {data}")  # <- importante log aqui!

        if application is None:
            print("⚠️ Application ainda não foi inicializada!")
            return "Application not ready", 503

        update = Update.de_json(data, application.bot)
        application.update_queue.put_nowait(update)
        return "OK", 200

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return "Internal Server Error", 500

# --------------------- INICIALIZAÇÃO ASSÍNCRONA --------------------

async def main():
    global application
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT, menu_principal))
    application.add_handler(CallbackQueryHandler(router))

    await application.bot.set_webhook(
        url=f"{APP_URL}/webhook",
        secret_token=WEBHOOK_SECRET,
    )
    print("📡 Webhook registrado com sucesso!")
    await application.initialize()
    await application.start()
    print("✅ Bot Telegram com webhook pronto!")

# --------------------- START FLASK + BOT --------------------

if __name__ == "__main__":
    # Inicia o bot em background
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    # Inicia o servidor Flask (Render detecta essa porta)
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
