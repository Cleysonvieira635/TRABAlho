import time
import pandas as pd
import sqlite3
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from fastapi import FastAPI
from datetime import datetime
import json

# Banco de dados
conn = sqlite3.connect("dados_commodities.db")
cursor = conn.cursor()

# Criar tabelas no banco de dados
cursor.execute("""
CREATE TABLE IF NOT EXISTS leiloes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    preco_atual TEXT,
    encerramento TEXT,
    data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS compras_governamentais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descricao TEXT,
    valor TEXT,
    data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS importacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    origem TEXT,
    data_chegada TEXT,
    valor TEXT,
    data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# FastAPI para acessar os dados via API
app = FastAPI()

@app.get("/leiloes")
def listar_leiloes():
    cursor.execute("SELECT * FROM leiloes ORDER BY data_extracao DESC")
    leiloes = cursor.fetchall()
    return {"leiloes": leiloes}

@app.get("/compras_governamentais")
def listar_compras_governamentais():
    cursor.execute("SELECT * FROM compras_governamentais ORDER BY data_extracao DESC")
    compras = cursor.fetchall()
    return {"compras_governamentais": compras}

@app.get("/importacoes")
def listar_importacoes():
    cursor.execute("SELECT * FROM importacoes ORDER BY data_extracao DESC")
    importacoes = cursor.fetchall()
    return {"importacoes": importacoes}

# Funções de web scraping

# Função para capturar leilões de commodities
def capturar_leiloes():
    url = "https://www.leiloescommodities.com.br"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    leiloes = []
    for item in soup.find_all("div", class_="leilao"):
        produto = item.find("h2").text.strip()
        preco_atual = item.find("span", class_="preco").text.strip()
        encerramento = item.find("span", class_="data").text.strip()
        leiloes.append((produto, preco_atual, encerramento))
    
    cursor.executemany("INSERT INTO leiloes (produto, preco_atual, encerramento) VALUES (?, ?, ?)", leiloes)
    conn.commit()
    driver.quit()

# Função para capturar compras governamentais
def capturar_compras_governamentais():
    url = "https://www.portaldecompras.gov.br/licitacoes"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    compras = []
    for item in soup.find_all("div", class_="licitacao"):
        titulo = item.find("h2").text.strip()
        descricao = item.find("p").text.strip()
        valor = item.find("span", class_="valor").text.strip()
        compras.append((titulo, descricao, valor))
    
    cursor.executemany("INSERT INTO compras_governamentais (titulo, descricao, valor) VALUES (?, ?, ?)", compras)
    conn.commit()
    driver.quit()

# Função para capturar dados de importações usando API
def capturar_importacoes():
    url = "https://api.exemplo.com/importacoes"  # URL fictícia da API
    response = requests.get(url)
    dados_importacao = response.json()
    
    importacoes = []
    for item in dados_importacao['data']:
        produto = item["produto"]
        origem = item["origem"]
        data_chegada = item["data_chegada"]
        valor = item["valor"]
        importacoes.append((produto, origem, data_chegada, valor))
    
    cursor.executemany("INSERT INTO importacoes (produto, origem, data_chegada, valor) VALUES (?, ?, ?, ?)", importacoes)
    conn.commit()

# Função de análise preditiva de demanda com Machine Learning
def analise_predictiva_demanda():
    # Exemplo de dados para análise preditiva (substituir por dados reais)
    dados = pd.read_sql_query("SELECT * FROM leiloes", conn)
    dados['preco_atual'] = dados['preco_atual'].apply(pd.to_numeric, errors='coerce')
    dados = dados.dropna()

    X = dados[['preco_atual']]  # Previsores
    y = dados['preco_atual']  # Variável alvo

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar os dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Previsão
    previsoes = model.predict(X_test)
    print(f"Previsões: {previsoes}")

# Função para monitoramento de padrões de importação
def monitorar_importacoes():
    # Exemplo simples de monitoramento
    cursor.execute("SELECT produto, valor FROM importacoes")
    importacoes = cursor.fetchall()
    for produto, valor in importacoes:
        if float(valor) < 1000:  # Exemplo de regra de monitoramento
            print(f"Alerta! Produto {produto} abaixo do valor esperado: {valor}")

# Loop para executar as funções periodicamente
def executar_monitoramento():
    while True:
        capturar_leiloes()
        capturar_compras_governamentais()
        capturar_importacoes()
        analise_predictiva_demanda()
        monitorar_importacoes()
        time.sleep(3600)  # Espera 1 hora para rodar novamente

if __name__ == "__main__":
    executar_monitoramento()
