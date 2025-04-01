import sqlite3
import requests
import schedule
import time
from fastapi import FastAPI
from transformers import pipeline

# Configuração do banco de dados
def criar_banco():
    conn = sqlite3.connect("compradores.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT UNIQUE,
            empresa TEXT,
            interesse TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            data TEXT,
            local TEXT,
            status TEXT DEFAULT 'pendente'
        )
    """)
    conn.commit()
    conn.close()

# Função para buscar compradores qualificados (exemplo com API fictícia)
def coletar_compradores():
    url = "https://api.exclusivedatabase.com/compradores"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        conn = sqlite3.connect("compradores.db")
        cursor = conn.cursor()
        for comprador in dados["compradores"][:1000]:
            try:
                cursor.execute("INSERT INTO compradores (nome, email, empresa, interesse) VALUES (?, ?, ?, ?)",
                               (comprador["nome"], comprador["email"], comprador["empresa"], comprador["interesse"]))
            except sqlite3.IntegrityError:
                pass  # Evita duplicatas
        conn.commit()
        conn.close()
    else:
        print("Erro ao coletar compradores")

# Modelo de NLP para automação de follow-ups
nlp = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def gerar_mensagem(nome, interesse):
    prompt = f"Olá {nome}, percebemos seu interesse em {interesse}. Gostaria de conversar sobre oportunidades?"
    return nlp(prompt, max_length=50)[0]["generated_text"]

def enviar_followups():
    conn = sqlite3.connect("compradores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, interesse FROM compradores")
    compradores = cursor.fetchall()
    for nome, email, interesse in compradores:
        mensagem = gerar_mensagem(nome, interesse)
        print(f"Enviando email para {email}: {mensagem}")  # Aqui pode ser integrada uma API de envio de e-mails
    conn.close()

# Buscar eventos globais de commodities
def coletar_eventos():
    url = "https://api.commodityevents.com/events"
    response = requests.get(url)
    if response.status_code == 200:
        eventos = response.json()
        conn = sqlite3.connect("compradores.db")
        cursor = conn.cursor()
        for evento in eventos["eventos"][:3]:
            cursor.execute("INSERT INTO eventos (nome, data, local) VALUES (?, ?, ?)",
                           (evento["nome"], evento["data"], evento["local"]))
        conn.commit()
        conn.close()
    else:
        print("Erro ao coletar eventos")

# API para acesso aos dados
app = FastAPI()

@app.get("/compradores")
def listar_compradores():
    conn = sqlite3.connect("compradores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM compradores")
    compradores = cursor.fetchall()
    conn.close()
    return {"compradores": compradores}

@app.get("/eventos")
def listar_eventos():
    conn = sqlite3.connect("compradores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos")
    eventos = cursor.fetchall()
    conn.close()
    return {"eventos": eventos}

# Agendamento de tarefas
schedule.every().day.at("08:00").do(coletar_compradores)
schedule.every().day.at("09:00").do(enviar_followups)
schedule.every(30).days.do(coletar_eventos)

if __name__ == "__main__":
    criar_banco()
    while True:
        schedule.run_pending()
        time.sleep(60)
