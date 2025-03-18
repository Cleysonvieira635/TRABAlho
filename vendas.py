import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import requests
import datetime
def get_weather_data(city):
    api_key = 'sua_chave_api_aqui'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = {
            "temperature": main_data["temp"],
            "humidity": main_data["humidity"],
            "pressure": main_data["pressure"]
        }
        return weather_data
    else:
        return None
# Supondo que você tenha um arquivo CSV com dados históricos de preços
df = pd.read_csv('historico_precos.csv')

# Exemplo de como pode ser estruturado o arquivo
# | data       | preco_comodidade | clima_temperatura | oferta | demanda |
# |------------|------------------|-------------------|--------|---------|

# Processamento de dados
df['data'] = pd.to_datetime(df['data'])
df['preco_comodidade'] = df['preco_comodidade'].astype(float)

# Suponha que você tenha variáveis de previsão como "clima_temperatura", "oferta", "demanda"
X = df[['clima_temperatura', 'oferta', 'demanda']]
y = df['preco_comodidade']
# Dividindo os dados em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Usando regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Prevendo os preços no conjunto de teste
y_pred = model.predict(X_test)

# Avaliando o modelo
mse = mean_squared_error(y_test, y_pred)
print(f"Erro Quadrático Médio (MSE): {mse}")

# Exibindo as previsões e os valores reais
print(f"Previsões: {y_pred}")
print(f"Valores Reais: {y_test.values}")
# Dados de entrada para previsão (exemplo)
input_data = {
    "clima_temperatura": 25,  # Temperatura média (em °C)
    "oferta": 50000,  # Quantidade de oferta
    "demanda": 45000  # Quantidade de demanda
}

# Prevendo o preço
input_df = pd.DataFrame([input_data])
previsao = model.predict(input_df)

print(f"Previsão de preço para as condições atuais: {previsao[0]}")
# Prevendo a demanda futura
def prever_demanda(preco, clima, oferta):
    # Exemplo simples com base no preço e outras variáveis
    demanda_prevista = oferta * (1 - (preco * 0.01)) + clima * 0.5
    return demanda_prevista

# Exemplo de uso
demanda_futura = prever_demanda(preco=300, clima=25, oferta=50000)
print(f"Demanda futura prevista: {demanda_futura}")
from sqlalchemy import create_engine

# Criando a conexão com o banco de dados
engine = create_engine('mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco')

# Salvando o DataFrame de previsões no banco de dados
df.to_sql('previsoes_comodities', con=engine, if_exists='replace', index=False)
