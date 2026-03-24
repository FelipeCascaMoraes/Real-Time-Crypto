# 🚀 Real-Time Crypto

Dashboard de criptomoedas em tempo real com visualização de dados de mercado, gráficos interativos e notícias atualizadas.

---

## 📊 Sobre o Projeto

O **Real-Time Crypto** é uma aplicação desenvolvida em Python utilizando Streamlit para visualização de dados do mercado de criptomoedas em tempo real.

O sistema consome dados de APIs externas para fornecer:

- Preços atualizados  
- Métricas de mercado  
- Histórico de preços  
- Notícias recentes do setor  

---

## ⚙️ Funcionalidades

- 🔍 Busca de criptomoedas por nome (ex: bitcoin, ethereum, solana)

- 📈 Gráfico interativo com múltiplos períodos:
  - 1D (1 dia)
  - 1S (7 dias)
  - 1M (30 dias)
  - 6M (180 dias)
  - 1A (365 dias)

- 📊 Métricas em tempo real:
  - Preço atual
  - Variação 24h
  - Market Cap
  - Volume

- 🌐 Visualização simultânea de múltiplas criptomoedas  
- 📰 Feed de notícias atualizado automaticamente  
- 🎨 Interface customizada (tema dark + Plotly)  

---

## 🔌 APIs Utilizadas

### 🟡 CoinGecko API
Responsável pelos dados de mercado:
- Preço atual  
- Market cap  
- Volume  
- Variação percentual  
- Histórico de preços  

---

### 🟣 CryptoPanic API
Responsável pelas notícias:
- Títulos  
- Links  
- Fonte  
- Data de publicação  

---

## 🧠 Estrutura do Projeto
📁 CRIPTO/
├── 📄 analise.py # Interface principal
├── 📄 api.py # Consumo de APIs
├── 📄 componentes.py # UI e gráficos
├── 📄 requirements.txt
└── 🔐 .env


---

## 📌 Possíveis Melhorias

- Sistema de alertas de preço  
- Indicadores técnicos (RSI, médias móveis)  
- Autenticação de usuários  
- Backend dedicado para melhor performance  
- Cache avançado para reduzir chamadas de API  

---

## 👨‍💻 Autor

Felipe Cascaioli de Moraes  

---

## ⭐ Objetivo

Projeto desenvolvido com foco em aprendizado e portfólio, demonstrando:

- Consumo de APIs  
- Visualização de dados  
- Desenvolvimento de interfaces com Streamlit  
- Organização de código em módulos  
