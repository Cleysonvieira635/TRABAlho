import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('compradores_premium.db')
cursor = conn.cursor()

# Criar tabela de compradores validados
cursor.execute("""
CREATE TABLE IF NOT EXISTS compradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    empresa TEXT,
    setor TEXT,
    volume_anual REAL,
    regiao TEXT,
    validado BOOLEAN DEFAULT 1,
    data_validacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
import requests
from bs4 import BeautifulSoup

# Função para capturar novos compradores de um portal financeiro
def capturar_compradores():
    url = "https://www.exemplo.com/compradores"  # Altere para uma fonte real
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    compradores = []
    for linha in soup.find_all("tr", class_="comprador"):
        nome = linha.find("td", class_="nome").text
        empresa = linha.find("td", class_="empresa").text
        setor = linha.find("td", class_="setor").text
        volume = float(linha.find("td", class_="volume").text.replace(",", ""))
        regiao = linha.find("td", class_="regiao").text

        compradores.append((nome, empresa, setor, volume, regiao))

    return compradores

# Inserir novos compradores no banco de dados
def inserir_compradores(compradores):
    for comprador in compradores:
        cursor.execute("INSERT INTO compradores (nome, empresa, setor, volume_anual, regiao) VALUES (?, ?, ?, ?, ?)",
                       comprador)
    conn.commit()

novos_compradores = capturar_compradores()
inserir_compradores(novos_compradores)
# Criar tabela de hedge funds e bancos
cursor.execute("""
CREATE TABLE IF NOT EXISTS hedge_funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    capital_disponivel REAL,
    regiao TEXT,
    setor_preferido TEXT
)
""")

# Criar um sistema de matching entre compradores e fundos de investimento
def encontrar_fundos_para_comprador(comprador_setor, comprador_regiao):
    cursor.execute("""
        SELECT * FROM hedge_funds
        WHERE setor_preferido = ? AND regiao = ?
        ORDER BY capital_disponivel DESC
    """, (comprador_setor, comprador_regiao))
    
    return cursor.fetchall()

# Exemplo de matching
comprador_exemplo = ("Agronegócio", "América do Norte")
fundos_recomendados = encontrar_fundos_para_comprador(*comprador_exemplo)

print("Fundos recomendados:", fundos_recomendados)
# Criar tabela de eventos exclusivos
cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    data TEXT,
    local TEXT,
    tipo TEXT,  -- 'painel', 'networking', 'lançamento'
    status TEXT DEFAULT 'planejado'
)
""")

# Inserir evento estratégico
def criar_evento(nome, data, local, tipo):
    cursor.execute("INSERT INTO eventos (nome, data, local, tipo) VALUES (?, ?, ?, ?)", 
                   (nome, data, local, tipo))
    conn.commit()

criar_evento("Cúpula Global de Commodities", "2025-09-15", "Dubai", "painel")
import requests

def verificar_credito_comprador(cnpj):
    url = f"https://api.serasa.com/credito?cnpj={cnpj}"
    headers = {"Authorization": "Bearer SEU_TOKEN"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Não foi possível verificar crédito"}

# Exemplo de uso
cnpj_teste = "00.000.000/0001-00"
resultado_credito = verificar_credito_comprador(cnpj_teste)
print(resultado_credito)
from fastapi import FastAPI

app = FastAPI()

# Rota para listar compradores validados
@app.get("/compradores")
def listar_compradores():
    cursor.execute("SELECT * FROM compradores WHERE validado = 1")
    compradores = cursor.fetchall()
    return {"compradores": compradores}

# Rota para listar eventos estratégicos
@app.get("/eventos")
def listar_eventos():
    cursor.execute("SELECT * FROM eventos WHERE status = 'planejado'")
    eventos = cursor.fetchall()
    return {"eventos": eventos}

uvicorn nome_do_arquivo:app --reload
