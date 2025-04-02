import requests
import pandas as pd

def get_fao_data():
    url = "http://www.fao.org/faostat/api/v1/en/data/QC"
    params = {"area": "all", "item": "all", "element": "all", "format": "json"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Erro ao acessar FAO: {response.status_code}"

def get_ocde_reports():
    ocde_url = "https://stats.oecd.org/"
    try:
        response = requests.get(ocde_url)
        if response.status_code == 200:
            return "Relatórios da OCDE acessados com sucesso."
        else:
            return f"Erro ao acessar OCDE: {response.status_code}"
    except Exception as e:
        return f"Erro: {e}"

def get_bloomberg_data():
    api_key = "SUA_CHAVE_AQUI"
    url = "https://api.bloomberg.com/data/commodities"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Erro ao acessar Bloomberg: {response.status_code}"
    except Exception as e:
        return f"Erro: {e}"

# Chamando as funções
dados_fao = get_fao_data()
dados_ocde = get_ocde_reports()
dados_bloomberg = get_bloomberg_data()

print(dados_fao)
print(dados_ocde)
print(dados_bloomberg)
