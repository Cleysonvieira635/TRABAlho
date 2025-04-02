import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
import smtplib
import json
import sqlite3
from fastapi import FastAPI

# Configurar banco de dados SQLite
conn = sqlite3.connect('compradores.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS compradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    origem TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# FastAPI
app = FastAPI()

# Web Scraping para extrair compradores
headers = {'User-Agent': 'Mozilla/5.0'}
def extrair_compradores(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    compradores = []
    for item in soup.find_all('div', class_='comprador-info'):
        nome = item.find('h2').text.strip()
        email = item.find('a', class_='email').text.strip()
        compradores.append({'nome': nome, 'email': email, 'origem': url})
    return compradores

# Salvar compradores no banco de dados
def salvar_comprador(nome, email, origem):
    try:
        cursor.execute("INSERT INTO compradores (nome, email, origem) VALUES (?, ?, ?)", (nome, email, origem))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"O comprador {email} já está cadastrado.")

# Automação de e-mails via SMTP
def enviar_email(destinatario, assunto, mensagem):
    remetente = 'seuemail@gmail.com'
    senha = 'suasenha'
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())

# Integração com Pipedrive
PIPEDRIVE_API_KEY = "SUA_API_KEY"
def adicionar_contato_pipedrive(nome, email):
    url = f"https://api.pipedrive.com/v1/persons?api_token={PIPEDRIVE_API_KEY}"
    dados = {"name": nome, "email": email}
    response = requests.post(url, json=dados)
    return response.json()

# Monitoramento de Grupos no Telegram
def obter_mensagens_telegram(token, chat_id):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    mensagens = response.json()
    return mensagens

# Automação de Google Ads
def criar_campanha_google_ads():
    url = "https://googleads.googleapis.com/v11/customers/{customer_id}/campaigns"
    headers = {"Authorization": "Bearer SUA_CHAVE_API", "Content-Type": "application/json"}
    payload = {
        "name": "Campanha Importadores Soja",
        "status": "ENABLED",
        "advertisingChannelType": "SEARCH",
        "biddingStrategyType": "MANUAL_CPC",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Rotas API FastAPI
@app.get("/compradores")
def listar_compradores():
    cursor.execute("SELECT * FROM compradores")
    compradores = cursor.fetchall()
    return {"compradores": compradores}

@app.post("/adicionar_comprador")
def adicionar_comprador_api(nome: str, email: str, origem: str):
    salvar_comprador(nome, email, origem)
    return {"status": "Comprador adicionado com sucesso"}

# Executar Web Scraping e salvar compradores
if __name__ == "__main__":
    urls = ["https://exemplo.com/compradores1", "https://exemplo.com/compradores2"]
    for url in urls:
        compradores = extrair_compradores(url)
        for comprador in compradores:
            salvar_comprador(comprador['nome'], comprador['email'], comprador['origem'])
            adicionar_contato_pipedrive(comprador['nome'], comprador['email'])
            enviar_email(comprador['email'], "Oferta de Commodities", "Temos ótimas ofertas para você!")
    print("Processo concluído!")