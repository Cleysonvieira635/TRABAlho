import sqlite3
import requests
import smtplib
import schedule
import time
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔹 Conexão com o banco de dados SQLite
conn = sqlite3.connect('compradores.db', check_same_thread=False)
cursor = conn.cursor()

# 🔹 Criar tabela de compradores se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS compradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    empresa TEXT,
    pais TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# 🔹 Função para buscar compradores via API (Exemplo: Tridge, AgFlow)
def buscar_compradores():
    api_urls = [
        "https://api.tridge.com/buyers",
        "https://api.agflow.com/compradores"
    ]
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        print("⚠️ API_KEY não configurada. Configure a variável de ambiente.")
        return
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for url in api_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            compradores = response.json()
            
            if isinstance(compradores, list):  # Verifica se a resposta é uma lista válida
                for comprador in compradores:
                    cursor.execute("INSERT OR IGNORE INTO compradores (nome, email, empresa, pais) VALUES (?, ?, ?, ?)", 
                                   (comprador.get("nome"), comprador.get("email"), comprador.get("empresa"), comprador.get("pais")))
                conn.commit()
                print(f"✅ Dados de compradores de {url} salvos com sucesso.")
            else:
                print(f"⚠️ Resposta inesperada da API {url}: {compradores}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao buscar compradores de {url}: {e}")

# 🔹 Função para envio de e-mails segmentados
def enviar_email(destinatario, assunto, mensagem):
    remetente = os.getenv("EMAIL_USER")
    senha = os.getenv("EMAIL_PASS")

    if not remetente or not senha:
        print("⚠️ Credenciais de e-mail não configuradas.")
        return

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(mensagem, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
        print(f"✅ E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail para {destinatario}: {e}")

# 🔹 Função para automação de mensagens no LinkedIn (API oficial necessária)
def enviar_mensagem_linkedin(usuario, mensagem):
    print(f"⚠️ A API oficial do LinkedIn deve ser usada. Mensagem para {usuario}: {mensagem}")
