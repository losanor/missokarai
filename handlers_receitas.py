from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db import buscar_receitas_por_categoria

async def menu_receitas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categorias = ["Snacks", "Prato Principal", "Vegano", "Sobremesa", "Molhos"]
    botoes = [[InlineKeyboardButton(c, callback_data=f"categoria_{c}")] for c in categorias]
    await update.message.reply_text("Escolha a categoria:", reply_markup=InlineKeyboardMarkup(botoes))

async def listar_receitas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    categoria = query.data.split("_")[1]
    receitas = buscar_receitas_por_categoria(categoria)

    if not receitas:
        await query.edit_message_text("Nenhuma receita encontrada nessa categoria.")
        return

    botoes = [[InlineKeyboardButton(nome, url=imagem_url)] for nome, imagem_url in receitas]
    await query.edit_message_text(f"🍳 Receitas de {categoria}:", reply_markup=InlineKeyboardMarkup(botoes))
