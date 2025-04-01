import requests
import sqlite3
from bs4 import BeautifulSoup
from fastapi import FastAPI
import schedule
import time

# Configuração do banco de dados
conn = sqlite3.connect('networking.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos_exclusivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    localizacao TEXT,
    data TEXT,
    link TEXT
)
""")
conn.commit()

# Função para buscar eventos exclusivos
def buscar_eventos_exclusivos():
    urls = [
        "https://www.londoncommoditiesclub.com/events",
        "https://www.globalgrain.com/meetings",
        "https://www.dubaibusinessnetwork.com",
        "https://www.singaporebusinessclub.com"
    ]
    
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            eventos = soup.find_all('div', class_='event-card')
            
            for evento in eventos:
                nome = evento.find('h2').text
                localizacao = evento.find('span', class_='location').text
                data = evento.find('span', class_='date').text
                link = evento.find('a')['href']
                
                cursor.execute("""
                    INSERT INTO eventos_exclusivos (nome, localizacao, data, link)
                    VALUES (?, ?, ?, ?)
                """, (nome, localizacao, data, link))
                conn.commit()
                print(f"Evento {nome} cadastrado no banco de dados.")
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

# API para acessar eventos exclusivos
app = FastAPI()

@app.get("/eventos_exclusivos")
def listar_eventos():
    cursor.execute("SELECT * FROM eventos_exclusivos")
    eventos = cursor.fetchall()
    return {"eventos": eventos}

# Agendamento para buscar eventos diariamente
schedule.every().day.at("08:00").do(buscar_eventos_exclusivos)

while True:
    schedule.run_pending()
    time.sleep(60)