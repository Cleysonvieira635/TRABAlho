import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Função para buscar importadores via API Tridge
def buscar_importadores(api_key, pais):
    url = f"https://api.tridge.com/importadores?pais={pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Falha ao acessar banco de dados"}

# Função para buscar dados alfandegários
def buscar_dados_alfandegarios(api_key, pais):
    url = f"https://api.customsdata.com/{pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Erro ao acessar dados alfandegários"}

# Função para buscar exportações via API Sicex
def buscar_exportacoes(api_key, pais):
    url = f"https://api.sicex.com/exportacoes?pais={pais}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": "Erro ao acessar Sicex"}

# Criando a aplicação FastAPI
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

# Rota para servir o HTML com o React embutido
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return f.read()

# Rodando o servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)