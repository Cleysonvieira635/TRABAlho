import requests
import sqlite3
import pandas as pd
from textblob import TextBlob
from pytrends.request import TrendReq
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px

# Conectar ao banco de dados
conn = sqlite3.connect('predicao_demanda.db')
cursor = conn.cursor()

# Criar tabela para armazenar dados de compra
cursor.execute("""
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    preco REAL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Capturar tendências do Google Trends
def obter_tendencias_google(produto):
    pytrends = TrendReq()
    pytrends.build_payload([produto], timeframe='today 3-m')
    data = pytrends.interest_over_time()
    if not data.empty:
        return data
    return None

# Análise de Sentimento
def analise_sentimento(texto):
    blob = TextBlob(texto)
    return blob.sentiment.polarity

# Capturar dados climáticos (NOAA, Agroclima, USDA Crop Reports)
def obter_dados_climaticos(api, url, params=None):
    headers = {"Authorization": f"Bearer {api}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# Construir modelo preditivo
def treinar_modelo():
    dados = pd.read_sql_query("SELECT preco FROM compras", conn)
    if dados.empty:
        print("Sem dados para treinar o modelo.")
        return None
    
    X = dados.index.values.reshape(-1, 1)
    y = dados['preco']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    modelo = RandomForestRegressor()
    modelo.fit(X_train, y_train)
    
    return modelo

# Previsão de demanda
def prever_demanda(modelo):
    futuro = [[len(pd.read_sql_query("SELECT * FROM compras", conn)) + i] for i in range(1, 11)]
    previsoes = modelo.predict(futuro)
    return previsoes

# Visualização no Power BI (Gerar gráfico interativo)
def visualizar_dados():
    dados = pd.read_sql_query("SELECT data, preco FROM compras", conn)
    fig = px.line(dados, x='data', y='preco', title='Evolução de Preços')
    fig.show()

# Exemplo de execução
modelo = treinar_modelo()
if modelo:
    previsoes = prever_demanda(modelo)
    print("Previsões para os próximos dias:", previsoes)
    visualizar_dados()

conn.close()