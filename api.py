import time
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()  

COINGECKO_BASE  = "https://api.coingecko.com/api/v3"
CRYPTOPANIC_KEY = os.getenv("CRYPTOPANIC_API_KEY")


@st.cache_data(ttl=60)  
def buscar_cripto(cripto_id: str) -> dict | None:
    """
    Busca informações detalhadas de uma criptomoeda pelo seu ID.
    Ex: buscar_cripto("bitcoin") -> {...}
    Retorna None se a cripto não for encontrada.
    """
    url = f"{COINGECKO_BASE}/coins/{cripto_id.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        return {
            "nome":       dados["name"],
            "simbolo":    dados["symbol"].upper(),
            "preco":      dados["market_data"]["current_price"]["usd"],
            "variacao":   dados["market_data"]["price_change_percentage_24h"],
            "market_cap": dados["market_data"]["market_cap"]["usd"],
            "volume":     dados["market_data"]["total_volume"]["usd"],
        }

    print(f"[ERRO] buscar_cripto({cripto_id}) → status {response.status_code}")
    return None


@st.cache_data(ttl=60)  
def buscar_historico(cripto_id: str, days: int = 1) -> list | None:
    """
    Busca o histórico de preços de uma cripto.
    Ex: buscar_historico("bitcoin", days=1) -> [(datetime, preco), ...]
    Retorna None se falhar.
    """
    url = f"{COINGECKO_BASE}/coins/{cripto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
    }

    
    time.sleep(1.5)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        dados = response.json()

        historico = [
            (pd.to_datetime(ponto[0], unit="ms"), ponto[1])
            for ponto in dados["prices"]
        ]
        return historico

    print(f"[ERRO] buscar_historico({cripto_id}) → status {response.status_code}")
    return None


@st.cache_data(ttl=300)  
def buscar_noticias() -> list | None:
    """
    Busca as últimas notícias do mercado cripto via CryptoPanic.
    Retorna uma lista de dicionários com título, url e data.
    """
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": CRYPTOPANIC_KEY,
        "public":     "true",
        "kind":       "news",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        dados = response.json()

        noticias = [
            {
                "titulo": item["title"],
                "url":    item["url"],
                "fonte":  item["source"]["title"],
                "data":   item["published_at"][:10],  # pega só a data (YYYY-MM-DD)
            }
            for item in dados["results"]
        ]
        return noticias

    print(f"[ERRO] buscar_noticias → status {response.status_code}")
    return None