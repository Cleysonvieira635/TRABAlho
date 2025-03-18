import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import datetime
# Exemplo de um DataFrame com dados históricos de preços e informações financeiras
# Supondo que você tenha uma tabela que inclui preço de commodity, receita, despesas, e outros dados financeiros.

df = pd.read_csv('historico_comodities_financeiro.csv')

# Estrutura do CSV:
# | data       | preco_comodidade | receita | despesa | margem_bruta | demanda |
# |------------|------------------|---------|---------|--------------|---------|

df['data'] = pd.to_datetime(df['data'])
df['preco_comodidade'] = df['preco_comodidade'].astype(float)
df['receita'] = df['receita'].astype(float)
df['despesa'] = df['despesa'].astype(float)
df['margem_bruta'] = df['margem_bruta'].astype(float)
df['demanda'] = df['demanda'].astype(float)

# Selecionando variáveis para prever o preço e analisar as finanças
X = df[['receita', 'despesa', 'demanda']]
y = df['preco_comodidade']
# Dividindo os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Usando regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Prevendo o preço no conjunto de teste
y_pred = model.predict(X_test)

# Avaliando o modelo
mse = mean_squared_error(y_test, y_pred)
print(f"Erro Quadrático Médio (MSE): {mse}")

# Exibindo as previsões e valores reais
print(f"Previsões: {y_pred}")
print(f"Valores Reais: {y_test.values}")
def calcular_faturamento(preco_comodidade, demanda):
    return preco_comodidade * demanda

def calcular_lucro_bruto(receita, despesa):
    return receita - despesa

# Previsão de faturamento com base no preço e demanda
faturamento_previsto = calcular_faturamento(preco_comodidade=300, demanda=50000)
print(f"Faturamento previsto: {faturamento_previsto}")

# Cálculo de lucro bruto
lucro_bruto = calcular_lucro_bruto(receita=15000000, despesa=12000000)
print(f"Lucro Bruto: {lucro_bruto}")
def calcular_saldo_caixa(receita, despesa, saldo_inicial):
    return saldo_inicial + receita - despesa

# Prevendo a necessidade de crédito
def prever_necessidade_credito(saldo_caixa, saldo_minimo):
    if saldo_caixa < saldo_minimo:
        return saldo_minimo - saldo_caixa  # O quanto é necessário para atingir o saldo mínimo
    else:
        return 0

# Exemplo de uso
saldo_inicial = 500000  # Exemplo de saldo inicial
receita = 15000000
despesa = 12000000
saldo_caixa = calcular_saldo_caixa(receita, despesa, saldo_inicial)

# Definindo um saldo mínimo desejado
saldo_minimo = 1000000

necessidade_credito = prever_necessidade_credito(saldo_caixa, saldo_minimo)
print(f"Necessidade de Crédito: {necessidade_credito}")
from sqlalchemy import create_engine

# Criando a conexão com o banco de dados
engine = create_engine('mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco')

# Salvando os dados financeiros e previsões no banco de dados
df.to_sql('historico_comodities_financeiro', con=engine, if_exists='replace', index=False)

# Salvando previsões em uma tabela separada
previsoes_df = pd.DataFrame({'data': df['data'], 'previsao_preco': y_pred})
previsoes_df.to_sql('previsoes_comodities', con=engine, if_exists='replace', index=False)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/previsao', methods=['GET'])
def previsao():
    return jsonify({"previsao": y_pred.tolist()})

@app.route('/faturamento', methods=['GET'])
def faturamento():
    return jsonify({"faturamento_previsto": faturamento_previsto})

@app.route('/lucro', methods=['GET'])
def lucro():
    return jsonify({"lucro_bruto": lucro_bruto})

if __name__ == '__main__':
    app.run(debug=True)
