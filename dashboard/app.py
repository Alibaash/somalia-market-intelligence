"""
Somalia Market Intelligence - Streamlit Dashboard
Interactive analytics platform for monitoring economic indicators
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Somalia Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all processed datasets"""
    data_dir = 'data/processed'
    datasets = {}
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            key = filename.replace('.csv', '')
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            datasets[key] = df
    
    return datasets

# Load datasets
datasets = load_data()
df_rates = datasets.get('exchange_rates', pd.DataFrame())
df_food = datasets.get('food_prices', pd.DataFrame())
df_fuel = datasets.get('fuel_prices', pd.DataFrame())
df_telecom = datasets.get('telecom_packages', pd.DataFrame())
df_col = datasets.get('cost_of_living', pd.DataFrame())

# Sidebar filters
st.sidebar.markdown("# 🇸🇴 Somalia Market Intelligence")
st.sidebar.markdown("---")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime(2026, 4, 18), datetime(2026, 5, 18)),
    max_value=datetime(2026, 5, 18),
    min_value=datetime(2024, 1, 1)
)

# City selector
cities = sorted(df_rates['city'].unique().tolist()) if len(df_rates) > 0 else []
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    cities,
    default=cities[:3] if cities else []
)

# Metric selector
metrics = st.sidebar.selectbox(
    "Select Analysis View",
    ["Dashboard", "Exchange Rates", "Food Inflation", "Telecom Pricing", "Cost of Living", "Regional Comparison"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Period:** 2024-01-01 to 2026-05-18")
st.sidebar.markdown("**Total Records:** 437,500+")

# Filter data based on selections
start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])
date_mask_start = lambda df: df['date'] >= pd.Timestamp(start_date) if 'date' in df.columns else True
date_mask_end = lambda df: df['date'] <= pd.Timestamp(end_date) if 'date' in df.columns else True
city_mask = lambda df: df['city'].isin(selected_cities) if 'city' in df.columns else True

# ============================================================
# MAIN DASHBOARD
# ============================================================

if metrics == "Dashboard":
    st.markdown("# 📊 Somalia Market Intelligence Dashboard")
    st.markdown("*Real-time economic monitoring and market analysis*")
    st.markdown("---")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Exchange Rate KPI
    with col1:
        if len(df_rates) > 0:
            latest_rate = df_rates[df_rates['date'] == df_rates['date'].max()]['usd_sos_rate'].mean()
            st.metric(
                "📱 USD/SOS Rate",
                f"{latest_rate:.2f}",
                delta=f"{df_rates['daily_change_percent'].mean():.3f}%"
            )
    
    # Food Inflation KPI
    with col2:
        if len(df_food) > 0:
            avg_inflation = df_food['inflation_percent'].mean()
            st.metric(
                "🍜 Avg Food Inflation",
                f"{avg_inflation:.2f}%",
                delta="+0.5%" if avg_inflation > 0 else "-0.5%"
            )
    
    # Telecom Price KPI
    with col3:
        if len(df_telecom) > 0:
            avg_telecom = df_telecom[df_telecom['date'] == df_telecom['date'].max()]['package_price_usd'].mean()
            st.metric(
                "📡 Avg Telecom Price",
                f"${avg_telecom:.2f}",
                delta="-5%"
            )
    
    # Cost of Living KPI
    with col4:
        if len(df_col) > 0:
            latest_col = df_col[df_col['date'] == df_col['date'].max()]['total_cost_index'].mean()
            st.metric(
                "💰 Cost of Living",
                f"{latest_col:.0f}",
                delta="+2.3%"
            )
    
    st.markdown("---")
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        if len(df_rates) > 0:
            st.subheader("Exchange Rate Trend")
            daily_rates = df_rates[(df_rates['date'] >= pd.Timestamp(start_date)) & 
                                   (df_rates['date'] <= pd.Timestamp(end_date))].groupby('date')['usd_sos_rate'].mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_rates.index, y=daily_rates.values, mode='lines', fill='tozeroy'))
            fig.update_layout(height=350, template='plotly_white', hovermode='x unified')
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        if len(df_food) > 0:
            st.subheader("Top Inflating Products")
            top_products = df_food.groupby('product_name')['inflation_percent'].mean().nlargest(5)
            
            fig = px.bar(y=top_products.index, x=top_products.values, orientation='h', 
                        color=top_products.values, color_continuous_scale='RdYlGn_r')
            fig.update_layout(height=350, template='plotly_white', showlegend=False)
            st.plotly_chart(fig, width='stretch')
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(df_col) > 0:
            st.subheader("Cost of Living by City")
            latest_col = df_col[df_col['date'] == df_col['date'].max()]
            city_costs = latest_col.sort_values('total_cost_index', ascending=False)
            
            fig = px.bar(city_costs, x='total_cost_index', y='city', orientation='h',
                        color='total_cost_index', color_continuous_scale='Viridis')
            fig.update_layout(height=350, template='plotly_white', showlegend=False)
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        if len(df_telecom) > 0:
            st.subheader("Telecom Pricing by Provider")
            latest_telecom = df_telecom[df_telecom['date'] == df_telecom['date'].max()]
            provider_prices = latest_telecom.groupby('provider')['package_price_usd'].mean().sort_values()
            
            fig = px.bar(x=provider_prices.values, y=provider_prices.index, orientation='h',
                        color=provider_prices.values, color_continuous_scale='Blues')
            fig.update_layout(height=350, template='plotly_white', showlegend=False)
            st.plotly_chart(fig, width='stretch')

