import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from helpers import BRT, VERDE_TICKERS, VERMELHA_TICKERS, ativos, fetch_mxn_brl

def render_backtest(start_dt, end_dt):
    st.markdown("### Backtest de Correlação")

    verde = ativos(VERDE_TICKERS, start_dt, end_dt, modo='alta')
    vermelha = ativos(VERMELHA_TICKERS, start_dt, end_dt, modo='baixa')
    mxn_bruto, brl_bruto, mxn_ref, brl_ref = fetch_mxn_brl(start_dt, end_dt)

    if verde.empty or vermelha.empty:
        st.warning("Sem dados suficientes para o backtest.")
        return

    common_idx = verde.index.intersection(vermelha.index)
    if common_idx.empty:
        st.warning("Sem interseção entre as séries para o backtest.")
        return

    verde = verde.loc[common_idx]
    vermelha = vermelha.loc[common_idx]

    spread = verde - vermelha

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=common_idx,
        y=spread,
        mode='lines',
        name='Spread',
        line=dict(color='#38BDF8', width=2)
    ))

    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )

    st.plotly_chart(fig, use_container_width=True)
