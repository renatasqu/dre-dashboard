"""
DRE Dashboard — Posto de Combustível
Dashboard interativo de Demonstrativo de Resultados para posto de combustível.
Compatível com Streamlit (streamlit run app.py) e visualização direta no VSCode
via extensão Streamlit ou executando localmente.

Autor: Portfólio Pessoal
Versão: 1.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DRE — Posto Combustível",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DADOS MOCKUP — substitua pela integração real
# ─────────────────────────────────────────────
PERIODO = "Março / 2026"

# Receita bruta por combustível (R$)
combustiveis = {
    "Etanol Hidratado": 118_174.68,
    "Gasolina Aditivada": 61_058.54,
    "Gasolina Comum": 828_098.63,
    "Diesel S10": 191_903.02,
    "Diesel S500": 104_380.40,
}

# CMV por combustível (R$)
cmv_combustiveis = {
    "Etanol Hidratado": 112_320.00,
    "Gasolina Aditivada": 58_000.00,
    "Gasolina Comum": 742_770.00,
    "Diesel S10": 166_500.00,
    "Diesel S500": 79_430.00,
}

# Vendas à vista — litros e valores
vendas_vista = pd.DataFrame({
    "Combustível":  ["Etanol", "Gas. Comum", "Gas. Aditivada", "Diesel S10", "Diesel S500"],
    "Litros (R$)":  [24_410.23, 135_402.34, 7_527.41, 25_086.33, 11_643.90],
    "Valor (R$)":   [121_586.85, 850_590.84, 51_002.31, 183_203.51, 76_891.07],
    "Lucro (R$)":   [17_295.69, 104_596.89, 8_534.19, 31_343.87, 10_451.55],
})

# Receita de produtos
produtos = {"Aditivos": 2_595.15, "Lubrificantes": 40_987.33, "Filtros": 6_246.72}
cmv_produtos = {"Aditivos": 1_430.24, "Lubrificantes": 17_217.82, "Filtros": 2_446.52}

# Serviços
servicos = {"Lava Jato": 5_496.30, "Troca de Óleo": 36_821.33}

# Despesas
folha = 43_700.00
despesas_op = 30_905.88
taxas_cartao = 14_511.88

# KPIs derivados
receita_bruta = sum(combustiveis.values())
cmv_total = sum(cmv_combustiveis.values())
lucro_comb_vista = vendas_vista["Lucro (R$)"].sum()          # 172 222,19
lucro_prod_vista = 20_068.82
margem_bruta = lucro_comb_vista + lucro_prod_vista + sum(servicos.values())  # 234 608,64
vendas_prazo_lucro = 23_708.60
resultado_final = 169_199.48

# Operadoras de cartão
cartoes = pd.DataFrame({
    "Operadora":    ["Rede", "Cielo", "Alelo", "Ticketlog", "Pluxee/Sodexo"],
    "Bruto (R$)":  [725_228.02, 56_936.24, 46_532.47, 66_024.83, 1_901.69],
    "Taxas (R$)":  [10_673.43, 11.16, 1_328.69, 2_498.60, 0.00],
    "Real (R$)":   [655_123.15, 56_925.08, 45_203.78, 63_526.23, 1_901.69],
})

# ─────────────────────────────────────────────
# ESTILOS CUSTOMIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background: #0d1117; }

    .kpi-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #8b949e;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #e6edf3;
        line-height: 1;
    }
    .kpi-delta-pos { font-size: 12px; color: #3fb950; margin-top: 4px; }
    .kpi-delta-neg { font-size: 12px; color: #f85149; margin-top: 4px; }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: .1em;
        text-transform: uppercase;
        color: #58a6ff;
        border-bottom: 1px solid #21262d;
        padding-bottom: 8px;
        margin: 32px 0 16px;
    }
    [data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #21262d; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛽ DRE Dashboard")
    st.markdown(f"**Período:** {PERIODO}")
    st.divider()
    st.markdown("**Navegação**")
    secao = st.radio(
        label="",
        options=["Visão Geral", "Combustíveis", "Produtos & Serviços", "Despesas", "Cartões"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Dashboard de portfólio — dados fictícios para fins demonstrativos.")

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="padding: 16px 0 8px">
    <span style="font-family:'Space Grotesk',sans-serif; font-size:28px; font-weight:700; color:#e6edf3;">
        Demonstrativo de Resultados
    </span>
    <span style="font-size:14px; color:#8b949e; margin-left:12px;">{PERIODO}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ── VISÃO GERAL ──────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
if secao == "Visão Geral":

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "Receita Bruta", receita_bruta, None),
        (c2, "CMV Combustíveis", cmv_total, None),
        (c3, "Margem Bruta", margem_bruta, f"{margem_bruta/receita_bruta*100:.1f}% da receita"),
        (c4, "Resultado Final", resultado_final, None),
        (c5, "Margem Líquida", resultado_final / receita_bruta * 100, None),
    ]
    for col, label, value, delta in kpis:
        with col:
            fmt = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") \
                if label != "Margem Líquida" else f"{value:.2f}%"
            delta_html = f'<div class="kpi-delta-pos">{delta}</div>' if delta else ""
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{fmt}</div>
                {delta_html}
            </div>""", unsafe_allow_html=True)

    # Waterfall — resultado final
    st.markdown('<div class="section-title">Composição do Resultado</div>', unsafe_allow_html=True)

    wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
        x=["Margem Bruta", "Vendas a Prazo", "Folha", "Desp. Operacionais", "Taxas Cartão", "Outros", "Resultado Final"],
        y=[margem_bruta, vendas_prazo_lucro, -folha, -despesas_op, -taxas_cartao, 0, resultado_final],
        connector={"line": {"color": "#30363d"}},
        increasing={"marker": {"color": "#3fb950"}},
        decreasing={"marker": {"color": "#f85149"}},
        totals={"marker": {"color": "#58a6ff"}},
        text=[f"R$ {v:,.0f}".replace(",","X").replace(".",",").replace("X",".")
              for v in [margem_bruta, vendas_prazo_lucro, -folha, -despesas_op, -taxas_cartao, 0, resultado_final]],
        textposition="outside",
    ))
    wf.update_layout(
        plot_bgcolor="#161b22", paper_bgcolor="#0d1117",
        font=dict(color="#8b949e", size=11),
        yaxis=dict(gridcolor="#21262d", tickprefix="R$ "),
        xaxis=dict(gridcolor="#21262d"),
        margin=dict(t=20, b=20),
        height=380,
        showlegend=False,
    )
    st.plotly_chart(wf, use_container_width=True)

    # Receita vs CMV por combustível
    st.markdown('<div class="section-title">Receita vs CMV por Combustível</div>', unsafe_allow_html=True)
    labels = list(combustiveis.keys())
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(name="Receita Bruta", x=labels, y=list(combustiveis.values()),
                              marker_color="#58a6ff"))
    fig_bar.add_trace(go.Bar(name="CMV", x=labels, y=list(cmv_combustiveis.values()),
                              marker_color="#f85149"))
    fig_bar.update_layout(
        barmode="group", plot_bgcolor="#161b22", paper_bgcolor="#0d1117",
        font=dict(color="#8b949e"), legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", tickprefix="R$ "),
        xaxis=dict(gridcolor="#21262d"),
        margin=dict(t=10, b=10), height=340,
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# ── COMBUSTÍVEIS ─────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
elif secao == "Combustíveis":

    st.markdown('<div class="section-title">Receita Bruta por Combustível</div>', unsafe_allow_html=True)

    col_pie, col_tab = st.columns([1, 1.4])

    with col_pie:
        pie = px.pie(
            values=list(combustiveis.values()),
            names=list(combustiveis.keys()),
            color_discrete_sequence=["#58a6ff", "#3fb950", "#f0883e", "#bc8cff", "#ff7b72"],
            hole=0.55,
        )
        pie.update_layout(
            plot_bgcolor="#161b22", paper_bgcolor="#161b22",
            font=dict(color="#e6edf3", size=12),
            legend=dict(bgcolor="#161b22"),
            margin=dict(t=10, b=10, l=10, r=10),
            height=320,
        )
        pie.update_traces(textinfo="percent+label")
        st.plotly_chart(pie, use_container_width=True)

    with col_tab:
        df_comb = pd.DataFrame({
            "Combustível": list(combustiveis.keys()),
            "Receita (R$)": [f"{v:,.2f}" for v in combustiveis.values()],
            "CMV (R$)":     [f"{v:,.2f}" for v in cmv_combustiveis.values()],
            "Lucro (R$)":   [f"{r-c:,.2f}" for r, c in zip(combustiveis.values(), cmv_combustiveis.values())],
            "Margem %":     [f"{(r-c)/r*100:.1f}%" for r, c in zip(combustiveis.values(), cmv_combustiveis.values())],
        })
        st.dataframe(df_comb, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Vendas à Vista — Detalhamento</div>', unsafe_allow_html=True)
    st.dataframe(
        vendas_vista.style.format({
            "Litros (R$)": "R$ {:,.2f}", "Valor (R$)": "R$ {:,.2f}", "Lucro (R$)": "R$ {:,.2f}"
        }),
        use_container_width=True, hide_index=True,
    )

    lucro_total_comb = vendas_vista["Lucro (R$)"].sum()
    st.metric("Lucro Líquido Combustíveis (à vista)", f"R$ {lucro_total_comb:,.2f}")


# ─────────────────────────────────────────────────────────────
# ── PRODUTOS & SERVIÇOS ───────────────────────────────────────
# ─────────────────────────────────────────────────────────────
elif secao == "Produtos & Serviços":

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Receita de Produtos</div>', unsafe_allow_html=True)
        df_prod = pd.DataFrame({
            "Produto":   list(produtos.keys()),
            "Receita":   [f"R$ {v:,.2f}" for v in produtos.values()],
            "CMV":       [f"R$ {v:,.2f}" for v in cmv_produtos.values()],
            "Lucro":     [f"R$ {r-c:,.2f}" for r, c in zip(produtos.values(), cmv_produtos.values())],
        })
        st.dataframe(df_prod, use_container_width=True, hide_index=True)

    with c2:
        st.markdown('<div class="section-title">Serviços</div>', unsafe_allow_html=True)
        for nome, valor in servicos.items():
            st.metric(nome, f"R$ {valor:,.2f}")

    st.markdown('<div class="section-title">Composição da Receita Total</div>', unsafe_allow_html=True)
    categorias = {
        "Combustíveis à Vista": lucro_comb_vista,
        "Produtos à Vista": lucro_prod_vista,
        "Lava Jato": servicos["Lava Jato"],
        "Troca de Óleo": servicos["Troca de Óleo"],
    }
    fig_cat = px.bar(
        x=list(categorias.keys()), y=list(categorias.values()),
        color=list(categorias.keys()),
        color_discrete_sequence=["#58a6ff", "#3fb950", "#f0883e", "#bc8cff"],
        labels={"x": "", "y": "R$"},
    )
    fig_cat.update_layout(
        plot_bgcolor="#161b22", paper_bgcolor="#0d1117",
        font=dict(color="#8b949e"), showlegend=False,
        yaxis=dict(gridcolor="#21262d", tickprefix="R$ "),
        margin=dict(t=10, b=10), height=320,
    )
    st.plotly_chart(fig_cat, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# ── DESPESAS ─────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
elif secao == "Despesas":

    st.markdown('<div class="section-title">Estrutura de Despesas</div>', unsafe_allow_html=True)

    # Composição despesas
    desp = {
        "Folha de Pagamento": folha,
        "Despesas Operacionais": despesas_op,
        "Taxas de Cartão": taxas_cartao,
    }
    fig_d = go.Figure(go.Pie(
        labels=list(desp.keys()), values=list(desp.values()),
        hole=0.6,
        marker=dict(colors=["#f85149", "#f0883e", "#ffa657"]),
        textinfo="percent+label",
    ))
    fig_d.update_layout(
        plot_bgcolor="#161b22", paper_bgcolor="#161b22",
        font=dict(color="#e6edf3"), legend=dict(bgcolor="#161b22"),
        margin=dict(t=10, b=10), height=320,
    )
    st.plotly_chart(fig_d, use_container_width=True)

    st.markdown('<div class="section-title">Folha de Pagamento — Setores</div>', unsafe_allow_html=True)
    folha_setores = {
        "Frentistas": 21_000.00, "Administração": 8_500.00,
        "Lava Jato": 4_600.00, "Troca de Óleo": 2_500.00,
        "Segurança": 2_700.00, "Gerência": 3_500.00, "Extras": 900.00,
    }
    df_folha = pd.DataFrame({
        "Setor": list(folha_setores.keys()),
        "Valor (R$)": [f"R$ {v:,.2f}" for v in folha_setores.values()],
        "% do Total": [f"{v/folha*100:.1f}%" for v in folha_setores.values()],
    })
    st.dataframe(df_folha, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Análise Vertical — % sobre Receita Bruta</div>', unsafe_allow_html=True)
    av = {
        "Receita Bruta":     (receita_bruta, 100.0),
        "(-) CMV":           (cmv_total, cmv_total / receita_bruta * 100),
        "= Margem Bruta":    (margem_bruta, margem_bruta / receita_bruta * 100),
        "(-) Folha":         (folha, folha / receita_bruta * 100),
        "(-) Desp. Op.":     (despesas_op, despesas_op / receita_bruta * 100),
        "(-) Taxas Cartão":  (taxas_cartao, taxas_cartao / receita_bruta * 100),
        "= Resultado Final": (resultado_final, resultado_final / receita_bruta * 100),
    }
    df_av = pd.DataFrame({
        "Item": list(av.keys()),
        "Valor (R$)": [f"R$ {v[0]:,.2f}" for v in av.values()],
        "% Receita":  [f"{v[1]:.2f}%" for v in av.values()],
    })
    st.dataframe(df_av, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────
# ── CARTÕES ──────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
elif secao == "Cartões":

    st.markdown('<div class="section-title">Receita por Operadora de Cartão</div>', unsafe_allow_html=True)

    total_bruto = cartoes["Bruto (R$)"].sum()
    total_taxas = cartoes["Taxas (R$)"].sum()
    total_real  = cartoes["Real (R$)"].sum()

    cc1, cc2, cc3 = st.columns(3)
    for col, label, val in [(cc1, "Total Bruto", total_bruto), (cc2, "Total Taxas", total_taxas), (cc3, "Recebimento Real", total_real)]:
        with col:
            cor = "#f85149" if label == "Total Taxas" else "#3fb950" if label == "Recebimento Real" else "#58a6ff"
            fmt = f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{cor}">{fmt}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Detalhamento por Operadora</div>', unsafe_allow_html=True)
    df_cart = cartoes.copy()
    df_cart["Taxa %"] = (df_cart["Taxas (R$)"] / df_cart["Bruto (R$)"] * 100).round(2).fillna(0)
    st.dataframe(
        df_cart.style.format({
            "Bruto (R$)": "R$ {:,.2f}", "Taxas (R$)": "R$ {:,.2f}",
            "Real (R$)": "R$ {:,.2f}", "Taxa %": "{:.2f}%",
        }),
        use_container_width=True, hide_index=True,
    )

    fig_op = px.bar(
        cartoes, x="Operadora", y=["Bruto (R$)", "Taxas (R$)", "Real (R$)"],
        barmode="group",
        color_discrete_sequence=["#58a6ff", "#f85149", "#3fb950"],
        labels={"value": "R$", "variable": ""},
    )
    fig_op.update_layout(
        plot_bgcolor="#161b22", paper_bgcolor="#0d1117",
        font=dict(color="#8b949e"), legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", tickprefix="R$ "),
        margin=dict(t=10, b=10), height=360,
    )
    st.plotly_chart(fig_op, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr style="border-color:#21262d; margin-top:48px"/>
<div style="text-align:center; color:#484f58; font-size:11px; padding-bottom:16px">
    Dashboard de portfólio — Dados fictícios para fins demonstrativos · Construído com Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