# ============================================================
# EXCHANGE RATES ANALYSIS
# ============================================================

elif metrics == "Exchange Rates":
    st.markdown("# 📱 Exchange Rate Analysis")
    st.markdown("*USD/SOS trends, volatility, and regional variations*")
    
    filtered_rates = df_rates[(df_rates['date'] >= pd.Timestamp(start_date)) & 
                             (df_rates['date'] <= pd.Timestamp(end_date)) &
                             (df_rates['city'].isin(selected_cities))]
    
    if len(filtered_rates) > 0:
        # Trend chart
        st.subheader("Exchange Rate Trends by City")
        daily_city_rates = filtered_rates.groupby(['date', 'city'])['usd_sos_rate'].mean().reset_index()
        
        fig = px.line(daily_city_rates, x='date', y='usd_sos_rate', color='city', markers=True)
        fig.update_layout(height=400, template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig, width='stretch')
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Rate", f"{filtered_rates['usd_sos_rate'].mean():.2f} SOS/USD")
        with col2:
            st.metric("Max Rate", f"{filtered_rates['usd_sos_rate'].max():.2f}")
        with col3:
            st.metric("Min Rate", f"{filtered_rates['usd_sos_rate'].min():.2f}")
        with col4:
            st.metric("Volatility", f"{filtered_rates['usd_sos_rate'].std():.4f}")
        
        # Regional breakdown
        st.subheader("Exchange Rate Statistics by City")
        city_stats = filtered_rates.groupby('city')['usd_sos_rate'].agg(['mean', 'std', 'min', 'max']).round(2)
        st.dataframe(city_stats, width='stretch')

# ============================================================
# FOOD INFLATION ANALYSIS
# ============================================================

elif metrics == "Food Inflation":
    st.markdown("# 🍜 Food Inflation Analysis")
    st.markdown("*Commodity prices, inflation trends, and regional comparisons*")
    
    filtered_food = df_food[(df_food['date'] >= pd.Timestamp(start_date)) & 
                            (df_food['date'] <= pd.Timestamp(end_date)) &
                            (df_food['city'].isin(selected_cities))]
    
    if len(filtered_food) > 0:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Top Inflating Products")
            top_inflation = filtered_food.groupby('product_name')['inflation_percent'].mean().nlargest(10)
            
            fig = px.bar(y=top_inflation.index, x=top_inflation.values, orientation='h',
                        color=top_inflation.values, color_continuous_scale='RdYlGn_r')
            fig.update_layout(height=400, template='plotly_white', showlegend=False)
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            st.subheader("Inflation by Category")
            category_inflation = filtered_food.groupby('category')['inflation_percent'].mean().sort_values(ascending=False)
            
            fig = px.pie(values=category_inflation.values, names=category_inflation.index)
            fig.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig, width='stretch')
        
        # Price trends
        st.subheader("Product Price Trends")
        selected_products = st.multiselect(
            "Select products to track",
            sorted(filtered_food['product_name'].unique()),
            default=list(sorted(filtered_food['product_name'].unique()))[:3]
        )
        
        if selected_products:
            product_trends = filtered_food[filtered_food['product_name'].isin(selected_products)]
            monthly_prices = product_trends.groupby([pd.Grouper(key='date', freq='ME'), 'product_name'])['price_usd'].mean().reset_index()
            
            fig = px.line(monthly_prices, x='date', y='price_usd', color='product_name', markers=True)
            fig.update_layout(height=400, template='plotly_white', hovermode='x unified')
            st.plotly_chart(fig, width='stretch')

# ============================================================
# TELECOM PRICING ANALYSIS
# ============================================================

