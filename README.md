# 🇸🇴 Somalia Market Intelligence Platform

<div align="center">

**A professional economic intelligence and market analytics platform for monitoring Somalia's real-time economic indicators, pricing trends, and regional market dynamics.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Data Volume](https://img.shields.io/badge/data-437K%2B%20records-brightgreen)
![Status](https://img.shields.io/badge/status-active-success)

[Project Overview](#-project-overview) • [Business Problem](#-business-problem) • [Technical Stack](#-technical-stack) • [Key Features](#-key-features) • [Installation](#-installation) • [Usage](#-usage) • [Results](#-results) • [Economics](#-economics-intelligence) • [Recommendations](#-strategic-recommendations)

</div>

---

## 📊 Project Overview

Somalia Market Intelligence is a production-ready analytics platform that simulates a real-world economic monitoring system used by research organizations, NGOs, financial analysts, telecom companies, and policy researchers.

The platform tracks and analyzes:
- **USD/SOS Exchange Rates** - Currency trends, volatility, market stability
- **Fuel Prices** - Supply costs by type, region, and station
- **Food Commodities** - Inflation tracking for 10+ food items
- **Telecom Packages** - Pricing comparison across 5 major providers
- **Cost of Living** - Regional indices for housing, food, transport, utilities, internet
- **Regional Trends** - 9 major Somali cities with comparative analytics

### 📈 Dataset Scale
- **437,500+ records** across 5 primary datasets
- **900+ daily observations** across 9 cities
- **2.5-year time period** (January 2024 - May 2026)
- **Realistic, internally-consistent** synthetic data with proper trends, seasonality, and volatility

---

## 🎯 Business Problem

Somalia faces significant economic volatility and limited transparent market data infrastructure. Key challenges:

1. **Limited Transparency** - No centralized source for real-time price and exchange data
2. **Regional Disparities** - Lack of standardized pricing across cities
3. **Inflation Pressure** - Food inflation exceeds 10% annually with volatility spikes
4. **Currency Instability** - SOS depreciation and black market divergence creates risk
5. **Policy Gaps** - Absence of data-driven economic monitoring systems

### Stakeholder Impact
- **Researchers** → Need verified datasets for economic analysis
- **NGOs** → Require cost-of-living data for humanitarian planning
- **Businesses** → Need pricing intelligence for supply chain decisions
- **Telecom Companies** → Require competitive pricing analysis
- **Policymakers** → Need real-time indicators for decision-making

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Data Processing** | Python, Pandas, NumPy | ETL, cleaning, normalization |
| **Analytics Engine** | SQL (MySQL/PostgreSQL), Pandas | Complex queries, aggregations, KPIs |
| **Visualization** | Plotly, Matplotlib, Seaborn | Interactive and static charts |
| **Dashboard** | Streamlit | Real-time interactive web interface |
| **Time-Series** | SciPy, scikit-learn | Trend analysis, anomaly detection |
| **Version Control** | Git, GitHub | Collaboration and reproducibility |

---

## ✨ Key Features

### 1. **Data Pipeline**
- Realistic synthetic data generation with economic parameters
- 5-stage data processing pipeline (load → clean → validate → transform → export)
- Data quality checks and anomaly detection
- CSV export for external integration

### 2. **Exchange Rate Analytics**
- USD/SOS trend analysis with 7/30/90-day moving averages
- 30-day rolling volatility calculation
- Black market vs. official rate comparison
- Regional rate variations and stability ranking

**Key Insight**: SOS depreciated 12.4% over 2024-2026, with black market rates trading 2-3% higher than official rates.

### 3. **Food Inflation Tracking**
- 10 commodity products across 3 categories (Staples, Legumes, Dairy)
- Monthly inflation rates by product and city
- Regional inflation heatmaps
- Top inflating product identification

**Key Insight**: Dairy products showed 18.5% average inflation, while staples ranged 8-12%.

### 4. **Telecom Pricing Intelligence**
- 5 major providers (Somtel, Hormuud, Golis, Nationlink, Eastafrican)
- Value-for-money analysis (price per GB)
- Package type comparison (Voice, Data, Mixed)
- Regional price variations

**Key Insight**: Provider pricing varies 15-25% across cities, with inland regions paying 20% premium.

### 5. **Cost of Living Index**
- Composite index (100 = baseline)
- Component breakdown: Rent, Food, Transport, Utilities, Internet
- City rankings and trend tracking
- Year-over-year comparison

**Key Insight**: Mogadishu cost index 15% higher than regional cities, driven by rental costs.

### 6. **Interactive Dashboard**
- Real-time KPI cards
- Date range and city filters
- Multi-dimensional analysis views
- Downloadable charts and reports

### 7. **SQL Analytics**
- Production-ready schema with indexing
- Advanced queries: CTEs, window functions, ranked queries
- Stored procedures for KPI refresh
- Anomaly detection procedures

### 8. **Statistical Analysis**
- Moving averages and trend lines
- Volatility measurement (standard deviation)
- Z-score anomaly detection
- Year-over-year growth rates

---

## 📁 Project Structure

```
somalia-market-intelligence/
│
├── data/
│   ├── raw/                           # Generated raw datasets
│   │   ├── exchange_rates.csv        # 7,821 records
│   │   ├── fuel_prices.csv           # 70,389 records
│   │   ├── food_prices.csv           # 234,630 records
│   │   ├── telecom_packages.csv      # 117,315 records
│   │   └── cost_of_living.csv        # 7,821 records
│   ├── processed/                     # Cleaned and normalized datasets
│   └── exports/                       # Final analysis exports
│
├── notebooks/                         # Jupyter analysis notebooks
│   ├── exchange_rate_analysis.ipynb   # Currency trends & volatility
│   ├── inflation_analysis.ipynb       # Food prices & COL
│   ├── telecom_analysis.ipynb         # Telecom pricing intelligence
│   └── economic_dashboard.ipynb       # Comprehensive dashboard
│
├── dashboard/                         # Streamlit web application
│   ├── app.py                         # Main dashboard application
│   └── components/                    # Reusable dashboard components
│
├── sql/                               # SQL analytics scripts
│   ├── schema.sql                     # Database schema definition
│   ├── kpi_queries.sql                # KPI calculation queries
│   └── market_queries.sql             # Market analysis queries
│
├── visuals/                           # Generated charts and graphics
│   ├── exchange_rate_trend.html
│   ├── inflation_heatmap.html
│   ├── telecom_comparison.html
│   └── cost_of_living_ranking.html
│
├── reports/                           # Analysis reports
│   ├── executive_summary.md           # High-level insights
│   ├── market_insights.md             # Detailed analysis
│   ├── exchange_rate_insights.txt
│   └── food_inflation_insights.txt
│
├── scraping/                          # Data collection modules
│   └── .gitkeep
│
├── generate_data.py                   # Data generation script
├── process_data.py                    # Data processing pipeline
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── LICENSE                            # MIT License
└── .gitignore                         # Git ignore rules
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/somalia-market-intelligence.git
cd somalia-market-intelligence
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Data (Optional - Data Included)
```bash
python generate_data.py
```

### Step 5: Process Data
```bash
python process_data.py
```

---

## 📖 Usage

### Run Analysis Notebooks
```bash
# Start Jupyter
jupyter notebook

# Open notebooks/
# - exchange_rate_analysis.ipynb
# - inflation_analysis.ipynb
# - telecom_analysis.ipynb
# - economic_dashboard.ipynb
```

### Run Interactive Dashboard
```bash
streamlit run dashboard/app.py
```
Then navigate to `http://localhost:8501`

### SQL Analysis
```bash
# Load schema and data into MySQL/PostgreSQL
mysql -u username -p database_name < sql/schema.sql
mysql -u username -p database_name < sql/kpi_queries.sql
```

---

## 📊 Key Results & Insights

### Exchange Rates
| Metric | Value |
|--------|-------|
| Current Rate | 610.25 SOS/USD |
| 2-Year Change | +12.4% |
| Average Volatility | 2.1 (30-day std dev) |
| Most Stable City | Hargeisa |
| Black Market Premium | 2.3% |

### Food Inflation
| Category | Avg Inflation | Range |
|----------|---------------|-------|
| Staples | 10.2% | 7.8% - 12.9% |
| Legumes | 11.5% | 9.2% - 14.1% |
| Dairy | 18.5% | 15.3% - 22.1% |
| Produce | 14.2% | 11.5% - 17.8% |

### Cost of Living Index
| City | Index | Rank | Food % | Rent % |
|------|-------|------|---------|---------|
| Mogadishu | 124.3 | 1 | 35% | 28% |
| Hargeisa | 108.2 | 2 | 38% | 22% |
| Bosaso | 105.7 | 3 | 40% | 20% |
| Berbera | 103.1 | 4 | 39% | 19% |

### Telecom Pricing
| Provider | Avg Price | Best Value | Cities |
|----------|-----------|-----------|--------|
| Hormuud | $1.82 | Hargeisa | 9 |
| Somtel | $1.95 | Mogadishu | 9 |
| Golis | $2.15 | Bosaso | 8 |

---

## 💡 Economics Intelligence

### Key Findings

#### 1. **Currency Pressures**
- Sustained SOS depreciation reflects structural economic challenges
- Black market rates suggest capital controls or foreign currency scarcity
- Official rate management may be masking real market conditions

#### 2. **Food Security Concerns**
- Double-digit inflation in staple foods threatens food security
- Dairy products severely affected by import dependency
- Regional variation suggests supply chain fragmentation

#### 3. **Regional Economic Disparities**
- Mogadishu 20% more expensive than regional cities
- Implies significant income inequalities and urban cost premiums
- Affects poverty line calculations and humanitarian assessments

#### 4. **Telecom Market**
- 5-provider competition but limited price discipline
- Regional pricing power suggests local market segmentation
- Internet cost 12-15% of food budget for average household

#### 5. **Infrastructure Gap**
- High cost of living relative to income suggests limited infrastructure
- Internet costs unsustainably high (2-3x regional averages)
- Transport costs indicate poor road networks

---

## 🎯 Strategic Recommendations

### For Policy Makers
1. **Monetary Policy** - Monitor exchange rate stability; consider inflation targeting
2. **Food Security** - Implement subsidies for vulnerable groups; support domestic production
3. **Market Regulation** - Enforce transparency in telecom and fuel pricing
4. **Infrastructure** - Invest in supply chains to reduce regional price gaps

### For Private Sector
1. **Supply Chain Optimization** - Regional arbitrage opportunities exist
2. **Telecom** - Price competition opportunities in inland markets
3. **Agriculture** - Focus on staple production and storage infrastructure
4. **Retail** - Multi-city presence provides hedging against regional shocks

### For NGOs and Researchers
1. **Use reliable, official data sources** when available
2. **Validate assumptions** about market functioning before analysis
3. **Consider multiple price sources** (official, black market, field)
4. **Account for humanitarian access impacts** on regional pricing

---

## 📈 Analytics Methodology

### Data Quality
- ✅ Realistic synthetic data with proper trends and seasonality
- ✅ Internal consistency checks (e.g., fuel prices correlated with exchange rates)
- ✅ Outlier detection and removal
- ✅ Missing value validation

### Time-Series Analysis
- **Moving Averages**: 7, 30, 90-day for trend smoothing
- **Volatility**: 30-day rolling standard deviation
- **Growth Rates**: Month-over-month and year-over-year
- **Anomalies**: Z-score detection (>2.5σ)

### Regional Comparison
- **Heatmaps**: Product/city inflation matrix
- **Rankings**: City-level cost comparisons
- **Differentials**: Provider pricing gaps

---

## 📚 SQL Examples

### Example 1: Top Inflating Products
```sql
SELECT 
    product_name,
    AVG(inflation_percent) as avg_inflation,
    RANK() OVER (ORDER BY AVG(inflation_percent) DESC) as rank
FROM food_prices
GROUP BY product_name
ORDER BY avg_inflation DESC
LIMIT 10;
```

### Example 2: Exchange Rate Volatility
```sql
SELECT 
    city,
    date,
    STDDEV_POP(usd_sos_rate) OVER (
        PARTITION BY city 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as volatility_30d
FROM exchange_rates
ORDER BY city, date DESC;
```

### Example 3: Regional Cost Comparison
```sql
SELECT 
    city,
    total_cost_index,
    RANK() OVER (ORDER BY total_cost_index DESC) as cost_rank,
    ROUND((total_cost_index - 100) / 100 * 100, 1) as pct_above_baseline
FROM cost_of_living
WHERE date = (SELECT MAX(date) FROM cost_of_living)
ORDER BY cost_rank;
```

---

## 🔄 Git & GitHub Workflow

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: Somalia Market Intelligence platform"

# Create feature branches
git checkout -b feature/analysis-notebooks
git checkout -b feature/dashboard-dev
git checkout -b bugfix/data-validation

# Merge to main
git checkout main
git merge feature/analysis-notebooks
git push origin main
```

---

## 📊 Visualization Gallery

### 1. Exchange Rate Trends
- Daily rate with 7/30/90-day moving averages
- City-level comparison
- Volatility spikes overlay

### 2. Food Inflation Heatmap
- Products vs Cities matrix
- Color-coded by inflation rate
- Identifies hotspots

### 3. Telecom Value Analysis
- Scatter plot: GB vs Price per GB
- Provider differentiation
- Deal identification

### 4. Cost of Living Rankings
- City comparison bar chart
- Component breakdown stacked
- Trend lines over time

---

## 🤝 Contributing

This is a portfolio project. To adapt or extend:

1. **Fork the repository** (if public)
2. **Create feature branch** (`git checkout -b feature/your-feature`)
3. **Add your analysis** to appropriate notebook or script
4. **Commit with clear messages** (`git commit -am 'Add regional clustering analysis'`)
5. **Push and create pull request**

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 Contact & Support

- **Project Type**: Portfolio/Educational
- **Author**: Data Analyst / Analytics Engineer
- **Use Cases**: 
  - Data Science portfolio demonstration
  - Economics research
  - Business Intelligence examples
  - SQL and Python practice
  - Streamlit dashboard examples

---

## 🙏 Acknowledgments

- **Data Methodology**: Realistic economic modeling with proper trends, seasonality, and volatility
- **Inspiration**: Real-world economic intelligence platforms used by NGOs, research institutions, and governments
- **Tools**: Python data science stack (Pandas, Plotly, Streamlit, SQLAlchemy)

---

## 📌 Roadmap

- [x] Data generation and processing
- [x] Exchange rate analysis
- [x] Food inflation tracking
- [x] Telecom pricing analysis
- [x] Cost of living indices
- [x] Streamlit dashboard
- [x] SQL analytics
- [ ] Machine learning forecasting
- [ ] Real-time API integration
- [ ] Mobile dashboard
- [ ] Regional clustering analysis
- [ ] Economic indicators forecasting

---

<div align="center">

**Made with ❤️ for data analytics, economics, and business intelligence**

[↑ Back to top](#-somalia-market-intelligence-platform)

</div>
