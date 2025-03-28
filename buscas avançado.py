import requests
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

# Exemplo de API de importadores
def buscar_importadores(api_key, pais):
    url = f"https://api.tridge.com/importadores?pais={pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Falha ao acessar banco de dados"}

# Exemplo de API de Alfândega
def buscar_dados_alfandegarios(api_key, pais):
    url = f"https://api.customsdata.com/{pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Erro ao acessar dados alfandegários"}

# Exemplo de API de Exportações (Sicex)
def buscar_exportacoes(api_key, pais):
    url = f"https://api.sicex.com/exportacoes?pais={pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Erro ao acessar Sicex"}

# FastAPI - Criar rotas
app = FastAPI()

# API de Importadores
@app.get("/importadores/{pais}")
def listar_importadores(pais: str):
    api_key_tridge = "SUA_CHAVE_API"  # Substitua pela chave correta
    return buscar_importadores(api_key_tridge, pais)

# API de Dados Alfandegários
@app.get("/alfandega/{pais}")
def listar_dados_alfandega(pais: str):
    api_key_customs = "SUA_CHAVE_API"  # Substitua pela chave correta
    return buscar_dados_alfandegarios(api_key_customs, pais)

# API de Exportações
@app.get("/exportacoes/{pais}")
def listar_exportacoes(pais: str):
    api_key_sicex = "SUA_CHAVE_API"  # Substitua pela chave correta
    return buscar_exportacoes(api_key_sicex, pais)

# Serve os arquivos estáticos para o frontend React
app.mount("/static", StaticFiles(directory="static"), name="static")

# Servir o HTML com o React embutido
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Exemplo fictício de API de um banco de dados de importadores
def buscar_importadores(api_key, pais):
    url = f"https://api.tridge.com/importadores?pais={pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Falha ao acessar banco de dados"}

# Exemplo de uso
api_key_tridge = "SUA_CHAVE_API"
importadores_brasil = buscar_importadores(api_key_tridge, "Brasil")
print(importadores_brasil)

import blpapi

# Conectar ao Bloomberg Terminal
def consultar_bloomberg(ativo):
    session = blpapi.Session()
    session.start()
    session.openService("//blp/mktdata")
    service = session.getService("//blp/mktdata")
    
    request = service.createRequest("MarketDataRequest")
    request.append("securities", ativo)
    request.append("fields", "PX_LAST")  # Último preço

    session.sendRequest(request)
    return request

# Exemplo de consulta
dados = consultar_bloomberg("CORN COMDTY")
print(dados)
import pandas_datareader as pdr

# Obter preços de commodities via Reuters
dados = pdr.get_data_fred("DCOILWTICO")  # Exemplo: Preço do petróleo WTI
print(dados.tail())

def buscar_exportacoes(api_key, pais):
    url = f"https://api.sicex.com/exportacoes?pais={pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Erro ao acessar Sicex"}

# Exemplo de uso
api_key_sicex = "SUA_CHAVE_API"
exportacoes_brasil = buscar_exportacoes(api_key_sicex, "Brasil")
print(exportacoes_brasil)
from bs4 import BeautifulSoup

def capturar_exportacoes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dados = []
    for linha in soup.find_all("tr"):
        colunas = linha.find_all("td")
        if len(colunas) > 1:
            pais = colunas[0].text
            produto = colunas[1].text
            volume = colunas[2].text
            dados.append((pais, produto, volume))

    return dados

exportacoes = capturar_exportacoes("https://www.sicex.com/exportacoes")
print(exportacoes)

def buscar_dados_alfandegarios(api_key, pais):
    url = f"https://api.customsdata.com/{pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Erro ao acessar dados alfandegários"}

# Exemplo de uso
api_key_customs = "SUA_CHAVE_API"
dados_alfandegarios = buscar_dados_alfandegarios(api_key_customs, "Brasil")
print(dados_alfandegarios)

from fastapi import FastAPI

app = FastAPI()

# Rota para consultar importadores
@app.get("/importadores/{pais}")
def listar_importadores(pais: str):
    return buscar_importadores(api_key_tridge, pais)

# Rota para dados alfandegários
@app.get("/alfandega/{pais}")
def listar_dados_alfandega(pais: str):
    return buscar_dados_alfandegarios(api_key_customs, pais)
uvicorn app:app --reload

import React, { useEffect, useState } from "react";

function Importadores({ pais }) {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/importadores/${pais}`)
            .then((response) => response.json())
            .then((data) => setData(data));
    }, [pais]);

    return (
        <div>
            <h2>Importadores em {pais}</h2>
            <ul>
                {data.map((item, index) => (
                    <li key={index}>{item.nome} - {item.empresa}</li>
                ))}
            </ul>
        </div>
    );
}

export default Importadores;

/project
  ├── main.py
  └── static/
      ├── index.html
      └── app.js

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>API de Importadores e Alfândega</title>
  </head>
  <body>
    <div id="root"></div>
    <script src="/static/app.js"></script>
  </body>
</html>
import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";

function Importadores({ pais }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/importadores/${pais}`)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        setError("Erro ao carregar dados");
        setLoading(false);
      });
  }, [pais]);

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Importadores em {pais}</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item.nome} - {item.empresa}
          </li>
        ))}
      </ul>
    </div>
  );
}

function Exportacoes({ pais }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/exportacoes/${pais}`)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        setError("Erro ao carregar dados");
        setLoading(false);
      });
  }, [pais]);

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Exportações de {pais}</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item.pais} - {item.produto} - {item.volume}
          </li>
        ))}
      </ul>
    </div>
  );
}

function Alfandega({ pais }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/alfandega/${pais}`)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        setError("Erro ao carregar dados");
        setLoading(false);
      });
  }, [pais]);

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Dados Alfandegários de {pais}</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item.pais} - {item.produto} - {item.volume}
          </li>
        ))}
      </ul>
    </div>
  );
}

function App() {
  return (
    <div>
      <Importadores pais="Brasil" />
      <Exportacoes pais="Brasil" />
      <Alfandega pais="Brasil" />
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

pip install fastapi uvicorn requests

npx create-react-app static

uvicorn main:app --reload

npm start