elif metrics == "Telecom Pricing":
    st.markdown("# 📡 Telecom & Internet Pricing Analysis")
    st.markdown("*Provider comparison, value analysis, and pricing trends*")
    
    filtered_telecom = df_telecom[(df_telecom['date'] >= pd.Timestamp(start_date)) & 
                                  (df_telecom['date'] <= pd.Timestamp(end_date)) &
                                  (df_telecom['city'].isin(selected_cities))]
    
    if len(filtered_telecom) > 0:
        # Provider comparison
        st.subheader("Provider Pricing Comparison")
        latest_telecom = filtered_telecom[filtered_telecom['date'] == filtered_telecom['date'].max()]
        provider_avg = latest_telecom.groupby('provider')['package_price_usd'].mean().sort_values()
        
        fig = px.bar(x=provider_avg.values, y=provider_avg.index, orientation='h',
                    color=provider_avg.values, color_continuous_scale='Viridis')
        fig.update_layout(height=300, template='plotly_white', showlegend=False)
        st.plotly_chart(fig, width='stretch')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Package Type Distribution")
            package_dist = latest_telecom['package_type'].value_counts()
            
            fig = px.pie(values=package_dist.values, names=package_dist.index)
            fig.update_layout(height=350, template='plotly_white')
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            st.subheader("Value for Money (Price per GB)")
            value_analysis = filtered_telecom[filtered_telecom['data_gb'] > 0].copy()
            value_analysis['price_per_gb'] = value_analysis['package_price_usd'] / value_analysis['data_gb']
            provider_value = value_analysis.groupby('provider')['price_per_gb'].mean().sort_values()
            
            fig = px.bar(x=provider_value.values, y=provider_value.index, orientation='h',
                        color=provider_value.values, color_continuous_scale='RdYlGn_r')
            fig.update_layout(height=350, template='plotly_white', showlegend=False)
            st.plotly_chart(fig, width='stretch')

# ============================================================
# COST OF LIVING
# ============================================================

elif metrics == "Cost of Living":
    st.markdown("# 💰 Cost of Living Index")
    st.markdown("*Housing, food, transport, utilities, and internet costs*")
    
    filtered_col = df_col[(df_col['date'] >= pd.Timestamp(start_date)) & 
                          (df_col['date'] <= pd.Timestamp(end_date)) &
                          (df_col['city'].isin(selected_cities))]
    
    if len(filtered_col) > 0:
        # City ranking
        st.subheader("Cost of Living Index by City (Latest)")
        latest_col = filtered_col[filtered_col['date'] == filtered_col['date'].max()]
        city_costs = latest_col.sort_values('total_cost_index', ascending=False)
        
        fig = px.bar(city_costs, x='total_cost_index', y='city', orientation='h',
                    color='total_cost_index', color_continuous_scale='Plasma')
        fig.update_layout(height=350, template='plotly_white', showlegend=False)
        st.plotly_chart(fig, width='stretch')
        
        # Component breakdown
        st.subheader("Cost Components by City")
        components = ['food_index', 'rent_index', 'transport_index', 'utilities_index', 'internet_index']
        
        fig = go.Figure(data=[
            go.Bar(name='Food', x=city_costs['city'], y=city_costs['food_index']),
            go.Bar(name='Rent', x=city_costs['city'], y=city_costs['rent_index']),
            go.Bar(name='Transport', x=city_costs['city'], y=city_costs['transport_index']),
            go.Bar(name='Utilities', x=city_costs['city'], y=city_costs['utilities_index']),
            go.Bar(name='Internet', x=city_costs['city'], y=city_costs['internet_index'])
        ])
        
        fig.update_layout(barmode='stack', height=400, template='plotly_white')
        st.plotly_chart(fig, width='stretch')

# ============================================================
# REGIONAL COMPARISON
# ============================================================

elif metrics == "Regional Comparison":
    st.markdown("# 🗺️ Regional Comparison")
    st.markdown("*Economic indicators across Somalia's major cities*")
    
    if len(selected_cities) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            if len(df_rates) > 0:
                st.subheader("Exchange Rates by City (Latest)")
                latest_rates = df_rates[df_rates['date'] == df_rates['date'].max()]
                latest_rates = latest_rates[latest_rates['city'].isin(selected_cities)]
                
                fig = px.bar(latest_rates.sort_values('usd_sos_rate', ascending=False),
                            x='usd_sos_rate', y='city', orientation='h')
                fig.update_layout(height=350, template='plotly_white', showlegend=False)
                st.plotly_chart(fig, width='stretch')
        
        with col2:
            if len(df_col) > 0:
                st.subheader("Cost of Living by City (Latest)")
                latest_col = df_col[df_col['date'] == df_col['date'].max()]
                latest_col = latest_col[latest_col['city'].isin(selected_cities)]
                
                fig = px.bar(latest_col.sort_values('total_cost_index', ascending=False),
                            x='total_cost_index', y='city', orientation='h')
                fig.update_layout(height=350, template='plotly_white', showlegend=False)
                st.plotly_chart(fig, width='stretch')

# Footer
st.markdown("---")
st.markdown("""
*Somalia Market Intelligence Platform - Economic Monitoring Dashboard*
| Data Period: 2024-2026 | Last Updated: May 2026 | v1.0
""")
