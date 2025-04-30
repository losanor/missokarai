# handlers_lojas.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("❌ Variáveis SUPABASE_URL ou SUPABASE_KEY não definidas.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def buscar_lojas_por_regiao(regiao: str):
    try:
        response = supabase.table("lojas").select("*").eq("regiao", regiao).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar lojas do Supabase: {e}")
        return []

async def menu_lojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("Sul", callback_data="regiao_sul")],
        [InlineKeyboardButton("Norte", callback_data="regiao_norte")],
        [InlineKeyboardButton("Leste", callback_data="regiao_leste")],
        [InlineKeyboardButton("Oeste", callback_data="regiao_oeste")],
        [InlineKeyboardButton("Centro", callback_data="regiao_centro")],
        [InlineKeyboardButton("Interior", callback_data="regiao_interior")],
        [InlineKeyboardButton("🔙 Menu Principal", callback_data="voltar_menu")]
    ]
    await update.callback_query.message.edit_text(
        "📍 Escolha uma região para ver as lojas parceiras:",
        reply_markup=InlineKeyboardMarkup(botoes)
    )

async def listar_lojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    regiao = data.replace("regiao_", "")

    lojas_da_regiao = await buscar_lojas_por_regiao(regiao)
    if lojas_da_regiao:
        texto = f"*🏬 Lojas na região {regiao.title()}*\n\n"
        for loja in lojas_da_regiao:
            nome = loja["nome"]
            endereco = loja["endereco"]
            instagram = loja["instagram"].strip()

            texto += f"🏪 *{nome}*\n📍 {endereco}\n"
            if instagram:
                username = instagram.replace("@", "")
                texto += f"📸 [@{username}](https://instagram.com/{username})\n"
            texto += "\n"

        botoes = [
            [InlineKeyboardButton("🔄 Ver outras regiões", callback_data="menu_lojas")],
            [InlineKeyboardButton("🔙 Menu Principal", callback_data="voltar_menu")],
            [InlineKeyboardButton("✅ Finalizar", callback_data="finalizar")]
        ]

        try:
            await update.callback_query.message.edit_text(
                texto,
                reply_markup=InlineKeyboardMarkup(botoes),
                parse_mode="Markdown"
            )
        except BadRequest as e:
            if "Message is not modified" in str(e):
                pass
            else:
                raise
    else:
        texto = "⚠️ Em breve teremos loja aqui."

        botoes = [
            [InlineKeyboardButton("🔄 Ver outras regiões", callback_data="menu_lojas")],
            [InlineKeyboardButton("🔙 Menu Principal", callback_data="voltar_menu")],
            [InlineKeyboardButton("✅ Finalizar", callback_data="finalizar")]
        ]

        await update.callback_query.message.edit_text(
            texto,
            reply_markup=InlineKeyboardMarkup(botoes)
        )
