"""
DRE Dashboard — Posto de Combustível
Dashboard interativo de Demonstrativo de Resultados para posto de combustível.
Compatível com Streamlit (streamlit run app.py)

Autor: Portfólio Pessoal
Versão: 2.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

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
# DADOS MOCKUP — 12 MESES
# ─────────────────────────────────────────────
MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

random.seed(42)

def variar(base, pct=0.12):
    return [round(base * (1 + random.uniform(-pct, pct)), 2) for _ in range(12)]

receita_bruta_mensal     = variar(1_303_615.27)
cmv_mensal               = [round(r * 0.889, 2) for r in receita_bruta_mensal]
folha_mensal             = variar(43_700.00, 0.05)
despesas_op_mensal       = variar(30_905.88, 0.10)
taxas_cartao_mensal      = [round(r * 0.0111, 2) for r in receita_bruta_mensal]
vendas_prazo_mensal      = variar(23_708.60, 0.15)

margem_bruta_mensal = [
    round((r - c) * 0.18 / 0.1109 + s + lj, 2)
    for r, c, s, lj in zip(
        receita_bruta_mensal, cmv_mensal,
        variar(36_821.33, 0.10), variar(5_496.30, 0.15)
    )
]

resultado_mensal = [
    round(mb + vp - fp - do_ - tc, 2)
    for mb, vp, fp, do_, tc in zip(
        margem_bruta_mensal, vendas_prazo_mensal,
        folha_mensal, despesas_op_mensal, taxas_cartao_mensal
    )
]

# Março fixo (mês real da DRE)
receita_bruta_mensal[2]  = 1_303_615.27
cmv_mensal[2]            = 1_159_020.00
margem_bruta_mensal[2]   = 234_608.64
folha_mensal[2]          = 43_700.00
despesas_op_mensal[2]    = 30_905.88
taxas_cartao_mensal[2]   = 14_511.88
vendas_prazo_mensal[2]   = 23_708.60
resultado_mensal[2]      = 169_199.48

# Variação % do resultado mês a mês
variacao_pct = [None] + [
    round((resultado_mensal[i] - resultado_mensal[i-1]) / abs(resultado_mensal[i-1]) * 100, 2)
    for i in range(1, 12)
]

# Dados março (visão geral)
PERIODO = "Março / 2026"
receita_bruta   = receita_bruta_mensal[2]
cmv_total       = cmv_mensal[2]
margem_bruta    = margem_bruta_mensal[2]
folha           = folha_mensal[2]
despesas_op     = despesas_op_mensal[2]
taxas_cartao    = taxas_cartao_mensal[2]
resultado_final = resultado_mensal[2]
vendas_prazo_lucro = vendas_prazo_mensal[2]

combustiveis = {
    "Etanol Hidratado": 118_174.68, "Gasolina Aditivada": 61_058.54,
    "Gasolina Comum": 828_098.63,  "Diesel S10": 191_903.02, "Diesel S500": 104_380.40,
}
cmv_combustiveis = {
    "Etanol Hidratado": 112_320.00, "Gasolina Aditivada": 58_000.00,
    "Gasolina Comum": 742_770.00,   "Diesel S10": 166_500.00, "Diesel S500": 79_430.00,
}
vendas_vista = pd.DataFrame({
    "Combustível":  ["Etanol","Gas. Comum","Gas. Aditivada","Diesel S10","Diesel S500"],
    "Litros (R$)":  [24_410.23,135_402.34,7_527.41,25_086.33,11_643.90],
    "Valor (R$)":   [121_586.85,850_590.84,51_002.31,183_203.51,76_891.07],
    "Lucro (R$)":   [17_295.69,104_596.89,8_534.19,31_343.87,10_451.55],
})
produtos     = {"Aditivos":2_595.15,"Lubrificantes":40_987.33,"Filtros":6_246.72}
cmv_produtos = {"Aditivos":1_430.24,"Lubrificantes":17_217.82,"Filtros":2_446.52}
servicos     = {"Lava Jato":5_496.30,"Troca de Óleo":36_821.33}
cartoes = pd.DataFrame({
    "Operadora":   ["Rede","Cielo","Alelo","Ticketlog","Pluxee/Sodexo"],
    "Bruto (R$)":  [725_228.02,56_936.24,46_532.47,66_024.83,1_901.69],
    "Taxas (R$)":  [10_673.43,11.16,1_328.69,2_498.60,0.00],
    "Real (R$)":   [655_123.15,56_925.08,45_203.78,63_526.23,1_901.69],
})
lucro_comb_vista = vendas_vista["Lucro (R$)"].sum()
lucro_prod_vista = 20_068.82

# ─────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.kpi-card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px 24px;text-align:center;}
.kpi-label{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8b949e;margin-bottom:6px;}
.kpi-value{font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:700;color:#e6edf3;line-height:1;}
.kpi-delta-pos{font-size:12px;color:#3fb950;margin-top:4px;}
.kpi-delta-neg{font-size:12px;color:#f85149;margin-top:4px;}
.section-title{font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#58a6ff;border-bottom:1px solid #21262d;padding-bottom:8px;margin:32px 0 16px;}
[data-testid="stSidebar"]{background:#0d1117;border-right:1px solid #21262d;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛽ DRE Dashboard")
    st.markdown(f"**Período base:** {PERIODO}")
    st.divider()
    st.markdown("**Navegação**")
    secao = st.radio("", ["Visão Geral","DRE Anual","Variação do Resultado","Combustíveis","Produtos & Serviços","Despesas","Cartões"], label_visibility="collapsed")
    st.divider()
    st.caption("Dashboard de portfólio — dados fictícios para fins demonstrativos.")

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="padding:16px 0 8px">
  <span style="font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700;color:#e6edf3;">
    Demonstrativo de Resultados
  </span>
  <span style="font-size:14px;color:#8b949e;margin-left:12px;">{PERIODO}</span>
</div>
""", unsafe_allow_html=True)

