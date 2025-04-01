import sqlite3
import requests # type: ignore
from fastapi import FastAPI # type: ignore

# Conectar ao banco de dados
conn = sqlite3.connect('financiamento_comercio.db')
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS compradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    cnpj TEXT UNIQUE,
    setor TEXT,
    perfil_credito TEXT,  -- 'excelente', 'bom', 'regular', 'ruim'
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS financiamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comprador_id INTEGER,
    banco TEXT,
    valor REAL,
    tipo TEXT,  -- 'importacao', 'exportacao'
    status TEXT,  -- 'aprovado', 'pendente', 'negado'
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comprador_id) REFERENCES compradores(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS camaras_comerciais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    pais TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# FastAPI
app = FastAPI()

# Função para buscar financiamentos disponíveis via APIs bancárias
def buscar_financiamento_api(banco, cnpj):
    apis = {
        "HSBC": "https://api.hsbc.com/trade-finance",
        "Rabobank": "https://api.rabobank.com/finance",
        "Banco do Brasil": "https://api.bb.com.br/exportacao",
        "BNDES": "https://api.bndes.gov.br/credito"
    }
    
    url = apis.get(banco)
    if not url:
        return {"erro": "Banco não suportado"}
    
    params = {"cnpj": cnpj, "api_key": "SUA_API_KEY"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"erro": "Falha na API"}

# API para registrar comprador
@app.post("/registrar_comprador")
def registrar_comprador(nome: str, email: str, cnpj: str, setor: str, perfil_credito: str):
    cursor.execute("INSERT INTO compradores (nome, email, cnpj, setor, perfil_credito) VALUES (?, ?, ?, ?, ?)",
                   (nome, email, cnpj, setor, perfil_credito))
    conn.commit()
    return {"status": "Comprador registrado com sucesso"}

# API para consultar financiamentos
@app.get("/consultar_financiamento")
def consultar_financiamento(cnpj: str, banco: str):
    return buscar_financiamento_api(banco, cnpj)

# API para registrar financiamento
@app.post("/registrar_financiamento")
def registrar_financiamento(comprador_id: int, banco: str, valor: float, tipo: str, status: str):
    cursor.execute("INSERT INTO financiamentos (comprador_id, banco, valor, tipo, status) VALUES (?, ?, ?, ?, ?)",
                   (comprador_id, banco, valor, tipo, status))
    conn.commit()
    return {"status": "Financiamento registrado"}

# API para listar compradores qualificados
@app.get("/compradores_qualificados")
def compradores_qualificados():
    cursor.execute("SELECT * FROM compradores WHERE perfil_credito IN ('excelente', 'bom')")
    return {"compradores": cursor.fetchall()}

# API para listar câmaras comerciais
@app.get("/listar_camaras")
def listar_camaras():
    cursor.execute("SELECT * FROM camaras_comerciais")
    return {"camaras": cursor.fetchall()}

# Rodar servidor: uvicorn nome_do_arquivo:app --reload
