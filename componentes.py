import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from api import buscar_historico

# ── Paleta dark ───────────────────────────────────────────────
BG_CARD    = "#13131f"
BG_CHART   = "#0d0d18"
BORDER     = "#1e1e2e"
ACCENT     = "#f7931a"
TEXT_MUTED = "#6b6b8a"
TEXT_MAIN  = "#e8e8f0"
GREEN      = "#00d4aa"
RED        = "#ff4d6d"


def _cor_variacao(variacao: float) -> str:
    return GREEN if variacao >= 0 else RED


def painel_esquerdo(dados: dict):
    variacao = dados.get("variacao", 0)
    cor = _cor_variacao(variacao)
    sinal = "▲" if variacao >= 0 else "▼"

    st.markdown(f"""
    <div style="
        margin-top: 24px;
        padding: 20px;
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-left: 3px solid {ACCENT};
        border-radius: 12px;
    ">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="
                background: linear-gradient(135deg, {ACCENT}, #e8820a);
                color: #0a0a0f;
                font-weight: 800;
                font-size: 1rem;
                width: 42px; height: 42px;
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-family: 'Space Mono', monospace;
            ">{dados['simbolo'][:2]}</div>
            <div>
                <div style="font-size:1.2rem; font-weight:800; color:{TEXT_MAIN};">{dados['nome']}</div>
                <div style="font-size:0.75rem; color:{TEXT_MUTED}; font-family:'Space Mono',monospace;">{dados['simbolo']}</div>
            </div>
        </div>
        <div style="
            display: flex; align-items: center; gap: 10px;
            padding: 10px 0;
            border-top: 1px solid {BORDER};
        ">
            <div style="font-size:1.6rem; font-weight:800; font-family:'Space Mono',monospace; color:{TEXT_MAIN};">
                ${dados['preco']:,.2f}
            </div>
            <div style="font-size:0.85rem; font-weight:700; color:{cor}; font-family:'Space Mono',monospace;">
                {sinal} {abs(variacao):.2f}%
            </div>
        </div>
        <div style="font-size:0.7rem; color:{TEXT_MUTED}; margin-top:4px; font-family:'Space Mono',monospace;">
            Atualizado ao vivo · CoinGecko
        </div>
    </div>
    """, unsafe_allow_html=True)


def painel_metricas(dados: dict):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Preço Atual",  value=f"${dados['preco']:,.2f}")
    col2.metric(label="Variação 24h", value=f"{dados['variacao']:.2f}%", delta=f"{dados['variacao']:.2f}%")
    col3.metric(label="Market Cap",   value=f"${dados['market_cap']:,.0f}")
    col4.metric(label="Volume 24h",   value=f"${dados['volume']:,.0f}")


def _fig_linha(cripto_id: str, historico: list, height: int = 300) -> go.Figure:
    df = pd.DataFrame(historico, columns=["data", "preco"])

    subida = df["preco"].iloc[-1] >= df["preco"].iloc[0]
    cor_linha = GREEN if subida else RED

    # RGB para o gradiente SVG inline do Plotly
    rgb = "0,212,170" if subida else "255,77,109"

    preco_max = df["preco"].max()
    preco_min = df["preco"].min()
    idx_max   = df["preco"].idxmax()
    idx_min   = df["preco"].idxmin()

    fig = go.Figure()

    # ── Área preenchida com gradiente via SVG fill ────────────
    # Plotly não suporta gradiente nativo em fill, então usamos
    # duas camadas: fill sólido transparente + linha grossa
    fig.add_trace(go.Scatter(
        x=df["data"],
        y=df["preco"],
        mode="lines",
        line=dict(color=cor_linha, width=2.5, shape="spline", smoothing=0.6),
        fill="tozeroy",
        fillcolor=f"rgba({rgb}, 0.12)",
        name=cripto_id.upper(),
        hovertemplate=(
            "<b>%{x|%d/%m %H:%M}</b><br>"
            "Preço: <b>$%{y:,.2f}</b><extra></extra>"
        ),
    ))

    # Camada extra de gradiente mais intenso no topo da área
    y_topo = df["preco"].copy()
    y_topo_upper = y_topo * 1.0
    fig.add_trace(go.Scatter(
        x=pd.concat([df["data"], df["data"][::-1]]),
        y=pd.concat([y_topo_upper, pd.Series([df["preco"].min()] * len(df))]),
        fill="toself",
        fillcolor=f"rgba({rgb}, 0.04)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False,
    ))

    # ── Anotação de máximo ────────────────────────────────────
    fig.add_annotation(
        x=df["data"].iloc[idx_max],
        y=preco_max,
        text=f"▲ ${preco_max:,.0f}",
        showarrow=True,
        arrowhead=0,
        arrowcolor=cor_linha,
        arrowwidth=1,
        ax=0, ay=-28,
        font=dict(size=10, color=cor_linha, family="Space Mono"),
        bgcolor="rgba(13,13,24,0.85)",
        bordercolor=cor_linha,
        borderwidth=1,
        borderpad=4,
    )

    # ── Anotação de mínimo ────────────────────────────────────
    fig.add_annotation(
        x=df["data"].iloc[idx_min],
        y=preco_min,
        text=f"▼ ${preco_min:,.0f}",
        showarrow=True,
        arrowhead=0,
        arrowcolor=TEXT_MUTED,
        arrowwidth=1,
        ax=0, ay=28,
        font=dict(size=10, color=TEXT_MUTED, family="Space Mono"),
        bgcolor="rgba(13,13,24,0.85)",
        bordercolor=BORDER,
        borderwidth=1,
        borderpad=4,
    )

    fig.update_layout(
        title=dict(
            text=f"<b>{cripto_id.upper()}</b>",
            font=dict(family="Syne, sans-serif", size=14, color=TEXT_MAIN),
            x=0,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG_CHART,
        height=height,
        margin=dict(l=10, r=10, t=44, b=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#151525",
            gridwidth=1,
            linecolor=BORDER,
            tickfont=dict(size=9, color=TEXT_MUTED, family="Space Mono"),
            tickformat="%H:%M\n%d/%m",
            showspikes=True,
            spikecolor=BORDER,
            spikethickness=1,
            spikedash="dot",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#151525",
            gridwidth=1,
            linecolor=BORDER,
            tickfont=dict(size=9, color=TEXT_MUTED, family="Space Mono"),
            tickprefix="$",
            tickformat=",.0f",
            showspikes=True,
            spikecolor=BORDER,
            spikethickness=1,
            spikedash="dot",
            side="right",
        ),
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1a1a2e",
            bordercolor=cor_linha,
            font=dict(family="Space Mono", size=11, color=TEXT_MAIN),
        ),
    )

    return fig


