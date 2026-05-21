"""
Data Processing Pipeline for Somalia Market Intelligence
Cleans, validates, and transforms raw data into analysis-ready format
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_raw_data(data_dir='data/raw'):
    """Load all raw datasets"""
    datasets = {}
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            key = filename.replace('.csv', '')
            datasets[key] = pd.read_csv(filepath)
            datasets[key]['date'] = pd.to_datetime(datasets[key]['date'])
            print(f"✓ Loaded {key}: {len(datasets[key]):,} rows")
    
    return datasets

def clean_exchange_rates(df):
    """Clean exchange rate data"""
    df = df.copy()
    
    # Remove outliers (keep rates between 500-700)
    df = df[(df['usd_sos_rate'] >= 500) & (df['usd_sos_rate'] <= 700)]
    
    # Fill any missing values
    df = df.dropna(subset=['usd_sos_rate'])
    
    # Ensure daily_change_percent is within reasonable bounds
    df['daily_change_percent'] = df['daily_change_percent'].clip(-5, 5)
    
    return df

def clean_fuel_prices(df):
    """Clean fuel price data"""
    df = df.copy()
    
    # Remove outliers
    df = df[(df['fuel_price_usd'] >= 0.30) & (df['fuel_price_usd'] <= 1.50)]
    df = df[(df['fuel_price_sos'] >= 100) & (df['fuel_price_sos'] <= 1000)]
    
    df = df.dropna(subset=['fuel_price_usd', 'fuel_price_sos'])
    
    return df

def clean_food_prices(df):
    """Clean food price data"""
    df = df.copy()
    
    # Remove unrealistic prices
    df = df[df['price_usd'] > 0]
    
    # Ensure inflation percentages are reasonable
    df['inflation_percent'] = df['inflation_percent'].clip(-100, 200)
    
    df = df.dropna(subset=['price_usd'])
    
    return df

def clean_telecom_packages(df):
    """Clean telecom package data"""
    df = df.copy()
    
    # Remove unrealistic prices
    df = df[df['package_price_usd'] > 0]
    df = df[df['package_price_sos'] > 0]
    
    df = df.dropna(subset=['package_price_usd'])
    
    return df

def clean_cost_of_living(df):
    """Clean cost of living data"""
    df = df.copy()
    
    # All indices should be positive
    for col in ['rent_index', 'food_index', 'transport_index', 'utilities_index', 'internet_index']:
        df[col] = df[col].clip(lower=50)
    
    df = df.dropna()
    
    return df

def add_calculated_fields(datasets):
    """Add useful calculated fields to datasets"""
    
    # Exchange rates: add 7-day moving average
    datasets['exchange_rates']['rate_ma7'] = (
        datasets['exchange_rates']
        .groupby('city')['usd_sos_rate']
        .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    )
    
    # Exchange rates: add 30-day moving average
    datasets['exchange_rates']['rate_ma30'] = (
        datasets['exchange_rates']
        .groupby('city')['usd_sos_rate']
        .transform(lambda x: x.rolling(window=30, min_periods=1).mean())
    )
    
    # Food prices: add category summary fields
    datasets['food_prices']['price_sos'] = (
        datasets['food_prices']['price_usd'] * 
        datasets['food_prices']['date'].dt.to_period('D').astype(str).apply(lambda x: 610)  # approx exchange rate
    )
    
    # Cost of living: add month-year column
    datasets['cost_of_living']['month_year'] = datasets['cost_of_living']['date'].dt.to_period('M')
    
    # Telecom: add price per GB (for data packages)
    datasets['telecom_packages']['price_per_gb_usd'] = (
        np.where(datasets['telecom_packages']['data_gb'] > 0,
                datasets['telecom_packages']['package_price_usd'] / datasets['telecom_packages']['data_gb'],
                np.nan)
    )
    
    return datasets

def save_processed_data(datasets, output_dir='data/processed'):
    """Save processed datasets"""
    os.makedirs(output_dir, exist_ok=True)
    
    for name, df in datasets.items():
        filepath = os.path.join(output_dir, f'{name}.csv')
        df.to_csv(filepath, index=False)
        print(f"✓ Saved {name}: {len(df):,} rows")

def create_summary_statistics(datasets):
    """Generate summary statistics"""
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    
    for name, df in datasets.items():
        print(f"\n📊 {name.upper()}")
        print(f"   Records: {len(df):,}")
        print(f"   Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"   Missing values: {df.isnull().sum().sum()}")

def main():
    """Run complete data processing pipeline"""
    print("\n🔄 SOMALIA MARKET INTELLIGENCE - DATA PROCESSING PIPELINE")
    print("="*70)
    
    # Load raw data
    print("\n📥 Loading raw data...")
    datasets = load_raw_data('data/raw')
    
    # Clean datasets
    print("\n🧹 Cleaning datasets...")
    datasets['exchange_rates'] = clean_exchange_rates(datasets['exchange_rates'])
    print("   ✓ Exchange rates cleaned")
    
    datasets['fuel_prices'] = clean_fuel_prices(datasets['fuel_prices'])
    print("   ✓ Fuel prices cleaned")
    
    datasets['food_prices'] = clean_food_prices(datasets['food_prices'])
    print("   ✓ Food prices cleaned")
    
    datasets['telecom_packages'] = clean_telecom_packages(datasets['telecom_packages'])
    print("   ✓ Telecom packages cleaned")
    
    datasets['cost_of_living'] = clean_cost_of_living(datasets['cost_of_living'])
    print("   ✓ Cost of living cleaned")
    
    # Add calculated fields
    print("\n📈 Adding calculated fields...")
    datasets = add_calculated_fields(datasets)
    print("   ✓ Calculated fields added")
    
    # Save processed data
    print("\n💾 Saving processed data...")
    save_processed_data(datasets)
    
    # Summary statistics
    create_summary_statistics(datasets)
    
    print("\n" + "="*70)
    print("✅ Data processing complete!")

if __name__ == '__main__':
    main()