def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ══════════════════════════════════════════════
# VISÃO GERAL
# ══════════════════════════════════════════════
if secao == "Visão Geral":
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        (c1,"Receita Bruta",receita_bruta,None),
        (c2,"CMV Combustíveis",cmv_total,None),
        (c3,"Margem Bruta",margem_bruta,f"{margem_bruta/receita_bruta*100:.1f}% da receita"),
        (c4,"Resultado Final",resultado_final,None),
        (c5,"Margem Líquida",resultado_final/receita_bruta*100,None),
    ]
    for col,label,value,delta in kpis:
        with col:
            fv = f"{value:.2f}%" if label=="Margem Líquida" else fmt_brl(value)
            dh = f'<div class="kpi-delta-pos">{delta}</div>' if delta else ""
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{fv}</div>{dh}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Composição do Resultado</div>', unsafe_allow_html=True)
    wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","relative","relative","relative","total"],
        x=["Margem Bruta","Vendas a Prazo","Folha","Desp. Operacionais","Taxas Cartão","Resultado Final"],
        y=[margem_bruta,vendas_prazo_lucro,-folha,-despesas_op,-taxas_cartao,resultado_final],
        connector={"line":{"color":"#30363d"}},
        increasing={"marker":{"color":"#3fb950"}},
        decreasing={"marker":{"color":"#f85149"}},
        totals={"marker":{"color":"#58a6ff"}},
        text=[fmt_brl(v) for v in [margem_bruta,vendas_prazo_lucro,-folha,-despesas_op,-taxas_cartao,resultado_final]],
        textposition="outside",
    ))
    wf.update_layout(plot_bgcolor="#161b22",paper_bgcolor="#0d1117",font=dict(color="#8b949e",size=11),
        yaxis=dict(gridcolor="#21262d"),xaxis=dict(gridcolor="#21262d"),margin=dict(t=20,b=20),height=380,showlegend=False)
    st.plotly_chart(wf, use_container_width=True)

    st.markdown('<div class="section-title">Receita vs CMV por Combustível</div>', unsafe_allow_html=True)
    labels = list(combustiveis.keys())
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(name="Receita Bruta",x=labels,y=list(combustiveis.values()),marker_color="#58a6ff"))
    fig_bar.add_trace(go.Bar(name="CMV",x=labels,y=list(cmv_combustiveis.values()),marker_color="#f85149"))
    fig_bar.update_layout(barmode="group",plot_bgcolor="#161b22",paper_bgcolor="#0d1117",
        font=dict(color="#8b949e"),legend=dict(bgcolor="#161b22",bordercolor="#30363d"),
        yaxis=dict(gridcolor="#21262d"),margin=dict(t=10,b=10),height=340)
    st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════
