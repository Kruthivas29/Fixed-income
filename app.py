import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

# ── All data embedded inline – no external files needed ─────────────────────
_CSV = {
"bond": """Year,US_Total,US_Government,US_Corporate,India_Total,India_Government,India_Corporate,GCC_Total_USDbn,GCC_Saudi_USDbn,GCC_UAE_USDbn,GCC_GDP_Proxy_pct
2018,163,84,46,14,11,3,58,28,16,2.76
2019,168,88,47,15,11,3,72,39,17,3.43
2020,190,100,51,17,13,4,76,37,23,3.62
2021,181,98,49,17,13,4,95,46,27,4.52
2022,169,95,46,16,12,4,100,51,28,4.76
2023,163,97,44,18,13,5,142,72,35,6.76
2024,155,98,46,19,14,5,148,80,39,7.05""",

"liq": """Indicator,US,India,GCC,Unit,Source
Daily Govt Bond Turnover,900,4,0.5,USD bn,SIFMA / RBI / Markaz
Corporate Bond ADV,51.6,0.3,0.1,USD bn,SIFMA / SEBI
Bid-Ask Spread (Govt),1.5,20,35,basis points,BIS / CRISIL
Turnover Ratio,1.80,0.28,0.08,ratio,BIS / Markaz
Foreign Investor Share,33,1,7.5,percent,TIC / RBI / Markaz""",

"inv": """Investor_Category,US,India,GCC
Commercial Banks,10,40,50
Pension Funds / Insurance,30,20,10
Mutual Funds,15,12,8
Foreign Investors,33,1,7.5
Sovereign Wealth Funds,2,1,25
Retail / Other,10,26,7""",

"struct": """Indicator,US,India,GCC,Unit
Bank Credit / GDP,50,75,70,percent
Corp Bonds / GDP,46,5,8,percent
10Y Sovereign Yield,4.5,7.0,5.5,percent
Annualised Yield Volatility,0.80,1.50,1.20,percent
CPI Inflation,3.0,5.5,2.5,percent
Real Yield,1.5,1.5,3.0,percent
HHI Concentration Index,2418,2822,3394,score""",

"h3cross": """Country,Bank_Credit_GDP_pct,Corp_Bonds_GDP_pct
United States,50,46
Japan,100,18
Germany,80,8
United Kingdom,65,25
India,75,5
Saudi Arabia,68,7
UAE,72,9
China,180,35
Brazil,70,12
South Africa,45,20""",

"panel": """Country,Year,Bond_GDP_pct,BankCredit_GDP_pct
US,2018,163,49
US,2019,168,50
US,2020,190,55
US,2021,181,54
US,2022,169,52
US,2023,163,51
US,2024,155,50
India,2018,14,72
India,2019,15,73
India,2020,17,74
India,2021,17,73
India,2022,16,74
India,2023,18,75
India,2024,19,75
GCC,2018,2.76,66
GCC,2019,3.43,67
GCC,2020,3.62,68
GCC,2021,4.52,69
GCC,2022,4.76,70
GCC,2023,6.76,70
GCC,2024,7.05,70""",

"hyp": """Hypothesis,Statement,Test_Method,Test_Statistic,P_Value,Decision,Support_Level
H1,Bond-market / GDP differs across US India GCC,One-way ANOVA,1210.99,0.000,Reject H0,Strongly Supported
H2,Investor HHI is negatively correlated with liquidity,Pearson Correlation (r=-0.87),−0.87,0.330,Fail to reject H0 (n too small),Direction Supported
H3 Cross-section,Bank-credit dominance predicts corp-bond size,OLS Regression,0.077,0.543,Fail to reject H0,Not Supported
H3 Panel FE,Bank-credit dominance after country fixed effects,Panel FE / LSDV,3.17,0.000,Significant,Strongly Supported
H4,Yield pickup in EM not justified on risk-adjusted basis,Sharpe Differential,1.67,n/a,H0 not rejected - India/GCC attractive,Partially Supported""",

"yield_": """Metric,US,India,GCC
Nominal Yield pct,4.5,7.0,5.5
Real Yield pct,1.5,1.5,3.0
Yield Volatility pct,0.80,1.50,1.20
Nominal Pickup vs US bps,0,250,100
Real Pickup vs US bps,0,0,150
Sharpe Ratio,0,1.67,0.83
Yield per unit Volatility,5.63,4.67,4.58""",
}

