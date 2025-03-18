import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import datetime
import random
# Exemplo de um DataFrame com dados históricos de produção e estoque
df = pd.DataFrame({
    'data': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'temperatura_media': np.random.normal(25, 5, 100),  # Temperatura média
    'umidade': np.random.normal(60, 10, 100),  # Umidade do solo
    'preco_comodidade': np.random.normal(300, 50, 100),  # Preço da commodity
    'produzido': np.random.normal(1000, 200, 100),  # Quantidade produzida
    'estoque': np.random.normal(500, 100, 100)  # Estoque disponível
})

# Exibindo os primeiros dados para verificar
df.head()
# Variáveis de entrada: temperatura média e umidade do solo
X = df[['temperatura_media', 'umidade']]
y = df['produzido']

# Dividindo os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criando e treinando o modelo de regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Fazendo previsões sobre a produção
y_pred = model.predict(X_test)

# Avaliando o modelo
mse = mean_squared_error(y_test, y_pred)
print(f"Erro Quadrático Médio (MSE): {mse}")

# Exibindo as previsões e valores reais
print(f"Previsões de produção: {y_pred}")
print(f"Valores reais de produção: {y_test.values}")
# Função para controlar o estoque
def controle_estoque(estoque_atual, quantidade_produzida, demanda_prevista):
    # Atualiza o estoque após a produção
    estoque_atual += quantidade_produzida
    
    # Consome o estoque com base na demanda prevista
    estoque_atual -= demanda_prevista
    
    # Se o estoque for negativo, retornamos zero
    if estoque_atual < 0:
        estoque_atual = 0
    
    return estoque_atual

# Simulando a reposição e consumo de estoque
estoque_atual = 500  # Estoque inicial
quantidade_produzida = random.randint(800, 1200)  # Quantidade produzida
demanda_prevista = random.randint(700, 1000)  # Demanda prevista

novo_estoque = controle_estoque(estoque_atual, quantidade_produzida, demanda_prevista)
print(f"Estoque após atualização: {novo_estoque}")
# Função para prever demanda
def prever_demanda(preco, estoque, producao):
    # A demanda aumenta quando o preço é baixo ou o estoque é alto, e diminui quando o preço é alto
    demanda = max(0, (1000 / preco) * (estoque / 1000) * (producao / 1000))
    return demanda

# Prevendo a demanda futura
demanda_futura = prever_demanda(preco=300, estoque=novo_estoque, producao=quantidade_produzida)
print(f"Demanda futura prevista: {demanda_futura}")
# Função para otimizar o uso de recursos (ex: água e fertilizantes)
def otimizar_recursos(producao, demanda):
    # A quantidade de recursos necessária depende da diferença entre produção e demanda
    if producao > demanda:
        recursos = producao * 0.1  # Menos recursos se a produção for alta
    else:
        recursos = producao * 0.2  # Mais recursos se a produção for baixa
    return recursos

# Calculando a otimização de recursos
recursos_necessarios = otimizar_recursos(producao=quantidade_produzida, demanda=demanda_futura)
print(f"Recursos necessários para otimização: {recursos_necessarios} unidades")
from sqlalchemy import create_engine

# Criando a conexão com o banco de dados
engine = create_engine('mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco')

# Salvando o DataFrame no banco de dados
df.to_sql('historico_producao_estoque', con=engine, if_exists='replace', index=False)

# Salvando as previsões de produção em uma tabela separada
previsoes_df = pd.DataFrame({'data': df['data'], 'previsao_producao': y_pred})
previsoes_df.to_sql('previsoes_producao', con=engine, if_exists='replace', index=False)