# DRE ANUAL — TABELA MÊS A MÊS
# ══════════════════════════════════════════════
elif secao == "DRE Anual":
    st.markdown('<div class="section-title">DRE — Todos os Meses</div>', unsafe_allow_html=True)

    acum_receita  = sum(receita_bruta_mensal)
    acum_cmv      = sum(cmv_mensal)
    acum_margem   = sum(margem_bruta_mensal)
    acum_folha    = sum(folha_mensal)
    acum_desp     = sum(despesas_op_mensal)
    acum_taxas    = sum(taxas_cartao_mensal)
    acum_result   = sum(resultado_mensal)

    linhas = {
        "Receita Bruta":          receita_bruta_mensal,
        "(-) CMV":                cmv_mensal,
        "= Margem Bruta":         margem_bruta_mensal,
        "(-) Folha de Pagamento": folha_mensal,
        "(-) Despesas Operac.":   despesas_op_mensal,
        "(-) Taxas de Cartão":    taxas_cartao_mensal,
        "= Resultado Final":      resultado_mensal,
    }
    acumulados = [acum_receita, acum_cmv, acum_margem, acum_folha, acum_desp, acum_taxas, acum_result]

    rows = []
    for (nome, vals), acum in zip(linhas.items(), acumulados):
        row = {"Item": nome}
        for m, v in zip(MESES, vals):
            row[m] = fmt_brl(v)
        row["Acumulado"] = fmt_brl(acum)
        rows.append(row)

    df_anual = pd.DataFrame(rows)

    # Highlight nas linhas de resultado
    def highlight_rows(row):
        if "Resultado" in row["Item"] or "Margem" in row["Item"]:
            return ["background-color: #1c2a1c; color: #3fb950; font-weight:600"] * len(row)
        elif "(-)" in row["Item"]:
            return ["background-color: #1c1616; color: #f85149"] * len(row)
        else:
            return [""] * len(row)

    st.dataframe(
        df_anual.style.apply(highlight_rows, axis=1),
        use_container_width=True, hide_index=True, height=320
    )

    # Gráfico de barras empilhadas — resultado vs despesas
    st.markdown('<div class="section-title">Resultado vs Despesas — Evolução Mensal</div>', unsafe_allow_html=True)
    fig_ev = go.Figure()
    fig_ev.add_trace(go.Bar(name="Folha",x=MESES,y=folha_mensal,marker_color="#f85149"))
    fig_ev.add_trace(go.Bar(name="Desp. Operacionais",x=MESES,y=despesas_op_mensal,marker_color="#f0883e"))
    fig_ev.add_trace(go.Bar(name="Taxas Cartão",x=MESES,y=taxas_cartao_mensal,marker_color="#ffa657"))
    fig_ev.add_trace(go.Scatter(name="Resultado Final",x=MESES,y=resultado_mensal,
        mode="lines+markers",line=dict(color="#3fb950",width=3),marker=dict(size=8)))
    fig_ev.update_layout(barmode="stack",plot_bgcolor="#161b22",paper_bgcolor="#0d1117",
        font=dict(color="#8b949e"),legend=dict(bgcolor="#161b22",bordercolor="#30363d"),
        yaxis=dict(gridcolor="#21262d",tickprefix="R$ "),
        margin=dict(t=10,b=10),height=400)
    st.plotly_chart(fig_ev, use_container_width=True)

