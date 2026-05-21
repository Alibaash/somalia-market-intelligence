"""
Somalia Market Intelligence - Synthetic Data Generation
Generates realistic, internally-consistent datasets for Somalia economic monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

CITIES = ['Mogadishu', 'Hargeisa', 'Bosaso', 'Kismayo', 'Garowe', 
          'Baidoa', 'Beledweyne', 'Galkayo', 'Berbera']

DATE_RANGE = pd.date_range(start='2024-01-01', end='2026-05-18', freq='D')

# Base economic parameters by city (for realistic variation)
CITY_PARAMS = {
    'Mogadishu': {'inflation_base': 0.12, 'stability': 0.85, 'market_type': 'black/official'},
    'Hargeisa': {'inflation_base': 0.08, 'stability': 0.88, 'market_type': 'official'},
    'Bosaso': {'inflation_base': 0.10, 'stability': 0.86, 'market_type': 'black'},
    'Berbera': {'inflation_base': 0.09, 'stability': 0.87, 'market_type': 'official'},
    'Kismayo': {'inflation_base': 0.14, 'stability': 0.80, 'market_type': 'black'},
    'Garowe': {'inflation_base': 0.11, 'stability': 0.83, 'market_type': 'mixed'},
    'Baidoa': {'inflation_base': 0.13, 'stability': 0.82, 'market_type': 'black'},
    'Beledweyne': {'inflation_base': 0.12, 'stability': 0.84, 'market_type': 'mixed'},
    'Galkayo': {'inflation_base': 0.11, 'stability': 0.84, 'market_type': 'mixed'},
}

def generate_exchange_rates():
    """Generate USD/SOS exchange rate data"""
    records = []
    
    # Base rate starts at 580 SOS/USD (realistic for 2024)
    base_rate = 580
    
    for city in CITIES:
        rate = base_rate
        params = CITY_PARAMS[city]
        
        for date in DATE_RANGE:
            # Add trend (gradual depreciation over time)
            trend = (date - DATE_RANGE[0]).days * 0.02  # ~7.3 SOS/USD increase per year
            
            # Add seasonality (Q3 tends to be more volatile)
            seasonality = 5 * np.sin(2 * np.pi * date.dayofyear / 365)
            
            # Add random walk with volatility
            random_shock = np.random.normal(0, 2)
            
            # Occasional larger shocks (market disruptions)
            if np.random.random() < 0.01:
                random_shock *= 3
            
            rate = rate + trend/len(DATE_RANGE) + seasonality/len(DATE_RANGE) + random_shock
            
            # City-specific variation
            city_variation = np.random.normal(0, 1) * params['stability']
            rate += city_variation
            
            # Rate should stay reasonable (between 550-650)
            rate = max(550, min(650, rate))
            
            daily_change = ((rate - (rate - random_shock - trend/len(DATE_RANGE))) / 
                          (rate - random_shock - trend/len(DATE_RANGE)) * 100) if rate > 0 else 0
            
            records.append({
                'date': date,
                'city': city,
                'usd_sos_rate': round(rate, 2),
                'daily_change_percent': round(daily_change, 3),
                'market_type': params['market_type'],
                'source': 'Central Bank' if params['market_type'] == 'official' else 'Black Market'
            })
    
    return pd.DataFrame(records)

def generate_fuel_prices():
    """Generate fuel price data"""
    records = []
    
    fuel_types = ['Petrol', 'Diesel', 'Kerosene']
    station_types = ['Private Station', 'Government Station', 'Black Market']
    
    # Base prices USD/liter (realistic for Somalia)
    base_prices = {
        'Petrol': 0.85,
        'Diesel': 0.78,
        'Kerosene': 0.65
    }
    
    for city in CITIES:
        params = CITY_PARAMS[city]
        
        for fuel in fuel_types:
            base_price = base_prices[fuel]
            price = base_price
            
            for date in DATE_RANGE:
                # Global oil price trend (slight increase over period)
                global_trend = (date - DATE_RANGE[0]).days * 0.0001
                
                # Seasonal variation (higher in dry seasons)
                seasonality = 0.05 * np.sin(2 * np.pi * date.dayofyear / 365)
                
                # Random walk
                random_shock = np.random.normal(0, 0.02)
                
                price = price + global_trend + seasonality/len(DATE_RANGE) + random_shock
                price = max(0.50, min(1.20, price))  # Keep in reasonable range
                
                # Calculate SOS price (using exchange rate)
                sos_price = price * np.random.uniform(600, 620)  # Approximate exchange rate
                
                for station_type in station_types:
                    # Price variations by station type
                    if station_type == 'Government Station':
                        station_price = price * 0.95  # Slightly cheaper
                    elif station_type == 'Black Market':
                        station_price = price * 1.10  # More expensive
                    else:
                        station_price = price
                    
                    records.append({
                        'date': date,
                        'city': city,
                        'fuel_type': fuel,
                        'fuel_price_usd': round(station_price, 3),
                        'fuel_price_sos': round(station_price * sos_price / price, 2),
                        'station_type': station_type
                    })
    
    return pd.DataFrame(records)

def generate_food_prices():
    """Generate food commodity price data"""
    records = []
    
    commodities = {
        'Rice': {'unit': 'kg', 'base_price': 0.80, 'category': 'Staple'},
        'Flour': {'unit': 'kg', 'base_price': 0.60, 'category': 'Staple'},
        'Sugar': {'unit': 'kg', 'base_price': 1.20, 'category': 'Staple'},
        'Oil': {'unit': 'liter', 'base_price': 1.50, 'category': 'Staple'},
        'Beans': {'unit': 'kg', 'base_price': 0.90, 'category': 'Legume'},
        'Maize': {'unit': 'kg', 'base_price': 0.55, 'category': 'Staple'},
        'Milk (Powder)': {'unit': 'kg', 'base_price': 4.50, 'category': 'Dairy'},
        'Banana': {'unit': 'kg', 'base_price': 0.40, 'category': 'Fruit'},
        'Onion': {'unit': 'kg', 'base_price': 0.35, 'category': 'Vegetable'},
        'Tomato': {'unit': 'kg', 'base_price': 0.45, 'category': 'Vegetable'},
    }
    
    supplier_types = ['Wholesale', 'Retail', 'Market Vendor']
    
    for city in CITIES:
        params = CITY_PARAMS[city]
        inflation_base = params['inflation_base']
        
        for product, info in commodities.items():
            price = info['base_price']
            
            for date in DATE_RANGE:
                # Inflation trend
                inflation_trend = inflation_base / 365  # Daily inflation rate
                
                # Seasonal variation (higher during off-season)
                if product in ['Banana', 'Tomato', 'Onion']:
                    seasonality = 0.15 * np.sin(2 * np.pi * date.dayofyear / 365)
                else:
                    seasonality = 0.08 * np.sin(2 * np.pi * date.dayofyear / 365)
                
                # Random walk
                random_shock = np.random.normal(0, 0.02)
                
                # Apply cumulative inflation
                price = price * (1 + inflation_trend + seasonality/len(DATE_RANGE) + random_shock)
                
                # Calculate inflation percent
                base_year_price = info['base_price'] * (1 + inflation_base * 
                                 ((date - DATE_RANGE[0]).days / 365))
                inflation_pct = ((price - base_year_price) / base_year_price * 100) if base_year_price > 0 else 0
                
                for supplier in supplier_types:
                    # Markup by supplier type
                    if supplier == 'Wholesale':
                        supplier_price = price * 0.92
                    elif supplier == 'Market Vendor':
                        supplier_price = price * 1.15
                    else:
                        supplier_price = price
                    
                    records.append({
                        'date': date,
                        'city': city,
                        'product_name': product,
                        'category': info['category'],
                        'unit': info['unit'],
                        'price_usd': round(supplier_price, 2),
                        'inflation_percent': round(inflation_pct, 2),
                        'supplier_type': supplier
                    })
    
    return pd.DataFrame(records)

def generate_telecom_packages():
    """Generate telecom and internet pricing data"""
    records = []
    
    providers = ['Somtel', 'Hormuud', 'Golis', 'Nationlink', 'Eastafrican']
    package_types = ['Voice Bundle', 'Data Bundle', 'Mixed Bundle']
    
    base_prices = {
        'Voice Bundle': 0.50,
        'Data Bundle': 1.50,
        'Mixed Bundle': 2.00
    }
    
    for city in CITIES:
        params = CITY_PARAMS[city]
        
        for provider in providers:
            # Provider-specific pricing (market competition)
            provider_multiplier = np.random.uniform(0.95, 1.08)
            
            for pkg_type in package_types:
                base_price = base_prices[pkg_type]
                price = base_price * provider_multiplier
                
                for date in DATE_RANGE:
                    # Gradual price increases (typical telecom behavior)
                    trend = (date - DATE_RANGE[0]).days * 0.0001
                    
                    # Occasional promotions (reduce by 10-20%)
                    if np.random.random() < 0.05:
                        promotion = np.random.uniform(0.80, 0.90)
                    else:
                        promotion = 1.0
                    
                    current_price = (price + trend) * promotion
                    
                    # Data amounts
                    if 'Data' in pkg_type or 'Mixed' in pkg_type:
                        data_gb = np.random.choice([0.5, 1, 2, 3, 5])
                    else:
                        data_gb = 0
                    
                    # Validity
                    if 'Data' in pkg_type:
                        validity = np.random.choice([1, 3, 7, 30])
                    else:
                        validity = np.random.choice([1, 7, 30])
                    
                    sos_price = current_price * np.random.uniform(600, 620)
                    
                    records.append({
                        'date': date,
                        'provider': provider,
                        'city': city,
                        'package_type': pkg_type,
                        'data_gb': data_gb,
                        'validity_days': validity,
                        'package_price_usd': round(current_price, 2),
                        'package_price_sos': round(sos_price, 2)
                    })
    
    return pd.DataFrame(records)

def generate_cost_of_living():
    """Generate cost of living indices"""
    records = []
    
    base_indices = {
        'rent_index': 100,
        'food_index': 100,
        'transport_index': 100,
        'utilities_index': 100,
        'internet_index': 100,
    }
    
    for city in CITIES:
        params = CITY_PARAMS[city]
        
        # City-specific base indices (capital city has higher costs)
        if city == 'Mogadishu':
            city_multiplier = 1.15
        elif city in ['Hargeisa', 'Berbera']:
            city_multiplier = 1.05
        else:
            city_multiplier = 1.00
        
        indices = {k: v * city_multiplier for k, v in base_indices.items()}
        
        for date in DATE_RANGE:
            # Inflation trend
            inflation_trend = params['inflation_base'] / 365
            
            # Seasonal variation
            seasonality = 5 * np.sin(2 * np.pi * date.dayofyear / 365)
            
            # Update indices
            for key in indices:
                indices[key] = indices[key] * (1 + inflation_trend/100 + 
                                              (seasonality/len(DATE_RANGE))/100 +
                                              np.random.normal(0, 0.5)/100)
            
            total_cost_index = sum(indices.values()) / len(indices)
            
            records.append({
                'date': date,
                'city': city,
                'rent_index': round(indices['rent_index'], 2),
                'food_index': round(indices['food_index'], 2),
                'transport_index': round(indices['transport_index'], 2),
                'utilities_index': round(indices['utilities_index'], 2),
                'internet_index': round(indices['internet_index'], 2),
                'total_cost_index': round(total_cost_index, 2)
            })
    
    return pd.DataFrame(records)

def main():
    """Generate all datasets"""
    print("🇸🇴 Somalia Market Intelligence - Data Generation")
    print("=" * 60)
    
    output_dir = '/workspaces/somalia-market-intelligence/data/raw'
    os.makedirs(output_dir, exist_ok=True)
    
    datasets = {
        'exchange_rates.csv': generate_exchange_rates,
        'fuel_prices.csv': generate_fuel_prices,
        'food_prices.csv': generate_food_prices,
        'telecom_packages.csv': generate_telecom_packages,
        'cost_of_living.csv': generate_cost_of_living,
    }
    
    for filename, generator in datasets.items():
        print(f"\n📊 Generating {filename}...")
        df = generator()
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"   ✓ {len(df):,} records created")
        print(f"   ✓ Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    
    print("\n" + "=" * 60)
    print("✅ All datasets generated successfully!")
    print(f"📁 Location: {output_dir}")

if __name__ == '__main__':
    main()