def grafico_preco(cripto_id: str, historico: list, height: int = 300):
    fig = _fig_linha(cripto_id, historico, height)
    st.plotly_chart(fig, use_container_width=True, key=f"grafico_{cripto_id}")


def graficos_mercado():
    CRIPTOS = ["bitcoin", "ethereum", "solana", "cardano"]
    col1, col2, col3, col4 = st.columns(4, gap="small")
    colunas = [col1, col2, col3, col4]

    for i, cripto in enumerate(CRIPTOS):
        historico = buscar_historico(cripto)
        if historico:
            with colunas[i]:
                fig = _fig_linha(cripto, historico, height=320)
                st.plotly_chart(fig, use_container_width=True, key=f"mercado_{cripto}")


def painel_noticias(noticias: list):
    st.markdown("<h2 style='margin-bottom:1.2rem;'>📰 Últimas Notícias</h2>", unsafe_allow_html=True)

    if not noticias:
        st.info("Nenhuma notícia disponível no momento.")
        return

    primeira = noticias[0]
    st.markdown(f"""
    <a href="{primeira['url']}" target="_blank" style="text-decoration:none;">
        <div style="
            padding: 28px 32px;
            background: linear-gradient(135deg, #1a1a2e 0%, #13131f 100%);
            border: 1px solid {BORDER};
            border-top: 3px solid {ACCENT};
            border-radius: 16px;
            margin-bottom: 24px;
            cursor: pointer;
        ">
            <div style="
                display: inline-block;
                background: rgba(247,147,26,0.15);
                color: {ACCENT};
                font-size: 0.65rem;
                font-weight: 700;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                padding: 4px 10px;
                border-radius: 4px;
                margin-bottom: 14px;
                font-family: 'Space Mono', monospace;
            ">⭐ Destaque · {primeira['fonte']}</div>
            <div style="
                font-size: 1.25rem;
                font-weight: 700;
                color: {TEXT_MAIN};
                line-height: 1.5;
                margin-bottom: 12px;
            ">{primeira['titulo']}</div>
            <div style="
                font-size: 0.72rem;
                color: {TEXT_MUTED};
                font-family: 'Space Mono', monospace;
            ">📅 {primeira['data']} · Clique para ler</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

    restantes = noticias[1:]
    if not restantes:
        return

    COLS = 3
    for linha in range(0, len(restantes), COLS):
        grupo = restantes[linha:linha + COLS]
        cols = st.columns(COLS, gap="small")

        for j, noticia in enumerate(grupo):
            with cols[j]:
                st.markdown(f"""
                <a href="{noticia['url']}" target="_blank" style="text-decoration:none;">
                    <div style="
                        padding: 18px 20px;
                        background: {BG_CARD};
                        border: 1px solid {BORDER};
                        border-radius: 12px;
                        margin-bottom: 12px;
                        height: 140px;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        overflow: hidden;
                    ">
                        <div style="
                            font-size: 0.88rem;
                            font-weight: 600;
                            color: {TEXT_MAIN};
                            line-height: 1.45;
                            display: -webkit-box;
                            -webkit-line-clamp: 3;
                            -webkit-box-orient: vertical;
                            overflow: hidden;
                        ">{noticia['titulo']}</div>
                        <div style="
                            font-size: 0.68rem;
                            color: {TEXT_MUTED};
                            font-family: 'Space Mono', monospace;
                            margin-top: 8px;
                        ">{noticia['fonte']} · {noticia['data']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)