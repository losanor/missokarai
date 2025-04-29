import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from handlers_lojas import menu_lojas, listar_lojas
from handlers_receitas import menu_receitas, listar_receitas

#inicializar chaves
load_dotenv()

# Variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "misso-karai-token")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 10000))
if not all([TOKEN, APP_URL]):
    raise EnvironmentError("❌ Variáveis de ambiente obrigatórias ausentes: TELEGRAM_TOKEN ou APP_URL")
# --------------------- HANDLERS TELEGRAM --------------------

async def menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("📍 Localizar Lojas", callback_data="menu_lojas")],
        [InlineKeyboardButton("🍳 Receitas", callback_data="menu_receitas")]
    ]
    if update.message:
        await update.message.reply_text("Olá eu sou a MK!Escolha uma opção:", reply_markup=InlineKeyboardMarkup(botoes))

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# --------------------- INICIALIZAÇÃO DO BOT --------------------

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_principal))
    application.add_handler(CallbackQueryHandler(router))

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{APP_URL}/webhook",
        secret_token=WEBHOOK_SECRET
    )

if __name__ == "__main__":
    main()
