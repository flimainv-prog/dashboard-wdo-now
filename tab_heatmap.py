import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from helpers import BRT, VERDE_TICKERS, VERMELHA_TICKERS, ativos

def render_heatmap(start_dt, end_dt):
    st.markdown("### Mapa de Calor Abertura")

    verde = ativos(VERDE_TICKERS, start_dt, end_dt, modo='alta')
    vermelha = ativos(VERMELHA_TICKERS, start_dt, end_dt, modo='baixa')

    if verde.empty or vermelha.empty:
        st.warning("Sem dados suficientes para o mapa de calor.")
        return

    common_idx = verde.index.intersection(vermelha.index)
    if common_idx.empty:
        st.warning("Sem dados em comum para o mapa de calor.")
        return

    verde = verde.loc[common_idx]
    vermelha = vermelha.loc[common_idx]

    heat = pd.DataFrame({
        "Verde": verde,
        "Vermelha": vermelha
    })

    fig = go.Figure(data=go.Heatmap(
        z=heat.T.values,
        x=[d.strftime("%H:%M") for d in heat.index],
        y=heat.columns,
        colorscale='Viridis'
    ))

    fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
