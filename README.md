# Somalia Market Intelligence Platform

A comprehensive data analytics platform for monitoring economic indicators across Somalia. Provides real-time insights into currency exchange rates, food inflation, telecommunications pricing, fuel costs, and cost of living indices across major Somali cities.

## Overview

This platform synthesizes economic data from multiple sources to create a unified intelligence system for understanding market dynamics in Somalia. It features interactive dashboards, statistical analysis notebooks, and automated data processing pipelines.

**Key Statistics:**
- **437,500+** economic data points
- **9** major Somali cities covered
- **2.5+ years** of historical data (Jan 2024 - May 2026)
- **5** economic indicators tracked

## Features

### 📊 Interactive Dashboard
- Real-time market indicators and KPIs
- Multi-dimensional filtering by city, date range, and metrics
- Interactive Plotly visualizations
- Professional styling with responsive design

### 📈 Economic Indicators Tracked
1. **USD/SOS Exchange Rates** - Currency valuation trends and volatility
2. **Food Inflation** - Price trends for essential commodities
3. **Fuel Prices** - Petrol, diesel, and kerosene cost tracking
4. **Telecom Pricing** - Mobile data packages and carrier pricing
5. **Cost of Living** - Composite indices by city and category

### 🔍 Analysis Notebooks
- **Exchange Rate Analysis** - Trend analysis, volatility assessment, market type comparison
- **Inflation Analysis** - Regional price variations, inflation rates by category
- **Economic Dashboard** - Comprehensive overview of all indicators
- **Telecom Analysis** - Market segmentation, pricing strategies, provider comparison

### 🛠️ Automated Pipelines
- Data generation with realistic economic modeling
- Synthetic data generation for consistent analysis
- Data processing and normalization
- Visualization export functionality

## Project Structure

```
somalia-market-intelligence/
├── data/
│   ├── raw/                 # Original unprocessed datasets
│   ├── processed/           # Cleaned and normalized data
│   └── exports/             # Data export outputs
├── notebooks/               # Jupyter analysis notebooks
│   ├── exchange_rate_analysis.ipynb
│   ├── inflation_analysis.ipynb
│   ├── economic_dashboard.ipynb
│   └── telecom_analysis.ipynb
├── dashboard/               # Streamlit dashboard application
│   ├── app.py              # Main dashboard
│   └── components/         # Reusable UI components
├── sql/                     # Database schemas and queries
├── visuals/                 # Exported HTML visualizations
├── reports/                 # Analysis reports and summaries
├── generate_data.py         # Synthetic data generation
├── process_data.py          # Data pipeline and ETL
├── generate_visuals.py      # Visualization export utility
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Alibaash/Somalia-Market-Intelligence.git
   cd Somalia-Market-Intelligence
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Dashboard

Start the interactive Streamlit dashboard:
```bash
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501` and provides:
- Real-time KPI metrics
- Multi-view analysis (Exchange Rates, Food Inflation, Telecom, Cost of Living)
- Regional comparison tools
- Date range filtering
- City-level segmentation

### Running Analysis Notebooks

Open and execute Jupyter notebooks for detailed analysis:
```bash
jupyter notebook notebooks/exchange_rate_analysis.ipynb
```

Available notebooks:
- **exchange_rate_analysis.ipynb** - USD/SOS trends, volatility, market analysis
- **inflation_analysis.ipynb** - Price trends and inflation calculations
- **economic_dashboard.ipynb** - Comprehensive economic overview
- **telecom_analysis.ipynb** - Telecom market segmentation

### Data Processing

Generate and process data:
```bash
python generate_data.py    # Generate synthetic data
python process_data.py     # Process and normalize data
python generate_visuals.py # Export visualizations
```

## Dataset

### Data Coverage
- **Time Period:** January 1, 2024 - May 18, 2026
- **Cities:** Mogadishu, Hargeisa, Bosaso, Kismayo, Garowe, Baidoa, Beledweyne, Galkayo, Berbera
- **Frequency:** Daily observations

### Data Files

| File | Records | Size | Description |
|------|---------|------|-------------|
| exchange_rates.csv | 120,000 | 657 KB | Daily USD/SOS rates by city and market type |
| food_prices.csv | 200,000 | 15 MB | Daily food commodity prices |
| fuel_prices.csv | 60,000 | 3.7 MB | Daily fuel prices by type |
| telecom_packages.csv | 50,000 | 7.3 MB | Telecom package pricing and details |
| cost_of_living.csv | 7,500 | 505 KB | Cost of living indices by category |

### Data Processing

Data flows through the following pipeline:
1. **Raw Data** (`data/raw/`) - Original datasets
2. **Processing** (`process_data.py`) - Cleaning, normalization, aggregation
3. **Processed Data** (`data/processed/`) - Analysis-ready datasets
4. **Visualization** (`generate_visuals.py`) - HTML exports
5. **Reports** (`reports/`) - Exported insights and summaries

## Technology Stack

**Data Processing:**
- pandas - Data manipulation and analysis
- numpy - Numerical computing

**Visualization:**
- Plotly - Interactive charts
- Matplotlib & Seaborn - Statistical plots

**Web Framework:**
- Streamlit - Rapid dashboard development

**Database:**
- SQLAlchemy - ORM and database toolkit

**Data Tools:**
- BeautifulSoup4 - Web scraping
- Scikit-learn - Data preprocessing and analysis

## Architecture

### Dashboard Architecture
The Streamlit dashboard (`dashboard/app.py`) provides:
- Cached data loading for performance
- Sidebar filters for dynamic analysis
- Multiple metric views with conditional rendering
- Real-time KPI calculations

### Data Pipeline
1. Raw data ingestion
2. Data validation and cleaning
3. Feature engineering and aggregations
4. Normalization and standardization
5. Output to processed datasets

### Notebook Analysis
Jupyter notebooks provide:
- Exploratory data analysis
- Statistical analysis and insights
- Time-series trend analysis
- Regional and category-level comparisons

## Key Insights

The platform enables analysis of:
- **Currency Trends** - USD/SOS depreciation patterns across cities
- **Inflation Dynamics** - Food price inflation by category and region
- **Market Segmentation** - Black market vs. official rate differentials
- **Telecom Competition** - Pricing strategies by provider and region
- **Regional Variations** - Economic differences across Somali cities

## Performance Optimization

- **Data Caching** - Streamlit cache decorator for efficient data loading
- **Vectorized Operations** - NumPy for fast computations
- **Lazy Loading** - On-demand data filtering
- **CSV Storage** - Efficient columnar storage format

## Version History

- **v1.0** - Initial release with core indicators
- Current version includes full economic indicator suite

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Contact

**Developer:** Alibaash

For inquiries or collaboration opportunities, please visit the project repository.

---

**Last Updated:** May 25, 2026

*Somalia Market Intelligence - Making economic data accessible and actionable*