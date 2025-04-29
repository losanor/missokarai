from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db import buscar_lojas_por_regiao
from utils import escape_markdown_v2

async def menu_lojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    regioes = ["Sul", "Norte", "Leste", "Oeste", "Central", "Interior"]
    botoes = [[InlineKeyboardButton(r, callback_data=f"regiao_{r}")] for r in regioes]
    await update.message.reply_text("Escolha a região:", reply_markup=InlineKeyboardMarkup(botoes))

async def listar_lojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    regiao = query.data.split("_")[1]
    lojas = buscar_lojas_por_regiao(regiao)

    if not lojas:
        await query.edit_message_text("Nenhuma loja encontrada nessa região.")
        return

    resposta = f"\ud83d\udccd *Lojas na região {escape_markdown_v2(regiao)}:*\n\n"
    for nome, endereco, instagram in lojas:
        resposta += f"• *{escape_markdown_v2(nome)}*\n{escape_markdown_v2(endereco)}\n[Instagram]({escape_markdown_v2(instagram)})\n\n"

    await query.edit_message_text(resposta, parse_mode="MarkdownV2", disable_web_page_preview=True)
