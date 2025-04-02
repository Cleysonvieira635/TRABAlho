import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from googlesearch import search
from fastapi import FastAPI
import sqlite3

# Configuração do banco de dados SQLite
conn = sqlite3.connect("compradores.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS compradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        linkedin TEXT,
        setor TEXT,
        empresa TEXT,
        interesse TEXT
    )
""")
conn.commit()

# Função para buscar dados do comprador no LinkedIn e Google

def pesquisar_comprador(nome):
    try:
        resultados = list(search(f"{nome} site:linkedin.com", num_results=5))
        return resultados if resultados else None
    except Exception as e:
        print(f"Erro ao pesquisar comprador: {e}")
        return None

# Web Scraping para LinkedIn (Exemplo: Usando Selenium)
def buscar_perfil_linkedin(url):
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service("/caminho/para/chromedriver"), options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        nome = soup.find("title").text.strip()
        return nome if nome else "Perfil não encontrado"
    except Exception as e:
        print(f"Erro ao buscar perfil no LinkedIn: {e}")
        return "Erro ao buscar perfil"

# Função para armazenar comprador no banco de dados
def adicionar_comprador(nome, email, linkedin, setor, empresa, interesse):
    try:
        cursor.execute("INSERT INTO compradores (nome, email, linkedin, setor, empresa, interesse) VALUES (?, ?, ?, ?, ?, ?)",
                       (nome, email, linkedin, setor, empresa, interesse))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Email já cadastrado")
    except Exception as e:
        print(f"Erro ao adicionar comprador: {e}")

# API com FastAPI
app = FastAPI()

@app.post("/adicionar_comprador/")
def api_adicionar_comprador(nome: str, email: str, setor: str, empresa: str, interesse: str):
    linkedin = pesquisar_comprador(nome)
    if linkedin:
        adicionar_comprador(nome, email, linkedin[0], setor, empresa, interesse)
        return {"status": "Comprador adicionado com sucesso", "linkedin": linkedin[0]}
    return {"status": "Não foi possível encontrar o perfil"}

@app.get("/listar_compradores/")
def listar_compradores():
    try:
        cursor.execute("SELECT * FROM compradores")
        compradores = cursor.fetchall()
        return {"compradores": compradores}
    except Exception as e:
        print(f"Erro ao listar compradores: {e}")
        return {"erro": "Falha ao recuperar dados"}

# Exemplo de Uso
if __name__ == "__main__":
    nome_teste = "Carlos Silva"
    linkedin_perfil = pesquisar_comprador(nome_teste)
    print(f"Perfil LinkedIn encontrado: {linkedin_perfil}")
