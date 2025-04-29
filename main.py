import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from handlers_lojas import menu_lojas, listar_lojas
from handlers_receitas import menu_receitas, listar_receitas

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def menu_principal(update, context):
    botoes = [
        [InlineKeyboardButton("\ud83d\udccd Localizar Lojas", callback_data="menu_lojas")],
        [InlineKeyboardButton("\ud83c\udf73 Receitas", callback_data="menu_receitas")]
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

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, menu_principal))
    app.add_handler(CallbackQueryHandler(router))

    app.run_polling()
