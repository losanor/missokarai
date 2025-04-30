from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Exemplo de dados de lojas (depois podemos migrar para banco Supabase)
lojas = {
    "zona_sul": [
        {"nome": "Loja A", "endereco": "Rua A, 123", "instagram": "@lojazs"},
        {"nome": "Loja B", "endereco": "Rua B, 456", "instagram": "@lojabzs"},
    ],
    "zona_norte": [
        {"nome": "Loja C", "endereco": "Rua C, 789", "instagram": "@lojan"},
    ]
}

async def menu_lojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("Sul", callback_data="regiao_zona_sul")],
        [InlineKeyboardButton("Norte", callback_data="regiao_zona_norte")],
        [InlineKeyboardButton("Leste", callback_data="regiao_zona_leste")],
        [InlineKeyboardButton("Oeste", callback_data="regiao_zona_oeste")],
        [InlineKeyboardButton("Central", callback_data="regiao_central")],
        [InlineKeyboardButton("Interior", callback_data="Interior")],
        [InlineKeyboardButton("🔙 Voltar ao Menu Principal", callback_data="voltar_menu")]
    ]
    await update.callback_query.message.edit_text(
        "Escolha uma região:", reply_markup=InlineKeyboardMarkup(botoes)
    )

async def listar_lojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    regiao = data.replace("regiao_", "")
    
    if regiao in lojas:
        texto = f"🏬 Lojas na {regiao.replace('_', ' ').title()}:\n\n"
        for loja in lojas[regiao]:
            texto += f"• {loja['nome']}\n  📍 {loja['endereco']}\n  📸 Instagram: {loja['instagram']}\n\n"
        botoes = [
            [InlineKeyboardButton("🔄 Voltar para regiões", callback_data="menu_lojas")],
            [InlineKeyboardButton("🔙 Menu Principal", callback_data="voltar_menu")],
            [InlineKeyboardButton("✅ Finalizar", callback_data="finalizar")]
        ]
        await update.callback_query.message.edit_text(
            texto,
            reply_markup=InlineKeyboardMarkup(botoes)
        )
    else:
        await update.callback_query.message.edit_text("Nenhuma loja cadastrada nesta região ainda.")
