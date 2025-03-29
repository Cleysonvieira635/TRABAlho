import sqlite3
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# Configuração do FastAPI
app = FastAPI()

# Conectar ao banco de dados e criar tabelas
def init_db():
    conn = sqlite3.connect('compradores_avancados.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        perfil_credito TEXT,  -- 'excelente', 'bom', 'regular', 'ruim'
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comprador_id INTEGER,
        valor REAL,
        tipo TEXT,  -- 'compra', 'pagamento', 'transferencia'
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (comprador_id) REFERENCES compradores(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bancos_parceiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        banco_nome TEXT,
        tipo_financiamento TEXT,  -- 'importacao', 'exportacao'
        comprador_id INTEGER,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (comprador_id) REFERENCES compradores(id)
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Modelo para entrada de dados
class Transacao(BaseModel):
    comprador_id: int
    valor: float
    tipo: str

# Função para acessar dados de crédito (exemplo com Serasa Experian)
def consultar_credito_serasa(cnpj):
    url = "https://api.serasaexperian.com/credito"
    params = {'cnpj': cnpj, 'api_key': 'SUA_API_KEY'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Falha ao consultar crédito", "status": response.status_code}

# Filtrar compradores qualificados
@app.get("/compradores_qualificados")
def obter_compradores_qualificados():
    conn = sqlite3.connect('compradores_avancados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM compradores WHERE perfil_credito IN ('excelente', 'bom')")
    compradores = cursor.fetchall()
    conn.close()
    return {"compradores_qualificados": compradores}

# Registrar transação
@app.post("/registrar_transacao")
def registrar_transacao_api(transacao: Transacao):
    conn = sqlite3.connect('compradores_avancados.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transacoes (comprador_id, valor, tipo) VALUES (?, ?, ?)",
                   (transacao.comprador_id, transacao.valor, transacao.tipo))
    conn.commit()
    conn.close()
    return {"status": "Transação registrada com sucesso"}

# Prever compra futura
@app.get("/prever_compra_futura")
def prever_compra_futura_api(comprador_id: int):
    conn = sqlite3.connect('compradores_avancados.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tipo, SUM(valor) 
        FROM transacoes 
        WHERE comprador_id = ? AND tipo = 'compra' 
        GROUP BY tipo
    """, (comprador_id,))
    transacoes = cursor.fetchall()
    conn.close()
    
    total_compras = sum(valor for tipo, valor in transacoes) if transacoes else 0
    previsao = total_compras > 10000  # Exemplo de critério
    return {"previsao_compra_futura": previsao}

# Criar parceria com banco
@app.post("/criar_parceria_banco")
def criar_parceria_banco_api(banco_nome: str, tipo_financiamento: str, comprador_id: int):
    conn = sqlite3.connect('compradores_avancados.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bancos_parceiros (banco_nome, tipo_financiamento, comprador_id) VALUES (?, ?, ?)",
                   (banco_nome, tipo_financiamento, comprador_id))
    conn.commit()
    conn.close()
    return {"status": "Parceria bancária criada com sucesso"}

# Listar parcerias bancárias
@app.get("/listar_parcerias_bancos")
def listar_parcerias_bancos_api():
    conn = sqlite3.connect('compradores_avancados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bancos_parceiros")
    parcerias = cursor.fetchall()
    conn.close()
    return {"parcerias_bancos": parcerias}
