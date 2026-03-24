import time
import streamlit as st
from api import buscar_cripto, buscar_historico, buscar_noticias
from componentes import painel_esquerdo, painel_metricas, grafico_preco, graficos_mercado, painel_noticias

# ── Configuração da página ─────────────────────────────────────
st.set_page_config(
    page_title="Real Time Crypto",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS Global ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a0a0f !important;
    color: #e8e8f0 !important;
}

[data-testid="stHeader"] {
    background-color: #0a0a0f !important;
}

html, body, * {
    font-family: 'Syne', sans-serif !important;
}

h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.4rem !important;
    letter-spacing: -1px !important;
    color: #ffffff !important;
    margin-bottom: 0.2rem !important;
}

h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

[data-testid="stTextInput"] input {
    background-color: #13131f !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 10px 14px !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #f7931a !important;
    box-shadow: 0 0 0 2px rgba(247, 147, 26, 0.2) !important;
}

[data-testid="stButton"] button {
    background: linear-gradient(135deg, #f7931a, #e8820a) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #ffaa40, #f7931a) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(247, 147, 26, 0.35) !important;
}

/* Radio estilizado como botões de período */
[data-testid="stRadio"] {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 4px 6px;
}
[data-testid="stRadio"] > div {
    gap: 2px !important;
}
[data-testid="stRadio"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #6b6b8a !important;
    padding: 6px 18px !important;
    border-radius: 7px !important;
    cursor: pointer !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #f7931a, #e8820a) !important;
    color: #0a0a0f !important;
}
[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}

[data-testid="stMetric"] {
    background-color: #13131f !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    color: #6b6b8a !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-family: 'Space Mono', monospace !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
}

hr {
    border-color: #1e1e2e !important;
    margin: 1.5rem 0 !important;
}

.js-plotly-plot .plotly {
    background: transparent !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #f7931a; }
</style>
""", unsafe_allow_html=True)

# ── session_state ─────────────────────────────────────────────
if "dados_cripto" not in st.session_state:
    st.session_state.dados_cripto = None

if "periodo" not in st.session_state:
    st.session_state.periodo = "1D"

# ══════════════════════════════════════════════════════════════
# SEÇÃO 1 — Busca (esquerda) + Métricas e Gráfico (direita)
# ══════════════════════════════════════════════════════════════
col_busca, col_info = st.columns([1, 2], gap="large")

with col_busca:
    st.title("₿ Real Time Crypto")
    st.markdown(
        "<p style='color:#6b6b8a; font-size:0.8rem; margin-top:-12px; margin-bottom:20px;"
        "font-family:Space Mono,monospace;'>Dados ao vivo do mercado cripto</p>",
        unsafe_allow_html=True,
    )

    cripto_id = st.text_input("", placeholder="Ex: bitcoin, ethereum, solana...")

    if st.button("🔍 Buscar"):
        if cripto_id.strip() == "":
            st.warning("Digite o nome de uma criptomoeda.")
        else:
            dados = buscar_cripto(cripto_id.strip())
            if dados:
                st.session_state.dados_cripto = dados
            else:
                st.session_state.dados_cripto = None
                st.error("Cripto não encontrada. Tente novamente.")

    if st.session_state.dados_cripto:
        painel_esquerdo(st.session_state.dados_cripto)

with col_info:
    if st.session_state.dados_cripto:
        painel_metricas(st.session_state.dados_cripto)

        # ── Seletor de período ────────────────────────────────
        periodo_map = {"1D": 1, "1S": 7, "1M": 30, "6M": 180, "1A": 365}
        opcoes = list(periodo_map.keys())

        periodo_selecionado = st.radio(
            label="Período",
            options=opcoes,
            index=opcoes.index(st.session_state.periodo),
            horizontal=True,
            key="radio_periodo",
            label_visibility="collapsed",
        )

        if periodo_selecionado != st.session_state.periodo:
            st.session_state.periodo = periodo_selecionado

        days = periodo_map[st.session_state.periodo]
        historico = buscar_historico(
            st.session_state.dados_cripto["nome"].lower(), days=days
        )
        if historico:
            grafico_preco(st.session_state.dados_cripto["nome"], historico, height=380)
    else:
        st.markdown("""
        <div style='
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px dashed #2a2a3d;
            border-radius: 16px;
            color: #3a3a5a;
            font-family: Space Mono, monospace;
            font-size: 0.85rem;
            text-align: center;
        '>
            ← Pesquise uma criptomoeda<br>para ver os dados
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SEÇÃO 2 — Mercado em Tempo Real (4 gráficos grandes)
# ══════════════════════════════════════════════════════════════
st.divider()
st.markdown(
    "<h2 style='margin-bottom:1rem;'>📈 Mercado em Tempo Real</h2>",
    unsafe_allow_html=True,
)

graficos_mercado()

# ══════════════════════════════════════════════════════════════
# SEÇÃO 3 — Notícias
# ══════════════════════════════════════════════════════════════
st.divider()
noticias = buscar_noticias()
painel_noticias(noticias)

# ── Atualização automática a cada 60 segundos ─────────────────
time.sleep(60)
st.rerun()