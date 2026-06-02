# Fixed-Income Market Disparities Dashboard
**Author:** Rishika Jain (MS25GF037) | SP Jain School of Global Management  
**Research:** Comparative Analysis of US, India & GCC Fixed-Income Markets (2018–2024)

## 🚀 Deploy on Streamlit Community Cloud

1. **Fork / push this repo to GitHub**
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Select your repo, branch `main`, file `app.py`
4. Click **Deploy**

## 📁 Project Structure
```
├── app.py                          # Main Streamlit dashboard
├── requirements.txt                # Python dependencies
├── data/
│   ├── bond_market_size.csv        # Bond/GDP time-series (2018–2024)
│   ├── liquidity_indicators.csv    # Turnover, spreads, ADV (2024)
│   ├── investor_composition.csv    # Investor base breakdown
│   ├── structural_indicators.csv   # Bank credit, yields, HHI
│   ├── cross_country_h3.csv        # H3 cross-section (n=10 countries)
│   ├── panel_regression.csv        # H3 panel data (3×7 country-years)
│   ├── hypothesis_summary.csv      # All H1–H4 test results
│   └── yield_risk.csv              # H4 yield & Sharpe analysis
└── README.md
```

## 🏃 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Dashboard Sections
| Section | Content |
|---|---|
| 🏠 Overview | KPIs, bond trends, investor pie charts, key findings |
| 📈 H1 | ANOVA, bond/GDP time-series, GCC issuance growth, liquidity |
| 👥 H2 | HHI concentration, investor composition, HHI vs turnover scatter |
| 🏦 H3 | Cross-section OLS scatter, panel fixed-effects results |
| 💹 H4 | Yield comparison, Sharpe ratios, risk-adjusted analysis |
| 🧪 Summary | Full hypothesis scorecard, -log₁₀(p) chart, limitations |

## 📚 Data Sources
BIS · IMF · World Bank · SIFMA · CRISIL · RBI · SEBI · Markaz · OECD · US Treasury TIC · HSBC Asset Management
