"""
Generate core visualizations for the Somalia Market Intelligence project.
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = 'data/processed'
VISUAL_DIR = 'visuals'

os.makedirs(VISUAL_DIR, exist_ok=True)

# Load processed data
exchange_rates = pd.read_csv(os.path.join(DATA_DIR, 'exchange_rates.csv'), parse_dates=['date'])
fuel = pd.read_csv(os.path.join(DATA_DIR, 'fuel_prices.csv'), parse_dates=['date'])
food = pd.read_csv(os.path.join(DATA_DIR, 'food_prices.csv'), parse_dates=['date'])
telecom = pd.read_csv(os.path.join(DATA_DIR, 'telecom_packages.csv'), parse_dates=['date'])
cost_of_living = pd.read_csv(os.path.join(DATA_DIR, 'cost_of_living.csv'), parse_dates=['date'])

# 1. Exchange rate trend
exchange_avg = exchange_rates.groupby('date')['usd_sos_rate'].mean().reset_index()
fig = px.line(exchange_avg, x='date', y='usd_sos_rate', title='Average USD/SOS Exchange Rate')
fig.write_html(os.path.join(VISUAL_DIR, 'exchange_rate_trend.html'))

# 2. Exchange market type comparison
market_rates = exchange_rates.groupby(['date', 'market_type'])['usd_sos_rate'].mean().reset_index()
fig = px.line(market_rates, x='date', y='usd_sos_rate', color='market_type', title='Official vs Black Market Exchange Rates')
fig.write_html(os.path.join(VISUAL_DIR, 'exchange_rate_market_type.html'))

# 3. Top inflating food products
product_inflation = food.groupby('product_name')['inflation_percent'].mean().sort_values(ascending=False).reset_index()
fig = px.bar(product_inflation.head(10), x='inflation_percent', y='product_name', orientation='h', title='Top 10 Food Inflation Products')
fig.write_html(os.path.join(VISUAL_DIR, 'top_inflating_products.html'))

# 4. Food inflation heatmap
pivot_food = food.pivot_table(values='inflation_percent', index='product_name', columns='city', aggfunc='mean')
fig = go.Figure(data=go.Heatmap(z=pivot_food.values, x=pivot_food.columns, y=pivot_food.index, colorscale='RdYlGn_r'))
fig.update_layout(title='Food Inflation Heatmap', height=600)
fig.write_html(os.path.join(VISUAL_DIR, 'food_inflation_heatmap.html'))

# 5. Cost of living by city
latest_col = cost_of_living.loc[cost_of_living.groupby('city')['date'].idxmax()]
fig = px.bar(latest_col.sort_values('total_cost_index', ascending=False), x='total_cost_index', y='city', orientation='h', title='Latest Cost of Living Index by City')
fig.write_html(os.path.join(VISUAL_DIR, 'cost_of_living_by_city.html'))

# 6. Telecom provider average pricing
telecom_latest = telecom[telecom['date'] == telecom['date'].max()]
provider_avg = telecom_latest.groupby('provider')['package_price_usd'].mean().reset_index().sort_values('package_price_usd')
fig = px.bar(provider_avg, x='package_price_usd', y='provider', orientation='h', title='Average Telecom Price by Provider')
fig.write_html(os.path.join(VISUAL_DIR, 'telecom_price_by_provider.html'))

print('✅ Visualizations generated in visuals/')
