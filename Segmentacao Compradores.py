import sqlite3
import pandas as pd
import requests
from fastapi import FastAPI
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Inicializa a API
app = FastAPI()

# Configuração do banco de dados
def criar_banco():
    conn = sqlite3.connect('compradores.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS compradores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        setor TEXT,
                        volume_anual REAL,
                        localizacao TEXT,
                        categoria TEXT)''')
    conn.commit()
    conn.close()

criar_banco()

# Função para inserir compradores no banco de dados
def inserir_comprador(nome, setor, volume_anual, localizacao, categoria):
    conn = sqlite3.connect('compradores.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO compradores (nome, setor, volume_anual, localizacao, categoria) VALUES (?, ?, ?, ?, ?)",
                   (nome, setor, volume_anual, localizacao, categoria))
    conn.commit()
    conn.close()

# Função para buscar dados de APIs externas (exemplo: crédito e mercado)
def buscar_dados_api(url, params={}):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao acessar API: {e}")
        return None

# Rota para cadastrar um comprador
@app.post("/cadastrar_comprador")
def cadastrar_comprador(nome: str, setor: str, volume_anual: float, localizacao: str, categoria: str):
    inserir_comprador(nome, setor, volume_anual, localizacao, categoria)
    return {"status": "Comprador cadastrado com sucesso"}

# Rota para listar compradores
@app.get("/listar_compradores")
def listar_compradores():
    conn = sqlite3.connect('compradores.db')
    df = pd.read_sql_query("SELECT * FROM compradores", conn)
    conn.close()
    return df.to_dict(orient="records")

# Modelo de machine learning para prever categoria de compradores
def treinar_modelo():
    conn = sqlite3.connect('compradores.db')
    df = pd.read_sql_query("SELECT setor, volume_anual, categoria FROM compradores", conn)
    conn.close()
    
    if df.empty:
        return None
    
    label_encoder = LabelEncoder()
    df['setor_encoded'] = label_encoder.fit_transform(df['setor'])
    X = df[['setor_encoded', 'volume_anual']]
    y = df['categoria']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model, label_encoder

modelo, encoder = treinar_modelo()

# Rota para prever categoria de um comprador com base nos dados
@app.get("/prever_categoria")
def prever_categoria(setor: str, volume_anual: float):
    if modelo is None:
        return {"erro": "Modelo ainda não treinado"}
    setor_encoded = encoder.transform([setor])[0]
    categoria_prevista = modelo.predict([[setor_encoded, volume_anual]])[0]
    return {"categoria_prevista": categoria_prevista}

# Rodar API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)