def _df(key): return pd.read_csv(io.StringIO(_CSV[key]))

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fixed-Income Market Disparities",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour Palette ───────────────────────────────────────────────────────────
PALETTE = {
    "US":    "#1B4F8A",
    "India": "#2E7D5E",
    "GCC":   "#B5862A",
    "border":"#D1DCE8",
    "text":  "#1A2733",
    "muted": "#6B7C8C",
    "white": "#FFFFFF",
}

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  .main .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}
  body, .stApp {{ background-color: #F5F8FC; color: {PALETTE['text']}; }}
  [data-testid="stSidebar"] {{ background-color: {PALETTE['white']}; border-right: 1px solid {PALETTE['border']}; }}
  [data-testid="stMetric"] {{ background: {PALETTE['white']}; border: 1px solid {PALETTE['border']}; border-radius: 8px; padding: 0.8rem 1rem; }}
  [data-testid="stMetricLabel"] {{ color: {PALETTE['muted']} !important; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
  [data-testid="stMetricValue"] {{ color: {PALETTE['text']} !important; font-size: 1.5rem; font-weight: 700; }}
  .section-header {{ background: {PALETTE['US']}; color: #fff; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.8rem; margin-top: 1rem; }}
  .badge-supported    {{ background:#D4EDDA; color:#155724; border-radius:4px; padding:3px 8px; font-size:0.78rem; font-weight:600; }}
  .badge-partial      {{ background:#FFF3CD; color:#856404; border-radius:4px; padding:3px 8px; font-size:0.78rem; font-weight:600; }}
  .badge-notsupported {{ background:#F8D7DA; color:#721C24; border-radius:4px; padding:3px 8px; font-size:0.78rem; font-weight:600; }}
  hr {{ border: none; border-top: 1px solid {PALETTE['border']}; margin: 1rem 0; }}
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    return (_df("bond"), _df("liq"), _df("inv"), _df("struct"),
            _df("h3cross"), _df("panel"), _df("hyp"), _df("yield_"))

bond, liq, inv, struct, h3cross, panel, hyp, yield_ = load()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Fixed-Income Dashboard")
    st.markdown("---")
    st.markdown("""
**Author:** Rishika Jain (MS25GF037)  
**Programme:** MGB – Global Finance  
**Institution:** SP Jain School of Global Management  
**Topic:** Fixed-Income Market Disparities: US, India & GCC  
**Period:** 2018 – 2024
""")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Overview",
        "📈 H1 – Market Depth",
        "👥 H2 – Investor Base",
        "🏦 H3 – Structural Constraints",
        "💹 H4 – Yield & Risk",
        "🧪 Hypothesis Summary",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"<small style='color:{PALETTE['muted']}'>Sources: BIS · IMF · World Bank · SIFMA · CRISIL · RBI · Markaz · OECD</small>", unsafe_allow_html=True)

# ── Helper ───────────────────────────────────────────────────────────────────
def layout():
    return dict(paper_bgcolor="white", plot_bgcolor="#F5F8FC",
                yaxis=dict(gridcolor=PALETTE["border"]),
                xaxis=dict(gridcolor=PALETTE["border"]),
                legend=dict(orientation="h"),
                margin=dict(t=20, b=50, l=55, r=20))


# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("Fixed-Income Market Disparities")
    st.subheader("Comparative Analysis: United States · India · Gulf Economies (2018–2024)")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("US Bond Market / GDP", "155%", "2024 est.")
    c2.metric("India Bond Market / GDP", "19%", "+1pp vs 2023")
    c3.metric("GCC Issuance 2024", "$148 bn", "+4% vs 2023")
    c4.metric("US–India Depth Ratio", "8.2×", "size gap")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Bond Market / GDP – Trend (2018–2024)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=bond.Year, y=bond.US_Total, name="US",
            line=dict(color=PALETTE["US"], width=3)))
        fig.add_trace(go.Scatter(x=bond.Year, y=bond.India_Total, name="India",
            line=dict(color=PALETTE["India"], width=3)))
        fig.add_trace(go.Scatter(x=bond.Year, y=bond.GCC_GDP_Proxy_pct, name="GCC proxy",
            line=dict(color=PALETTE["GCC"], width=3, dash="dot")))
        fig.update_layout(yaxis_title="% of GDP", height=320, **layout())
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Investor Base Composition (2024)</div>', unsafe_allow_html=True)
        fig2 = make_subplots(rows=1, cols=3, specs=[[{"type":"pie"},{"type":"pie"},{"type":"pie"}]],
                             subplot_titles=["US","India","GCC"])
        pie_colors = ["#1B4F8A","#2E7D5E","#B5862A","#5B8DB8","#8BC5A8","#D4B96A"]
        for i, mkt in enumerate(["US","India","GCC"]):
            fig2.add_trace(go.Pie(labels=inv.Investor_Category, values=inv[mkt],
                marker_colors=pie_colors, textposition="inside", textfont_size=9, hole=0.3),
                row=1, col=i+1)
        fig2.update_layout(paper_bgcolor="white", height=320, margin=dict(t=40,b=10,l=10,r=10),
            legend=dict(orientation="v", x=1.02, font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Research Hypotheses</div>', unsafe_allow_html=True)
        items = [
            ("H1","Market Depth & Liquidity Disparity","Strongly Supported","supported"),
            ("H2","Investor Base Diversification","Direction Supported","partial"),
            ("H3 Cross","Structural / Bank Dominance (OLS)","Not Supported","notsupported"),
            ("H3 Panel","Structural / Bank Dominance (FE)","Strongly Supported","supported"),
            ("H4","Yield Pickup – Risk Adjusted","Partially Supported","partial"),
        ]
        for h, stmt, v, cls in items:
            st.markdown(f"**{h}** — {stmt} &nbsp;<span class='badge-{cls}'>{v}</span>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-header">Key Findings</div>', unsafe_allow_html=True)
        st.markdown("""
- 🇺🇸 US leads with **155% bond/GDP** vs India's **19%** — an **8× gap**
- 🇮🇳 India is bank-dominated (~40%) with only **1% foreign participation**
- 🌍 GCC issuance grew **+155%** (2018–2024), driven by Saudi & UAE
- 📊 **ANOVA F = 1,211** confirms statistically significant depth differences
- 🏦 **Panel FE β₁ = 3.17** — bank credit crowds out bond markets within countries
- 💰 India yields (+250 bps) attractive but real yield parity limits the pickup
""")


# ══════════════════════════════════════════════════════════════════════════════
# H1 – MARKET DEPTH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 H1 – Market Depth":
    st.title("H1 – Fixed-Income Market Depth & Liquidity")
    st.markdown('<span class="badge-supported">✅ Strongly Supported | F = 1,210.99 | p < 0.0001</span>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Bond Market Size", "GCC Issuance Growth", "Liquidity Comparison"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Total Bond Market / GDP (%)</div>', unsafe_allow_html=True)
            fig = go.Figure()
            for mkt, col_n, clr in [("US","US_Total",PALETTE["US"]),("India","India_Total",PALETTE["India"])]:
                fig.add_trace(go.Bar(x=bond.Year, y=bond[col_n], name=mkt,
                    marker_color=clr, opacity=0.85))
            fig.update_layout(barmode="group", yaxis_title="% of GDP", height=360, **layout())
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">US Bond Breakdown / GDP (%)</div>', unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=bond.Year, y=bond.US_Government, name="Government",
                fill="tozeroy", line=dict(color=PALETTE["US"]), fillcolor="rgba(27,79,138,0.25)"))
            fig2.add_trace(go.Scatter(x=bond.Year, y=bond.US_Corporate, name="Corporate",
                fill="tozeroy", line=dict(color=PALETTE["GCC"]), fillcolor="rgba(181,134,42,0.25)"))
            fig2.update_layout(yaxis_title="% of GDP", height=360, **layout())
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-header">ANOVA Results</div>', unsafe_allow_html=True)
        anova = pd.DataFrame({
            "Source":["Between Groups","Within Groups","Total"],
            "SS":[11.88,0.088,11.97], "df":[2,18,20],
            "MS":[5.940,0.005,""], "F-Statistic":["1,210.99","",""],
            "p-value":["< 0.0001 ✅","",""],
        })
        st.dataframe(anova, use_container_width=True, hide_index=True)
        st.info("F = 1,210.99 >> F-critical (3.55) → Reject H₀. Bond market depth differs significantly across US, India, and GCC.")

    with tab2:
        st.markdown('<div class="section-header">GCC Issuance by Country – USD Billion</div>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=bond.Year, y=bond.GCC_Saudi_USDbn, name="Saudi Arabia", marker_color=PALETTE["US"]))
        fig3.add_trace(go.Bar(x=bond.Year, y=bond.GCC_UAE_USDbn, name="UAE", marker_color=PALETTE["GCC"]))
        others = bond.GCC_Total_USDbn - bond.GCC_Saudi_USDbn - bond.GCC_UAE_USDbn
        fig3.add_trace(go.Bar(x=bond.Year, y=others, name="Other GCC", marker_color=PALETTE["India"]))
        fig3.update_layout(barmode="stack", yaxis_title="USD Billion", height=400, **layout())
        st.plotly_chart(fig3, use_container_width=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("2018 GCC Issuance","$58 bn")
        c2.metric("2024 GCC Issuance","$148 bn")
        c3.metric("Growth 2018–2024","+155%","+$90 bn")

    with tab3:
        st.markdown('<div class="section-header">Liquidity Metrics (2024)</div>', unsafe_allow_html=True)
        for _, row in liq[liq.Indicator.isin(["Daily Govt Bond Turnover","Corporate Bond ADV","Turnover Ratio"])].iterrows():
            st.markdown(f"**{row.Indicator}** ({row.Unit})")
            vals = {"US": float(row.US), "India": float(row.India), "GCC": float(row.GCC)}
            max_v = max(vals.values()) or 1
            cols = st.columns(3)
            for idx, (mkt, v) in enumerate(vals.items()):
                pct = int(v / max_v * 100)
                clr = [PALETTE["US"], PALETTE["India"], PALETTE["GCC"]][idx]
                cols[idx].markdown(f"""
                    <div style='background:{clr};height:8px;border-radius:4px;width:{pct}%;margin-bottom:2px'></div>
                    <b style='color:{clr}'>{mkt}</b> {v:,.2f}
                """, unsafe_allow_html=True)
            st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# H2 – INVESTOR BASE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 H2 – Investor Base":
    st.title("H2 – Investor Base Diversification & Liquidity")
    st.markdown('<span class="badge-partial">⚠️ Direction Supported | Pearson r = −0.87 | p = 0.33 (n=3)</span>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Investor Composition by Market (%)</div>', unsafe_allow_html=True)
        inv_melt = inv.melt(id_vars="Investor_Category", var_name="Market", value_name="Share_pct")
        fig = px.bar(inv_melt, x="Investor_Category", y="Share_pct", color="Market",
            barmode="group",
            color_discrete_map={"US":PALETTE["US"],"India":PALETTE["India"],"GCC":PALETTE["GCC"]},
            labels={"Share_pct":"Share (%)","Investor_Category":""})
        fig.update_layout(height=380, xaxis_tickangle=-30, **layout())
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">HHI vs Turnover Ratio</div>', unsafe_allow_html=True)
        hhi_data = pd.DataFrame({"Market":["US","India","GCC"],
            "HHI":[2418,2822,3394], "Turnover_Ratio":[1.80,0.28,0.08]})
        fig2 = px.scatter(hhi_data, x="HHI", y="Turnover_Ratio", text="Market", color="Market",
            color_discrete_map={"US":PALETTE["US"],"India":PALETTE["India"],"GCC":PALETTE["GCC"]},
            labels={"HHI":"HHI Concentration","Turnover_Ratio":"Turnover Ratio"})
        x_r = np.linspace(2300,3500,100)
        z = np.polyfit(hhi_data.HHI, hhi_data.Turnover_Ratio, 1)
        fig2.add_trace(go.Scatter(x=x_r, y=np.poly1d(z)(x_r), mode="lines",
            name="Trend (r=−0.87)", line=dict(color="#999", dash="dash", width=1.5)))
        fig2.update_traces(textposition="top center", selector=dict(mode="markers+text"))
        fig2.update_layout(height=380, **layout())
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">HHI Summary</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Market":["US","India","GCC"],
        "HHI Score":["2,418","2,822","3,394"],
        "Classification":["Moderately Concentrated","Highly Concentrated","Highly Concentrated"],
        "Foreign Share":["33%","1%","7.5%"],
        "Turnover Ratio":["1.80","0.28","0.08"],
    }), use_container_width=True, hide_index=True)
    st.info("Strong negative directional correlation (r = −0.87) between HHI and turnover confirms H2's logic. Statistical significance is limited by sample size (n=3).")


# ══════════════════════════════════════════════════════════════════════════════
# H3 – STRUCTURAL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏦 H3 – Structural Constraints":
    st.title("H3 – Bank Credit Dominance vs Corporate Bond Markets")
    st.markdown("---")
    tab1, tab2 = st.tabs(["Cross-Section OLS (n=10)", "Panel Fixed Effects (3×7)"])

    with tab1:
        st.markdown('<span class="badge-notsupported">❌ Cross-section OLS: Fail to Reject H₀ | β₁ = 0.077 | p = 0.543</span>', unsafe_allow_html=True)
        st.markdown("")
        col1, col2 = st.columns([3,2])
        with col1:
            st.markdown('<div class="section-header">Bank Credit/GDP vs Corp Bonds/GDP</div>', unsafe_allow_html=True)
            fig = px.scatter(h3cross, x="Bank_Credit_GDP_pct", y="Corp_Bonds_GDP_pct",
                text="Country", color_discrete_sequence=[PALETTE["US"]],
                labels={"Bank_Credit_GDP_pct":"Bank Credit/GDP (%)","Corp_Bonds_GDP_pct":"Corp Bonds/GDP (%)"})
            z = np.polyfit(h3cross.Bank_Credit_GDP_pct, h3cross.Corp_Bonds_GDP_pct, 1)
            x_r = np.linspace(40,185,100)
            fig.add_trace(go.Scatter(x=x_r, y=np.poly1d(z)(x_r), mode="lines",
                name="OLS (β₁=0.077, p=0.54)", line=dict(color=PALETTE["GCC"], dash="dash")))
            fig.update_traces(textposition="top center", selector=dict(mode="markers+text"))
            fig.update_layout(height=420, **layout())
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">OLS Summary</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({
                "Parameter":["β₀","β₁ (BankCredit/GDP)","R²","t-stat","p-value","n"],
                "Value":["0.123","0.077","4.8%","0.635","0.543","10"],
            }), hide_index=True, use_container_width=True)
            st.warning("No significant relationship in cross-section — likely driven by outliers (China, US).")

    with tab2:
        st.markdown('<span class="badge-supported">✅ Panel FE: Strongly Supported | β₁ = 3.17 | p < 0.0001</span>', unsafe_allow_html=True)
        st.markdown("")
        col1, col2 = st.columns([3,2])
        with col1:
            st.markdown('<div class="section-header">Panel: Bond/GDP vs BankCredit/GDP (2018–2024)</div>', unsafe_allow_html=True)
            fig2 = px.scatter(panel, x="BankCredit_GDP_pct", y="Bond_GDP_pct",
                color="Country", symbol="Country", hover_data=["Year"],
                color_discrete_map={"US":PALETTE["US"],"India":PALETTE["India"],"GCC":PALETTE["GCC"]},
                labels={"BankCredit_GDP_pct":"Bank Credit/GDP (%)","Bond_GDP_pct":"Bond Market/GDP (%)"})
            fig2.update_layout(height=420, **layout())
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Fixed Effects Results</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({
                "Parameter":["β₁ (BankCredit/GDP)","γ_US","γ_India","R² (FE)","F-stat overall","F-stat Pooled vs FE","p-value (β₁)"],
                "Value":["3.171 **","2.191 **","−0.044","99.7%","1,924.8","377.1 **","< 0.0001"],
            }), hide_index=True, use_container_width=True)
            st.success("Country FE preferred. β₁ = 3.17 significant after controlling for country heterogeneity.")
            st.markdown("**Note on sign reversal:** Pooled OLS β₁ < 0, FE β₁ > 0 — Simpson's paradox. Cross-country differences dominate pooled OLS; FE reveals within-country time dynamics.")


# ══════════════════════════════════════════════════════════════════════════════
# H4 – YIELD & RISK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💹 H4 – Yield & Risk":
    st.title("H4 – Yield Pickup vs Risk-Adjusted Return")
    st.markdown('<span class="badge-partial">⚠️ Partially Supported | India Sharpe = 1.67 | GCC Sharpe = 0.83</span>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Nominal vs Real Yield (%)</div>', unsafe_allow_html=True)
        yp = pd.DataFrame({"Market":["US","India","GCC"],
            "Nominal Yield":[4.5,7.0,5.5], "Real Yield":[1.5,1.5,3.0], "Inflation":[3.0,5.5,2.5]})
        fig = go.Figure()
        for col_n, clr in [("Nominal Yield",PALETTE["US"]),("Real Yield",PALETTE["India"]),("Inflation",PALETTE["GCC"])]:
            fig.add_trace(go.Bar(x=yp.Market, y=yp[col_n], name=col_n, marker_color=clr, opacity=0.85))
        fig.update_layout(barmode="group", yaxis_title="% p.a.", height=360, **layout())
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Sharpe Ratio & Yield/Volatility</div>', unsafe_allow_html=True)
        sd = pd.DataFrame({"Market":["US","India","GCC"],
            "Sharpe":[0,1.67,0.83], "YieldVol":[5.63,4.67,4.58]})
        fig2 = make_subplots(specs=[[{"secondary_y":True}]])
        fig2.add_trace(go.Bar(x=sd.Market, y=sd.Sharpe, name="Sharpe Ratio",
            marker_color=[PALETTE["US"],PALETTE["India"],PALETTE["GCC"]], opacity=0.85), secondary_y=False)
        fig2.add_trace(go.Scatter(x=sd.Market, y=sd.YieldVol, name="Yield/Vol",
            mode="lines+markers", line=dict(color=PALETTE["GCC"],width=2), marker=dict(size=10)), secondary_y=True)
        fig2.update_yaxes(title_text="Sharpe Ratio", secondary_y=False, gridcolor=PALETTE["border"])
        fig2.update_yaxes(title_text="Yield per unit of Vol", secondary_y=True)
        fig2.update_layout(paper_bgcolor="white", plot_bgcolor="#F5F8FC", height=360,
            legend=dict(orientation="h"), margin=dict(t=20,b=60,l=50,r=60))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Risk Summary Table</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Metric":["10Y Yield (%)","Yield Volatility (%)","CPI Inflation (%)","Real Yield (%)","Nominal Pickup vs US (bps)","Real Pickup vs US (bps)","Sharpe Ratio","Yield / Volatility"],
        "US":["4.5","0.80","3.0","1.5","—","—","0.00","5.63"],
        "India":["7.0","1.50","5.5","1.5","+250","≈0","1.67 ✅","4.67"],
        "GCC":["5.5","1.20","2.5","3.0","+100","+150","0.83","4.58"],
    }), use_container_width=True, hide_index=True)
    st.info("India's +250 bps nominal pickup is eroded by higher inflation — real yield equals US at 1.5%. GCC shows strongest real pickup (+150 bps). H4 is not rejected — EM markets screen as attractive on Sharpe basis before FX/transaction costs.")


# ══════════════════════════════════════════════════════════════════════════════
# HYPOTHESIS SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧪 Hypothesis Summary":
    st.title("Hypothesis Testing – Summary")
    st.markdown("---")

    st.markdown('<div class="section-header">Results Scorecard</div>', unsafe_allow_html=True)
    rows = [
        ("H1","Bond-market/GDP differs across US, India & GCC","One-way ANOVA","F = 1,210.99","< 0.0001","Reject H₀","supported","✅ Strongly Supported"),
        ("H2","Investor HHI inversely related to liquidity","Pearson r","r = −0.87","0.330","Fail (n=3)","partial","⚠️ Direction Supported"),
        ("H3 OLS","Bank-credit dominance – cross-section","OLS","β₁ = 0.077","0.543","Fail to Reject","notsupported","❌ Not Supported"),
        ("H3 FE","Bank-credit dominance – panel fixed effects","Panel FE","β₁ = 3.171","< 0.0001","Reject H₀","supported","✅ Strongly Supported"),
        ("H4","EM yield pickup not justified risk-adjusted","Sharpe","SR_India=1.67","n/a","H₀ not rejected","partial","⚠️ Partially Supported"),
    ]
    for h,stmt,test,stat,pv,dec,cls,badge in rows:
        c1,c2,c3,c4 = st.columns([1,4,3,2])
        c1.markdown(f"**{h}**")
        c2.markdown(stmt)
        c3.markdown(f"*{test}* — `{stat}` | p={pv}")
        c4.markdown(f"<span class='badge-{cls}'>{badge}</span>", unsafe_allow_html=True)
        st.markdown('<hr style="margin:0.3rem 0">', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Statistical Significance (−log₁₀ p-value)</div>', unsafe_allow_html=True)
        labels = ["H1 ANOVA","H2 Corr","H3 OLS","H3 FE","H4 Sharpe"]
        pvals  = [1e-20, 0.330, 0.543, 9.43e-5, None]
        sig    = [-np.log10(p) if p else 0 for p in pvals]
        colors = [PALETTE["India"],PALETTE["GCC"],"#C0392B",PALETTE["US"],PALETTE["muted"]]
        fig = go.Figure(go.Bar(x=labels, y=sig, marker_color=colors, opacity=0.85))
        fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="#C0392B",
                      annotation_text="α=0.05", annotation_position="top right")
        fig.update_layout(yaxis_title="−log₁₀(p)", height=340, **layout())
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Limitations & Next Steps</div>', unsafe_allow_html=True)
        st.markdown("""
**Limitations:**
- H1/H2: only 3 markets → low statistical power
- H3 cross-section: n=10, outliers distort β
- H4: no FX hedging or bid-ask costs included
- GCC data primarily issuance, not outstanding stock

**Recommended Robustness:**
- Kruskal-Wallis non-parametric test (H1)
- Bootstrapped CIs (H2)
- 20+ country panel (H3)
- GARCH-adjusted volatility (H4)
- Exclude 2020 COVID year as sensitivity check

**Sources:** BIS · SIFMA · CRISIL · RBI · SEBI · Markaz · OECD · IMF · World Bank
""")
