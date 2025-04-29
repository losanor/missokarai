import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def conectar():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        return None

def buscar_lojas_por_regiao(regiao):
    conn = conectar()
    if conn is None:
        return []
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT nome, endereco, instagram FROM lojas WHERE regiao = %s ORDER BY nome", (regiao,))
        return cur.fetchall()

def buscar_receitas_por_categoria(categoria):
    conn = conectar()
    if conn is None:
        return []
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT nome, imagem_url FROM receitas WHERE categoria = %s ORDER BY nome", (categoria,))
        return cur.fetchall()
