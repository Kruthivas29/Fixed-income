import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# Resolve data folder relative to this script (works locally + Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fixed-Income Market Disparities",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour Palette ───────────────────────────────────────────────────────────
PALETTE = {
    "US":     "#1B4F8A",   # navy
    "India":  "#2E7D5E",   # teal-green
    "GCC":    "#B5862A",   # gold
    "accent": "#E8F0F7",
    "border": "#D1DCE8",
    "text":   "#1A2733",
    "muted":  "#6B7C8C",
    "white":  "#FFFFFF",
    "H_yes":  "#2E7D5E",
    "H_part": "#B5862A",
    "H_no":   "#C0392B",
}

MARKET_COLORS = [PALETTE["US"], PALETTE["India"], PALETTE["GCC"]]

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Base */
  .main .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}
  body, .stApp {{ background-color: #F5F8FC; color: {PALETTE['text']}; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{ background-color: {PALETTE['white']}; border-right: 1px solid {PALETTE['border']}; }}
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {{ color: {PALETTE['US']}; }}

  /* Metric Cards */
  [data-testid="stMetric"] {{ background: {PALETTE['white']}; border: 1px solid {PALETTE['border']};
      border-radius: 8px; padding: 0.8rem 1rem; }}
  [data-testid="stMetricLabel"] {{ color: {PALETTE['muted']} !important; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
  [data-testid="stMetricValue"] {{ color: {PALETTE['text']} !important; font-size: 1.5rem; font-weight: 700; }}

  /* Section headers */
  .section-header {{ background: {PALETTE['US']}; color: {PALETTE['white']};
      padding: 0.5rem 1rem; border-radius: 6px; font-weight: 700;
      font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase;
      margin-bottom: 0.8rem; margin-top: 1rem; }}

  /* Hypothesis badge */
  .badge-supported   {{ background:#D4EDDA; color:#155724; border-radius:4px; padding:3px 8px; font-size:0.78rem; font-weight:600; }}
  .badge-partial     {{ background:#FFF3CD; color:#856404; border-radius:4px; padding:3px 8px; font-size:0.78rem; font-weight:600; }}
  .badge-notsupported{{ background:#F8D7DA; color:#721C24; border-radius:4px; padding:3px 8px; font-size:0.78rem; font-size:0.78rem; font-weight:600; }}

  /* Tab styling */
  button[data-baseweb="tab"] {{ font-weight: 600; }}
  button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid {PALETTE['US']}; color: {PALETTE['US']}; }}

  /* Divider */
  hr {{ border: none; border-top: 1px solid {PALETTE['border']}; margin: 1rem 0; }}
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    def p(f): return os.path.join(DATA_DIR, f)
    bond    = pd.read_csv(p("bond_market_size.csv"))
    liq     = pd.read_csv(p("liquidity_indicators.csv"))
    inv     = pd.read_csv(p("investor_composition.csv"))
    struct  = pd.read_csv(p("structural_indicators.csv"))
    h3cross = pd.read_csv(p("cross_country_h3.csv"))
    panel   = pd.read_csv(p("panel_regression.csv"))
    hyp     = pd.read_csv(p("hypothesis_summary.csv"))
    yield_  = pd.read_csv(p("yield_risk.csv"))
    return bond, liq, inv, struct, h3cross, panel, hyp, yield_

bond, liq, inv, struct, h3cross, panel, hyp, yield_ = load()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/SP_Jain_School_of_Global_Management_logo.png/320px-SP_Jain_School_of_Global_Management_logo.png",
             use_container_width=True)
    st.markdown("---")
    st.markdown("### 📌 Research Overview")
    st.markdown("""
**Author:** Rishika Jain (MS25GF037)  
**Programme:** MGB – Global Finance  
**Institution:** SP Jain School of Global Management  
**Topic:** Fixed-Income Market Disparities: US, India & GCC  
**Period:** 2018 – 2024
""")
    st.markdown("---")
    st.markdown("### 🗂️ Navigation")
    page = st.radio("Go to section", [
        "🏠 Overview",
        "📈 H1 – Market Depth",
        "👥 H2 – Investor Base",
        "🏦 H3 – Structural Constraints",
        "💹 H4 – Yield & Risk",
        "🧪 Hypothesis Summary",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"<small style='color:{PALETTE['muted']}'>Sources: BIS · IMF · World Bank · SIFMA · CRISIL · RBI · Markaz · OECD</small>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("Fixed-Income Market Disparities")
    st.subheader("A Comparative Analysis of the United States, India & Gulf Economies")
    st.markdown("---")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("US Bond Market / GDP", "155%", "+0% vs 2023", help="2024 estimate")
    c2.metric("India Bond Market / GDP", "19%", "+1pp vs 2023")
    c3.metric("GCC Issuance (2024)", "$148 bn", "+4% vs 2023")
    c4.metric("US–India Size Ratio", "8.2×", "depth gap")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Bond Market / GDP – All Regions (2018–2024)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=bond["Year"], y=bond["US_Total"],
            name="US", line=dict(color=PALETTE["US"], width=3)))
        fig.add_trace(go.Scatter(x=bond["Year"], y=bond["India_Total"],
            name="India", line=dict(color=PALETTE["India"], width=3)))
        fig.add_trace(go.Scatter(x=bond["Year"], y=bond["GCC_GDP_Proxy_pct"],
            name="GCC (proxy)", line=dict(color=PALETTE["GCC"], width=3, dash="dot")))
        fig.update_layout(
            yaxis_title="% of GDP", xaxis_title="Year",
            legend=dict(orientation="h", y=-0.2),
            paper_bgcolor="white", plot_bgcolor="#F5F8FC",
            margin=dict(t=20, b=60, l=50, r=20), height=320,
            yaxis=dict(gridcolor=PALETTE["border"]),
            xaxis=dict(gridcolor=PALETTE["border"]),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Investor Base Composition (2024)</div>', unsafe_allow_html=True)
        fig2 = make_subplots(rows=1, cols=3, specs=[[{"type":"pie"},{"type":"pie"},{"type":"pie"}]],
                             subplot_titles=["US", "India", "GCC"])
        cats = inv["Investor_Category"].tolist()
        pie_colors = ["#1B4F8A","#2E7D5E","#B5862A","#5B8DB8","#8BC5A8","#D4B96A"]
        for i, (mkt, col) in enumerate([("US",1),("India",2),("GCC",3)]):
            fig2.add_trace(go.Pie(labels=cats, values=inv[mkt].tolist(),
                name=mkt, marker_colors=pie_colors,
                textposition="inside", textfont_size=9,
                hole=0.3), row=1, col=col)
        fig2.update_layout(paper_bgcolor="white", height=320,
            margin=dict(t=40, b=20, l=10, r=10),
            legend=dict(orientation="v", x=1.02, font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Research Hypotheses at a Glance</div>', unsafe_allow_html=True)
        hyp_data = [
            ("H1", "Market Depth & Liquidity Disparity", "Strongly Supported", "supported"),
            ("H2", "Investor Base Diversification", "Direction Supported", "partial"),
            ("H3 Cross", "Structural / Bank Dominance (OLS)", "Not Supported", "notsupported"),
            ("H3 Panel", "Structural / Bank Dominance (FE)", "Strongly Supported", "supported"),
            ("H4", "Yield Pickup – Risk Adjusted", "Partially Supported", "partial"),
        ]
        for h, stmt, verdict, cls in hyp_data:
            st.markdown(f"**{h}** — {stmt}  &nbsp; <span class='badge-{cls}'>{verdict}</span>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-header">Key Takeaways</div>', unsafe_allow_html=True)
        st.markdown("""
- 🇺🇸 **US** leads with **155% bond/GDP** vs India's **19%** — an **8× gap**
- 🇮🇳 **India** is bank-dominated (~40% banks) with only **1% foreign participation**
- 🌍 **GCC** issuance grew **+155%** (2018–2024) driven by Saudi Arabia & UAE
- 📊 **ANOVA F = 1,211** confirms statistically significant depth differences (H1)
- 🏦 **Panel FE** reveals bank-credit crowding out bond markets within countries (H3)
- 💰 India yields (+250 bps) look attractive but risk-adjusted picture is mixed (H4)
""")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: H1 – MARKET DEPTH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 H1 – Market Depth":
    st.title("H1 – Fixed-Income Market Depth & Liquidity")
    st.markdown('<span class="badge-supported">✅ Strongly Supported | F-stat = 1,210.99 | p < 0.0001</span>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Bond Market Size", "GCC Issuance Growth", "Liquidity Comparison"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Total Bond Market / GDP (%)</div>', unsafe_allow_html=True)
            fig = go.Figure()
            for mkt, col_name, clr in [("US","US_Total",PALETTE["US"]),
                                        ("India","India_Total",PALETTE["India"])]:
                fig.add_trace(go.Bar(x=bond["Year"], y=bond[col_name],
                    name=mkt, marker_color=clr, opacity=0.85))
            fig.update_layout(barmode="group", yaxis_title="% of GDP",
                paper_bgcolor="white", plot_bgcolor="#F5F8FC",
                legend=dict(orientation="h"), height=360,
                yaxis=dict(gridcolor=PALETTE["border"]),
                xaxis=dict(gridcolor=PALETTE["border"]),
                margin=dict(t=20, b=40, l=50, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">US Bond Composition / GDP (%)</div>', unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=bond["Year"], y=bond["US_Government"],
                name="Government", fill="tozeroy",
                line=dict(color=PALETTE["US"]), fillcolor="rgba(27,79,138,0.25)"))
            fig2.add_trace(go.Scatter(x=bond["Year"], y=bond["US_Corporate"],
                name="Corporate", fill="tozeroy",
                line=dict(color=PALETTE["GCC"]), fillcolor="rgba(181,134,42,0.25)"))
            fig2.update_layout(yaxis_title="% of GDP",
                paper_bgcolor="white", plot_bgcolor="#F5F8FC",
                legend=dict(orientation="h"), height=360,
                yaxis=dict(gridcolor=PALETTE["border"]),
                xaxis=dict(gridcolor=PALETTE["border"]),
                margin=dict(t=20, b=40, l=50, r=20))
            st.plotly_chart(fig2, use_container_width=True)

        # ANOVA Table
        st.markdown('<div class="section-header">ANOVA Results – H1</div>', unsafe_allow_html=True)
        anova = pd.DataFrame({
            "Source": ["Between Groups", "Within Groups", "Total"],
            "SS": [11.88, 0.088, 11.97],
            "df": [2, 18, 20],
            "MS": [5.940, 0.005, ""],
            "F-Statistic": ["1,210.99", "", ""],
            "p-value": ["< 0.0001 ✅", "", ""],
        })
        st.dataframe(anova, use_container_width=True, hide_index=True)
        st.info("**Interpretation:** F = 1,210.99 >> F-critical (3.55) → Reject H₀. Bond market depth differs significantly across US, India, and GCC.")

    with tab2:
        st.markdown('<div class="section-header">GCC Total Issuance – USD Billion (2018–2024)</div>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=bond["Year"], y=bond["GCC_Saudi_USDbn"],
            name="Saudi Arabia", marker_color=PALETTE["US"]))
        fig3.add_trace(go.Bar(x=bond["Year"], y=bond["GCC_UAE_USDbn"],
            name="UAE", marker_color=PALETTE["GCC"]))
        # Others = Total - Saudi - UAE
        others = bond["GCC_Total_USDbn"] - bond["GCC_Saudi_USDbn"] - bond["GCC_UAE_USDbn"]
        fig3.add_trace(go.Bar(x=bond["Year"], y=others,
            name="Other GCC", marker_color=PALETTE["India"]))
        fig3.update_layout(barmode="stack", yaxis_title="USD Billion",
            paper_bgcolor="white", plot_bgcolor="#F5F8FC",
            legend=dict(orientation="h"), height=400,
            yaxis=dict(gridcolor=PALETTE["border"]),
            xaxis=dict(gridcolor=PALETTE["border"]),
            margin=dict(t=20, b=40, l=50, r=20))
        st.plotly_chart(fig3, use_container_width=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("2018 GCC Issuance", "$58 bn")
        c2.metric("2024 GCC Issuance", "$148 bn")
        c3.metric("Growth 2018–2024", "+155%", "+$90 bn")

    with tab3:
        st.markdown('<div class="section-header">Liquidity Comparison (2024)</div>', unsafe_allow_html=True)
        metrics = ["Daily Govt Bond Turnover", "Corporate Bond ADV", "Turnover Ratio"]
        liq_filt = liq[liq["Indicator"].isin(metrics)].copy()
        
        for _, row in liq_filt.iterrows():
            st.markdown(f"**{row['Indicator']}** ({row['Unit']})")
            vals = {"US": float(row["US"]), "India": float(row["India"]), "GCC": float(row["GCC"])}
            max_v = max(vals.values()) or 1
            cols = st.columns(3)
            for idx, (mkt, v) in enumerate(vals.items()):
                pct = int(v / max_v * 100)
                clr = [PALETTE["US"], PALETTE["India"], PALETTE["GCC"]][idx]
                cols[idx].markdown(f"""
                    <div style='background:{clr};height:8px;border-radius:4px;width:{pct}%;margin-bottom:2px'></div>
                    <b style='color:{clr}'>{mkt}</b> {v:,.1f}
                """, unsafe_allow_html=True)
            st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: H2 – INVESTOR BASE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 H2 – Investor Base":
    st.title("H2 – Investor Base Diversification & Liquidity")
    st.markdown('<span class="badge-partial">⚠️ Direction Supported | Pearson r = −0.87 | p = 0.33 (n=3 too small)</span>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Investor Composition by Market (%)</div>', unsafe_allow_html=True)
        inv_melt = inv.melt(id_vars="Investor_Category", var_name="Market", value_name="Share_pct")
        fig = px.bar(inv_melt, x="Investor_Category", y="Share_pct", color="Market",
            barmode="group", color_discrete_map={"US":PALETTE["US"],"India":PALETTE["India"],"GCC":PALETTE["GCC"]},
            labels={"Share_pct":"Share (%)", "Investor_Category":"Investor Category"})
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="#F5F8FC", height=380,
            xaxis_tickangle=-30, legend=dict(orientation="h"),
            yaxis=dict(gridcolor=PALETTE["border"]),
            margin=dict(t=20, b=80, l=50, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">HHI vs Turnover Ratio</div>', unsafe_allow_html=True)
        hhi_data = pd.DataFrame({
            "Market": ["US", "India", "GCC"],
            "HHI": [2418, 2822, 3394],
            "Turnover_Ratio": [1.80, 0.28, 0.08],
        })
        fig2 = px.scatter(hhi_data, x="HHI", y="Turnover_Ratio", text="Market",
            color="Market", color_discrete_map={"US":PALETTE["US"],"India":PALETTE["India"],"GCC":PALETTE["GCC"]},
            size=[40,40,40], labels={"HHI":"HHI Concentration", "Turnover_Ratio":"Turnover Ratio"})
        # trendline manually
        x_range = np.linspace(2300, 3500, 100)
        # linear fit
        z = np.polyfit(hhi_data["HHI"], hhi_data["Turnover_Ratio"], 1)
        p_fit = np.poly1d(z)
        fig2.add_trace(go.Scatter(x=x_range, y=p_fit(x_range),
            mode="lines", name="Trend (r=−0.87)",
            line=dict(color="#999", dash="dash", width=1.5)))
        fig2.update_traces(textposition="top center", selector=dict(mode='markers+text'))
        fig2.update_layout(paper_bgcolor="white", plot_bgcolor="#F5F8FC", height=380,
            yaxis=dict(gridcolor=PALETTE["border"]),
            xaxis=dict(gridcolor=PALETTE["border"]),
            margin=dict(t=20, b=40, l=60, r=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">HHI Concentration Summary</div>', unsafe_allow_html=True)
    hhi_df = pd.DataFrame({
        "Market": ["US", "India", "GCC"],
        "HHI Score": ["2,418", "2,822", "3,394"],
        "Classification": ["Moderately Concentrated", "Highly Concentrated", "Highly Concentrated"],
        "Foreign Share": ["33%", "1%", "7.5%"],
        "Turnover Ratio": ["1.80", "0.28", "0.08"],
    })
    st.dataframe(hhi_df, use_container_width=True, hide_index=True)
    st.info("**Interpretation:** Strong negative directional correlation (r = −0.87) between HHI and turnover confirms H2's logic. Statistical significance is limited by sample size (n=3 markets), warranting a wider panel in the full dissertation.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: H3 – STRUCTURAL CONSTRAINTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏦 H3 – Structural Constraints":
    st.title("H3 – Bank Credit Dominance vs Corporate Bond Markets")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Cross-Section OLS (n=10)", "Panel Fixed Effects (3×7)"])

    with tab1:
        st.markdown('<span class="badge-notsupported">❌ H3 Cross-section: Fail to Reject H₀ | β₁ = 0.077 | p = 0.543</span>', unsafe_allow_html=True)
        st.markdown("")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown('<div class="section-header">Bank Credit/GDP vs Corp Bonds/GDP (2024 Cross-Section)</div>', unsafe_allow_html=True)
            fig = px.scatter(h3cross, x="Bank_Credit_GDP_pct", y="Corp_Bonds_GDP_pct",
                text="Country",
                labels={"Bank_Credit_GDP_pct":"Bank Credit / GDP (%)", "Corp_Bonds_GDP_pct":"Corp Bonds / GDP (%)"},
                color_discrete_sequence=[PALETTE["US"]])
            # OLS trendline
            z = np.polyfit(h3cross["Bank_Credit_GDP_pct"], h3cross["Corp_Bonds_GDP_pct"], 1)
            x_r = np.linspace(40, 185, 100)
            fig.add_trace(go.Scatter(x=x_r, y=np.poly1d(z)(x_r),
                mode="lines", name=f"OLS (β₁=0.077, p=0.54)",
                line=dict(color=PALETTE["GCC"], dash="dash")))
            fig.update_traces(textposition="top center", selector=dict(mode="markers+text"))
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="#F5F8FC", height=400,
                yaxis=dict(gridcolor=PALETTE["border"]),
                xaxis=dict(gridcolor=PALETTE["border"]),
                margin=dict(t=20, b=40, l=60, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">OLS Summary</div>', unsafe_allow_html=True)
            ols_df = pd.DataFrame({
                "Parameter": ["β₀ (Intercept)", "β₁ (BankCredit/GDP)", "R²", "t-stat (β₁)", "p-value (β₁)", "n"],
                "Value": ["0.123", "0.077", "4.8%", "0.635", "0.543", "10"],
            })
            st.dataframe(ols_df, hide_index=True, use_container_width=True)
            st.warning("Cross-sectional OLS shows **no significant relationship** between bank credit and corporate bond market size — likely driven by outliers (China, US).")

    with tab2:
        st.markdown('<span class="badge-supported">✅ H3 Panel FE: Strongly Supported | β₁ = 3.17 | p < 0.0001</span>', unsafe_allow_html=True)
        st.markdown("")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown('<div class="section-header">Panel: Bond/GDP vs BankCredit/GDP (2018–2024)</div>', unsafe_allow_html=True)
            fig2 = px.scatter(panel, x="BankCredit_GDP_pct", y="Bond_GDP_pct",
                color="Country", symbol="Country",
                color_discrete_map={"US":PALETTE["US"],"India":PALETTE["India"],"GCC":PALETTE["GCC"]},
                labels={"BankCredit_GDP_pct":"Bank Credit/GDP (%)", "Bond_GDP_pct":"Bond Market/GDP (%)"},
                hover_data=["Year"])
            fig2.update_layout(paper_bgcolor="white", plot_bgcolor="#F5F8FC", height=420,
                yaxis=dict(gridcolor=PALETTE["border"]),
                xaxis=dict(gridcolor=PALETTE["border"]),
                margin=dict(t=20, b=40, l=60, r=20))
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Fixed Effects Summary</div>', unsafe_allow_html=True)
            fe_df = pd.DataFrame({
                "Parameter": ["β₁ (BankCredit/GDP)", "γ_US (Dummy)", "γ_India (Dummy)", "R² (FE)", "F-stat (overall)", "F-stat (Pooled vs FE)", "p-value (β₁)"],
                "Value": ["3.171 **", "2.191 **", "−0.044", "99.7%", "1,924.8", "377.1 **", "< 0.0001"],
            })
            st.dataframe(fe_df, hide_index=True, use_container_width=True)
            st.success("**Fixed Effects preferred** — F-test rejects pooled OLS (F=377.1, p<0.0001). Country dummies capture unobserved heterogeneity. β₁ = 3.17 is significant after controlling for country effects.")
            st.markdown("""
**Note on sign reversal:**  
Pooled OLS shows β₁ < 0; Fixed Effects shows β₁ > 0. This Simpson's paradox arises because cross-country differences dominate pooled OLS, while FE reveals the **within-country** time dynamic.
""")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: H4 – YIELD & RISK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💹 H4 – Yield & Risk":
    st.title("H4 – Yield Pickup vs Risk-Adjusted Return")
    st.markdown('<span class="badge-partial">⚠️ Partially Supported | India Sharpe = 1.67 > US | GCC Sharpe = 0.83</span>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Nominal vs Real Yield Comparison (%)</div>', unsafe_allow_html=True)
        yield_plot = pd.DataFrame({
            "Market": ["US", "India", "GCC"],
            "Nominal Yield": [4.5, 7.0, 5.5],
            "Real Yield": [1.5, 1.5, 3.0],
            "Inflation": [3.0, 5.5, 2.5],
        })
        fig = go.Figure()
        for col_name, clr in [("Nominal Yield", PALETTE["US"]), ("Real Yield", PALETTE["India"]), ("Inflation", PALETTE["GCC"])]:
            fig.add_trace(go.Bar(x=yield_plot["Market"], y=yield_plot[col_name],
                name=col_name, marker_color=clr, opacity=0.85))
        fig.update_layout(barmode="group", yaxis_title="% p.a.",
            paper_bgcolor="white", plot_bgcolor="#F5F8FC",
            legend=dict(orientation="h"), height=360,
            yaxis=dict(gridcolor=PALETTE["border"]),
            margin=dict(t=20, b=60, l=50, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Sharpe Ratio & Yield per Unit of Volatility</div>', unsafe_allow_html=True)
        sharpe_data = pd.DataFrame({
            "Market": ["US", "India", "GCC"],
            "Sharpe Ratio": [0, 1.67, 0.83],
            "Yield/Vol": [5.63, 4.67, 4.58],
        })
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=sharpe_data["Market"], y=sharpe_data["Sharpe Ratio"],
            name="Sharpe Ratio", marker_color=[PALETTE["US"], PALETTE["India"], PALETTE["GCC"]],
            opacity=0.85), secondary_y=False)
        fig2.add_trace(go.Scatter(x=sharpe_data["Market"], y=sharpe_data["Yield/Vol"],
            name="Yield/Volatility", mode="lines+markers",
            line=dict(color=PALETTE["GCC"], width=2),
            marker=dict(size=10)), secondary_y=True)
        fig2.update_yaxes(title_text="Sharpe Ratio", secondary_y=False, gridcolor=PALETTE["border"])
        fig2.update_yaxes(title_text="Yield per unit of Vol", secondary_y=True)
        fig2.update_layout(paper_bgcolor="white", plot_bgcolor="#F5F8FC",
            height=360, legend=dict(orientation="h"),
            margin=dict(t=20, b=60, l=50, r=60))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Yield Pickup vs Risk Summary</div>', unsafe_allow_html=True)
    risk_df = pd.DataFrame({
        "Metric": ["10Y Yield (%)", "Yield Volatility (%)", "CPI Inflation (%)", "Real Yield (%)", "Nominal Pickup vs US (bps)", "Real Pickup vs US (bps)", "Sharpe Ratio", "Yield per unit Volatility"],
        "US": ["4.5", "0.80", "3.0", "1.5", "—", "—", "0.00", "5.63"],
        "India": ["7.0", "1.50", "5.5", "1.5", "+250", "≈0", "1.67 ✅", "4.67"],
        "GCC": ["5.5", "1.20", "2.5", "3.0", "+100", "+150", "0.83", "4.58"],
    })
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    st.info("""
**Interpretation:** India's +250 bps nominal pickup over US looks attractive, but real yield parity with US (both ~1.5%) means inflation erodes the advantage. 
GCC shows real yield pickup (+150 bps) with moderate volatility — most attractive on a pure risk-adjusted basis. H4 (yield not proportionally risk-adjusted) is **not rejected** — 
India/GCC actually screen as attractive once Sharpe ratios are computed, although transaction costs and FX hedging costs are not included.
""")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HYPOTHESIS SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧪 Hypothesis Summary":
    st.title("Hypothesis Testing – Summary")
    st.markdown("---")

    # Visual scorecard
    st.markdown('<div class="section-header">Results Scorecard</div>', unsafe_allow_html=True)
    hyp_display = [
        ("H1", "Bond-market / GDP differs across US, India & GCC", "One-way ANOVA", "F = 1,210.99", "< 0.0001", "Reject H₀", "supported", "✅ Strongly Supported"),
        ("H2", "Investor HHI inversely related to liquidity", "Pearson Correlation", "r = −0.87", "0.330", "Fail (n=3)", "partial", "⚠️ Direction Supported"),
        ("H3 (OLS)", "Bank-credit dominance predicts corp-bond size", "Cross-Section OLS", "β₁ = 0.077", "0.543", "Fail to Reject", "notsupported", "❌ Not Supported"),
        ("H3 (FE)", "Bank-credit dominance after country fixed effects", "Panel FE / LSDV", "β₁ = 3.171", "< 0.0001", "Reject H₀ ✅", "supported", "✅ Strongly Supported"),
        ("H4", "EM yield pickup not justified risk-adjusted", "Sharpe Differential", "SR_India=1.67", "n/a", "H₀ not rejected", "partial", "⚠️ Partially Supported"),
    ]
    
    for h, stmt, test, stat, pval, decision, cls, badge in hyp_display:
        with st.container():
            c1, c2, c3, c4 = st.columns([1, 4, 3, 2])
            c1.markdown(f"**{h}**")
            c2.markdown(stmt)
            c3.markdown(f"*{test}* — `{stat}` | p={pval}")
            c4.markdown(f"<span class='badge-{cls}'>{badge}</span>", unsafe_allow_html=True)
            st.markdown('<hr style="margin:0.4rem 0">', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Statistical Power Overview</div>', unsafe_allow_html=True)
        fig = go.Figure()
        hyp_labels = ["H1 (ANOVA)", "H2 (Corr)", "H3-OLS", "H3-FE", "H4 (Sharpe)"]
        p_vals = [0.000001, 0.330, 0.543, 0.000094, None]
        colors_bar = [PALETTE["India"], PALETTE["GCC"], "#C0392B", PALETTE["US"], PALETTE["muted"]]
        sig_vals = [-np.log10(p) if p and p > 0 else 0 for p in p_vals]
        fig.add_trace(go.Bar(x=hyp_labels, y=sig_vals, marker_color=colors_bar, opacity=0.85))
        fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="#C0392B",
                      annotation_text="α=0.05 threshold", annotation_position="top right")
        fig.update_layout(yaxis_title="-log₁₀(p-value)", paper_bgcolor="white",
            plot_bgcolor="#F5F8FC", height=340,
            yaxis=dict(gridcolor=PALETTE["border"]),
            margin=dict(t=20, b=40, l=60, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Limitations & Robustness</div>', unsafe_allow_html=True)
        st.markdown("""
**Current Limitations:**
- H1/H2: only 3 markets → limited statistical power
- H3 cross-section: n=10, outliers (China) distort β
- H4: no FX hedging costs, no bid-ask costs included
- GCC data less granular (primarily issuance, not outstanding)

**Recommended Robustness Checks:**
- Kruskal-Wallis non-parametric test (H1)
- Bootstrapped confidence intervals (H2)
- Wider panel: 20+ OECD+EM markets (H3)
- GARCH-adjusted volatility for Sharpe (H4)
- Exclude COVID year 2020 as sensitivity test

**Data Sources:** BIS · SIFMA · CRISIL · RBI · SEBI · Markaz · OECD · IMF · World Bank
""")
