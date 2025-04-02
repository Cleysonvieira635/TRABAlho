import sqlite3
import requests
from fastapi import FastAPI

# Configuração do banco de dados
conn = sqlite3.connect("compradores.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS compradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        pais TEXT,
        industria TEXT,
        fonte TEXT
    )
''')
conn.commit()

# Configuração da API
app = FastAPI()

# Chaves de API (substitua pelas credenciais reais)
API_KEYS = {
    "trademap": "SUA_CHAVE_TRADEMAP",
    "exportgenius": "SUA_CHAVE_EXPORTGENIUS",
    "kompass": "SUA_CHAVE_KOMPASS",
    "panjiva": "SUA_CHAVE_PANJIVA",
    "importgenius": "SUA_CHAVE_IMPORTGENIUS"
}

# Função genérica para buscar dados de APIs externas
def buscar_dados_api(nome_api, url, params=None):
    headers = {"Authorization": f"Bearer {API_KEYS[nome_api]}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar {nome_api}: {response.status_code}")
        return None

# Função para armazenar compradores no banco de dados
def salvar_comprador(nome, pais, industria, fonte):
    cursor.execute("INSERT INTO compradores (nome, pais, industria, fonte) VALUES (?, ?, ?, ?)", (nome, pais, industria, fonte))
    conn.commit()

# Função para buscar compradores nas APIs e salvar no banco
def capturar_compradores():
    fontes = {
        "trademap": "https://api.trademap.com/compradores",
        "exportgenius": "https://api.exportgenius.com/importers",
        "kompass": "https://api.kompass.com/buyers",
        "panjiva": "https://api.panjiva.com/clients",
        "importgenius": "https://api.importgenius.com/data"
    }
    
    for fonte, url in fontes.items():
        dados = buscar_dados_api(fonte, url)
        if dados:
            for comprador in dados.get("compradores", []):
                salvar_comprador(comprador["nome"], comprador["pais"], comprador["industria"], fonte)

# Endpoint para buscar compradores do banco de dados
@app.get("/compradores")
def listar_compradores():
    cursor.execute("SELECT * FROM compradores")
    compradores = cursor.fetchall()
    return {"compradores": compradores}

# Rota para capturar e armazenar compradores automaticamente
@app.post("/capturar_compradores")
def capturar_compradores_api():
    capturar_compradores()
    return {"status": "Dados capturados e armazenados com sucesso."}
