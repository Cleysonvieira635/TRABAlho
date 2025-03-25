import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('demanda_artificial.db')
cursor = conn.cursor()

# Criar tabela de acordos de pré-compra
cursor.execute("""
CREATE TABLE IF NOT EXISTS acordos_precompra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    distribuidor TEXT,
    produto TEXT,
    quantidade INTEGER,
    data_acordo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Criar tabela de notícias financeiras monitoradas
cursor.execute("""
CREATE TABLE IF NOT EXISTS noticias_financeiras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    fonte TEXT,
    impacto TEXT,  -- 'positivo', 'negativo', 'neutro'
    data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Criar tabela de campanhas de influência de mídia
cursor.execute("""
CREATE TABLE IF NOT EXISTS campanhas_midia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    canal TEXT,
    tipo TEXT,  -- 'relatório', 'publicidade', 'notícia manipulada'
    impacto TEXT,  -- 'alta demanda', 'escassez', 'oportunidade'
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
# Função para registrar uma nova campanha de influência
def criar_campanha_influencia(canal, tipo, impacto):
    cursor.execute("INSERT INTO campanhas_midia (canal, tipo, impacto) VALUES (?, ?, ?)",
                   (canal, tipo, impacto))
    conn.commit()
    print(f"Campanha lançada: {canal} - {tipo} - Impacto: {impacto}")

# Criando campanhas de urgência
criar_campanha_influencia("Jornal Econômico", "relatório", "alta demanda")
criar_campanha_influencia("Portal de Commodities", "notícia manipulada", "escassez")
import requests
from bs4 import BeautifulSoup

# Função para capturar notícias de um portal financeiro
def capturar_noticias():
    url = "https://www.exemplo.com/noticias-financeiras"  # Altere para uma fonte real
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    noticias = []
    for artigo in soup.find_all("article"):
        titulo = artigo.find("h2").text
        fonte = "Exemplo Financeiro"
        impacto = "neutro"  # Definir impacto com análise de sentimento

        noticias.append((titulo, fonte, impacto))
        cursor.execute("INSERT INTO noticias_financeiras (titulo, fonte, impacto) VALUES (?, ?, ?)",
                       (titulo, fonte, impacto))

    conn.commit()
    return noticias
from textblob import TextBlob

# Função para analisar sentimento de uma notícia
def analisar_sentimento(texto):
    analise = TextBlob(texto)
    polaridade = analise.sentiment.polarity

    if polaridade > 0:
        return "positivo"
    elif polaridade < 0:
        return "negativo"
    else:
        return "neutro"

# Aplicar análise de sentimento às notícias capturadas
def atualizar_impacto_noticias():
    cursor.execute("SELECT id, titulo FROM noticias_financeiras WHERE impacto = 'neutro'")
    noticias = cursor.fetchall()

    for id_noticia, titulo in noticias:
        impacto = analisar_sentimento(titulo)
        cursor.execute("UPDATE noticias_financeiras SET impacto = ? WHERE id = ?", (impacto, id_noticia))

    conn.commit()

atualizar_impacto_noticias()
# Criar um acordo de pré-compra estratégico
def criar_acordo_precompra(distribuidor, produto, quantidade):
    cursor.execute("INSERT INTO acordos_precompra (distribuidor, produto, quantidade) VALUES (?, ?, ?)",
                   (distribuidor, produto, quantidade))
    conn.commit()
    print(f"Acordo de pré-compra criado: {distribuidor} reservou {quantidade} unidades de {produto}.")

# Criando acordos com distribuidores para simular escassez
criar_acordo_precompra("Distribuidor X", "Soja", 50000)
criar_acordo_precompra("Distribuidor Y", "Milho", 30000)
from fastapi import FastAPI

app = FastAPI()

# Rota para listar campanhas de influência
@app.get("/campanhas_midia")
def listar_campanhas():
    cursor.execute("SELECT * FROM campanhas_midia")
    campanhas = cursor.fetchall()
    return {"campanhas": campanhas}

# Rota para listar notícias financeiras monitoradas
@app.get("/noticias_financeiras")
def listar_noticias():
    cursor.execute("SELECT * FROM noticias_financeiras")
    noticias = cursor.fetchall()
    return {"noticias": noticias}

# Rota para listar acordos de pré-compra
@app.get("/acordos_precompra")
def listar_acordos():
    cursor.execute("SELECT * FROM acordos_precompra")
    acordos = cursor.fetchall()
    return {"acordos_precompra": acordos}


uvicorn nome_do_arquivo:app --reload