# ══════════════════════════════════════════════
# VARIAÇÃO DO RESULTADO
# ══════════════════════════════════════════════
elif secao == "Variação do Resultado":
    st.markdown('<div class="section-title">Variação Percentual do Resultado — 2026</div>', unsafe_allow_html=True)

    cores_pontos = ["#3fb950" if (v or 0) >= 0 else "#f85149" for v in variacao_pct]
    meses_plot   = MESES[1:]
    var_plot     = variacao_pct[1:]
    cores_plot   = cores_pontos[1:]

    fig_var = go.Figure()
    # Linha zero
    fig_var.add_hline(y=0, line_dash="dot", line_color="#30363d", line_width=1)
    # Área colorida
    fig_var.add_trace(go.Scatter(
        x=meses_plot, y=var_plot,
        mode="lines+markers+text",
        line=dict(color="#58a6ff", width=3),
        marker=dict(size=12, color=cores_plot, line=dict(width=2, color="#0d1117")),
        text=[f"{v:+.2f}%" for v in var_plot],
        textposition="top center",
        textfont=dict(color="#e6edf3", size=11),
        fill="tozeroy",
        fillcolor="rgba(88,166,255,0.08)",
        name="Variação %",
    ))
    fig_var.update_layout(
        plot_bgcolor="#161b22", paper_bgcolor="#0d1117",
        font=dict(color="#8b949e"),
        yaxis=dict(gridcolor="#21262d", ticksuffix="%", zeroline=False),
        xaxis=dict(gridcolor="#21262d"),
        margin=dict(t=20, b=20), height=420,
        showlegend=False,
    )
    st.plotly_chart(fig_var, use_container_width=True)

    # Tabela de apoio
    st.markdown('<div class="section-title">Resultado Mensal</div>', unsafe_allow_html=True)
    df_var = pd.DataFrame({
        "Mês":           MESES,
        "Resultado":     [fmt_brl(v) for v in resultado_mensal],
        "Variação %":    [("—" if v is None else f"{v:+.2f}%") for v in variacao_pct],
    })
    def color_var(val):
        if val == "—": return ""
        if "+" in str(val): return "color: #3fb950; font-weight:600"
        return "color: #f85149; font-weight:600"

    st.dataframe(
        df_var.style.applymap(color_var, subset=["Variação %"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════════
# COMBUSTÍVEIS
# ══════════════════════════════════════════════
elif secao == "Combustíveis":
    st.markdown('<div class="section-title">Receita Bruta por Combustível</div>', unsafe_allow_html=True)
    col_pie, col_tab = st.columns([1,1.4])
    with col_pie:
        pie = px.pie(values=list(combustiveis.values()),names=list(combustiveis.keys()),
            color_discrete_sequence=["#58a6ff","#3fb950","#f0883e","#bc8cff","#ff7b72"],hole=0.55)
        pie.update_layout(plot_bgcolor="#161b22",paper_bgcolor="#161b22",
            font=dict(color="#e6edf3",size=12),legend=dict(bgcolor="#161b22"),
            margin=dict(t=10,b=10,l=10,r=10),height=320)
        pie.update_traces(textinfo="percent+label")
        st.plotly_chart(pie, use_container_width=True)
    with col_tab:
        df_comb = pd.DataFrame({
            "Combustível": list(combustiveis.keys()),
            "Receita":   [fmt_brl(v) for v in combustiveis.values()],
            "CMV":       [fmt_brl(v) for v in cmv_combustiveis.values()],
            "Lucro":     [fmt_brl(r-c) for r,c in zip(combustiveis.values(),cmv_combustiveis.values())],
            "Margem %":  [f"{(r-c)/r*100:.1f}%" for r,c in zip(combustiveis.values(),cmv_combustiveis.values())],
        })
        st.dataframe(df_comb, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Vendas à Vista — Detalhamento</div>', unsafe_allow_html=True)
    st.dataframe(vendas_vista.style.format({"Litros (R$)":"R$ {:,.2f}","Valor (R$)":"R$ {:,.2f}","Lucro (R$)":"R$ {:,.2f}"}),
        use_container_width=True, hide_index=True)
    st.metric("Lucro Líquido Combustíveis (à vista)", fmt_brl(vendas_vista["Lucro (R$)"].sum()))

# ══════════════════════════════════════════════
# PRODUTOS & SERVIÇOS
# ══════════════════════════════════════════════
elif secao == "Produtos & Serviços":
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Receita de Produtos</div>', unsafe_allow_html=True)
        df_prod = pd.DataFrame({
            "Produto": list(produtos.keys()),
            "Receita": [fmt_brl(v) for v in produtos.values()],
            "CMV":     [fmt_brl(v) for v in cmv_produtos.values()],
            "Lucro":   [fmt_brl(r-c) for r,c in zip(produtos.values(),cmv_produtos.values())],
        })
        st.dataframe(df_prod, use_container_width=True, hide_index=True)
    with c2:
        st.markdown('<div class="section-title">Serviços</div>', unsafe_allow_html=True)
        for nome,valor in servicos.items():
            st.metric(nome, fmt_brl(valor))

    st.markdown('<div class="section-title">Composição da Margem Bruta</div>', unsafe_allow_html=True)
    categorias = {"Combustíveis à Vista":lucro_comb_vista,"Produtos à Vista":lucro_prod_vista,
                  "Lava Jato":servicos["Lava Jato"],"Troca de Óleo":servicos["Troca de Óleo"]}
    fig_cat = px.bar(x=list(categorias.keys()),y=list(categorias.values()),
        color=list(categorias.keys()),color_discrete_sequence=["#58a6ff","#3fb950","#f0883e","#bc8cff"],
        labels={"x":"","y":"R$"})
    fig_cat.update_layout(plot_bgcolor="#161b22",paper_bgcolor="#0d1117",font=dict(color="#8b949e"),
        showlegend=False,yaxis=dict(gridcolor="#21262d"),margin=dict(t=10,b=10),height=320)
    st.plotly_chart(fig_cat, use_container_width=True)

# ══════════════════════════════════════════════
# DESPESAS
# ══════════════════════════════════════════════
elif secao == "Despesas":
    st.markdown('<div class="section-title">Estrutura de Despesas</div>', unsafe_allow_html=True)
    desp = {"Folha de Pagamento":folha,"Despesas Operacionais":despesas_op,"Taxas de Cartão":taxas_cartao}
    fig_d = go.Figure(go.Pie(labels=list(desp.keys()),values=list(desp.values()),hole=0.6,
        marker=dict(colors=["#f85149","#f0883e","#ffa657"]),textinfo="percent+label"))
    fig_d.update_layout(plot_bgcolor="#161b22",paper_bgcolor="#161b22",
        font=dict(color="#e6edf3"),legend=dict(bgcolor="#161b22"),margin=dict(t=10,b=10),height=320)
    st.plotly_chart(fig_d, use_container_width=True)

    st.markdown('<div class="section-title">Folha de Pagamento — Setores</div>', unsafe_allow_html=True)
    folha_setores = {"Frentistas":21_000.00,"Administração":8_500.00,"Lava Jato":4_600.00,
                     "Troca de Óleo":2_500.00,"Segurança":2_700.00,"Gerência":3_500.00,"Extras":900.00}
    df_folha = pd.DataFrame({
        "Setor": list(folha_setores.keys()),
        "Valor (R$)": [fmt_brl(v) for v in folha_setores.values()],
        "% do Total": [f"{v/folha*100:.1f}%" for v in folha_setores.values()],
    })
    st.dataframe(df_folha, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Análise Vertical — % sobre Receita Bruta</div>', unsafe_allow_html=True)
    av = {"Receita Bruta":(receita_bruta,100.0),"(-) CMV":(cmv_total,cmv_total/receita_bruta*100),
          "= Margem Bruta":(margem_bruta,margem_bruta/receita_bruta*100),
          "(-) Folha":(folha,folha/receita_bruta*100),"(-) Desp. Op.":(despesas_op,despesas_op/receita_bruta*100),
          "(-) Taxas Cartão":(taxas_cartao,taxas_cartao/receita_bruta*100),
          "= Resultado Final":(resultado_final,resultado_final/receita_bruta*100)}
    df_av = pd.DataFrame({"Item":list(av.keys()),"Valor (R$)":[fmt_brl(v[0]) for v in av.values()],
                           "% Receita":[f"{v[1]:.2f}%" for v in av.values()]})
    st.dataframe(df_av, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════
# CARTÕES
# ══════════════════════════════════════════════
elif secao == "Cartões":
    st.markdown('<div class="section-title">Receita por Operadora de Cartão</div>', unsafe_allow_html=True)
    cc1,cc2,cc3 = st.columns(3)
    for col,label,val,cor in [(cc1,"Total Bruto",cartoes["Bruto (R$)"].sum(),"#58a6ff"),
                               (cc2,"Total Taxas",cartoes["Taxas (R$)"].sum(),"#f85149"),
                               (cc3,"Recebimento Real",cartoes["Real (R$)"].sum(),"#3fb950")]:
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{cor}">{fmt_brl(val)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Detalhamento por Operadora</div>', unsafe_allow_html=True)
    df_cart = cartoes.copy()
    df_cart["Taxa %"] = (df_cart["Taxas (R$)"]/df_cart["Bruto (R$)"]*100).round(2).fillna(0)
    st.dataframe(df_cart.style.format({"Bruto (R$)":"R$ {:,.2f}","Taxas (R$)":"R$ {:,.2f}","Real (R$)":"R$ {:,.2f}","Taxa %":"{:.2f}%"}),
        use_container_width=True, hide_index=True)

    fig_op = px.bar(cartoes,x="Operadora",y=["Bruto (R$)","Taxas (R$)","Real (R$)"],barmode="group",
        color_discrete_sequence=["#58a6ff","#f85149","#3fb950"],labels={"value":"R$","variable":""})
    fig_op.update_layout(plot_bgcolor="#161b22",paper_bgcolor="#0d1117",font=dict(color="#8b949e"),
        legend=dict(bgcolor="#161b22",bordercolor="#30363d"),yaxis=dict(gridcolor="#21262d"),
        margin=dict(t=10,b=10),height=360)
    st.plotly_chart(fig_op, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr style="border-color:#21262d;margin-top:48px"/>
<div style="text-align:center;color:#484f58;font-size:11px;padding-bottom:16px">
    Dashboard de portfólio — Dados fictícios para fins demonstrativos · Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
