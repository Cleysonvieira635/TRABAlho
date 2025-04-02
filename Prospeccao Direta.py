import requests
import sqlite3
from fastapi import FastAPI

# Inicializa o banco de dados
conn = sqlite3.connect("prospeccao.db")
cursor = conn.cursor()

# Criar tabelas para armazenar contatos
cursor.execute("""
CREATE TABLE IF NOT EXISTS contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    empresa TEXT,
    email TEXT UNIQUE,
    telefone TEXT,
    origem TEXT -- feira, camara, broker
)
""")
conn.commit()

# APIs simuladas para eventos e contatos
EVENTOS_API = "https://api.eventos.com/v1/commodities"
CAMARAS_COMERCIO_API = "https://api.camaras.com/v1/contatos"
BROKERS_API = "https://api.brokers.com/v1/agentes"

# Função para buscar contatos de feiras e eventos
def buscar_eventos():
    response = requests.get(EVENTOS_API)
    if response.status_code == 200:
        return response.json()
    return []

# Função para buscar contatos de câmaras de comércio
def buscar_camaras():
    response = requests.get(CAMARAS_COMERCIO_API)
    if response.status_code == 200:
        return response.json()
    return []

# Função para buscar contatos de brokers
def buscar_brokers():
    response = requests.get(BROKERS_API)
    if response.status_code == 200:
        return response.json()
    return []

# Função para salvar contatos no banco
def salvar_contato(nome, empresa, email, telefone, origem):
    try:
        cursor.execute("""
        INSERT INTO contatos (nome, empresa, email, telefone, origem)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, empresa, email, telefone, origem))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Contato {email} já está salvo.")

# Automatiza a captura de contatos
def capturar_todos_contatos():
    for evento in buscar_eventos():
        salvar_contato(evento['nome'], evento['empresa'], evento['email'], evento['telefone'], "feira")
    for camara in buscar_camaras():
        salvar_contato(camara['nome'], camara['empresa'], camara['email'], camara['telefone'], "camara")
    for broker in buscar_brokers():
        salvar_contato(broker['nome'], broker['empresa'], broker['email'], broker['telefone'], "broker")
    print("Contatos capturados com sucesso!")

# API FastAPI para consultas
app = FastAPI()

@app.get("/contatos")
def listar_contatos():
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()
    return {"contatos": contatos}

@app.post("/capturar_contatos")
def api_capturar_contatos():
    capturar_todos_contatos()
    return {"status": "Contatos capturados com sucesso"}

# Rodar API
# uvicorn nome_do_arquivo:app --reload