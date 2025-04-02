import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

class PrevisaoDemanda:
    def __init__(self, dados):
        self.dados = dados
        self.modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def treinar_modelo(self):
        X = self.dados[["mes", "preco_mercado", "estoque"]]
        y = self.dados["demanda_real"]
        X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
        self.modelo.fit(X_treino, y_treino)
        y_pred = self.modelo.predict(X_teste)
        erro = mean_absolute_error(y_teste, y_pred)
        print(f"Erro médio da previsão: {erro:.2f}")
    
    def prever(self, mes, preco, estoque):
        entrada = np.array([[mes, preco, estoque]])
        return self.modelo.predict(entrada)[0]

class Contrato:
    def __init__(self, comprador, produto, quantidade, preco_unitario, prazo, tipo_pagamento):
        self.comprador = comprador
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.prazo = prazo
        self.tipo_pagamento = tipo_pagamento
        self.valor_total = quantidade * preco_unitario
    
    def gerar_contrato(self):
        return f"""
        CONTRATO DE VENDA DE COMMODITIES
        ----------------------------------
        Comprador: {self.comprador}
        Produto: {self.produto}
        Quantidade: {self.quantidade} toneladas
        Preço Unitário: ${self.preco_unitario}/tonelada
        Valor Total: ${self.valor_total}
        Prazo de Entrega: {self.prazo} dias
        Forma de Pagamento: {self.tipo_pagamento}
        """

def calcular_proposta(preco_base, frete, hedge, desconto_volume):
    return preco_base + frete - hedge - desconto_volume

dados = pd.DataFrame({
    "mes": np.arange(1, 13),
    "preco_mercado": np.random.randint(500, 800, 12),
    "estoque": np.random.randint(50, 200, 12),
    "demanda_real": np.random.randint(100, 300, 12)
})

previsao = PrevisaoDemanda(dados)
previsao.treinar_modelo()
print("Demanda prevista:", previsao.prever(6, 700, 120))

contrato = Contrato("Empresa X", "Soja", 100, 620, 30, "Carta de Crédito")
print(contrato.gerar_contrato())

oferta = calcular_proposta(600, 50, 30, 10)
print(f"Oferta final: ${oferta}/tonelada")
