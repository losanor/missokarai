from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Exemplo de categorias e receitas (depois também vai para banco)
receitas = {
    "entrada": [
        {"nome": "Salada com Missô Karai"},
    ],
    "principal": [
        {"nome": "Frango Grelhado com Missô Karai"},
    ]
}

async def menu_receitas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("Entradas", callback_data="categoria_entrada")],
        [InlineKeyboardButton("Pratos Principais", callback_data="categoria_principal")]
    ]
    await update.callback_query.message.edit_text(
        "Escolha uma categoria:", reply_markup=InlineKeyboardMarkup(botoes)
    )

async def listar_receitas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    categoria = data.replace("categoria_", "")
    
    if categoria in receitas:
        texto = f"🍽️ Receitas - {categoria.title()}:\n\n"
        for receita in receitas[categoria]:
            texto += f"• {receita['nome']}\n\n"
        await update.callback_query.message.edit_text(texto)
    else:
        await update.callback_query.message.edit_text("Nenhuma receita cadastrada nesta categoria ainda.")
