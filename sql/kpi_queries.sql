-- Somalia Market Intelligence - SQL Analysis Queries
-- Database schema and KPI calculations

-- ============================================================
-- 1. EXCHANGE RATE ANALYSIS QUERIES
-- ============================================================

-- Daily exchange rate statistics
SELECT 
    date,
    city,
    usd_sos_rate,
    ROUND(daily_change_percent, 4) as daily_pct_change,
    market_type,
    ROW_NUMBER() OVER (PARTITION BY city ORDER BY date) as day_number,
    AVG(usd_sos_rate) OVER (
        PARTITION BY city 
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma7_rate,
    AVG(usd_sos_rate) OVER (
        PARTITION BY city 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as ma30_rate
FROM exchange_rates
ORDER BY date DESC, city;

-- Exchange rate volatility by city (30-day rolling standard deviation)
SELECT 
    city,
    date,
    usd_sos_rate,
    STDDEV_POP(usd_sos_rate) OVER (
        PARTITION BY city 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as volatility_30d,
    AVG(ABS(daily_change_percent)) OVER (
        PARTITION BY city 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as avg_daily_volatility
FROM exchange_rates
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
ORDER BY city, date DESC;

-- Market type comparison
SELECT 
    date,
    market_type,
    COUNT(*) as num_records,
    AVG(usd_sos_rate) as avg_rate,
    MIN(usd_sos_rate) as min_rate,
    MAX(usd_sos_rate) as max_rate,
    STDDEV_POP(usd_sos_rate) as volatility
FROM exchange_rates
GROUP BY date, market_type
ORDER BY date DESC;

-- ============================================================
-- 2. FOOD INFLATION ANALYSIS QUERIES
-- ============================================================

-- Top 20 most inflating products
SELECT 
    product_name,
    category,
    AVG(inflation_percent) as avg_inflation,
    MIN(inflation_percent) as min_inflation,
    MAX(inflation_percent) as max_inflation,
    STDDEV_POP(inflation_percent) as volatility,
    COUNT(DISTINCT date) as observation_days
FROM food_prices
GROUP BY product_name, category
ORDER BY avg_inflation DESC
LIMIT 20;

-- Regional inflation comparison
SELECT 
    city,
    category,
    AVG(inflation_percent) as avg_inflation,
    AVG(price_usd) as avg_price_usd,
    COUNT(*) as total_records,
    RANK() OVER (PARTITION BY category ORDER BY AVG(inflation_percent) DESC) as inflation_rank
FROM food_prices
GROUP BY city, category
ORDER BY category, avg_inflation DESC;

-- Month-over-month inflation tracking
SELECT 
    YEAR(date) as year,
    MONTH(date) as month,
    product_name,
    AVG(price_usd) as avg_price,
    AVG(inflation_percent) as avg_inflation,
    LAG(AVG(price_usd)) OVER (
        PARTITION BY product_name 
        ORDER BY YEAR(date), MONTH(date)
    ) as prev_month_price,
    ROUND(
        ((AVG(price_usd) - LAG(AVG(price_usd)) OVER (
            PARTITION BY product_name 
            ORDER BY YEAR(date), MONTH(date)
        )) / LAG(AVG(price_usd)) OVER (
            PARTITION BY product_name 
            ORDER BY YEAR(date), MONTH(date)
        )) * 100, 2
    ) as month_over_month_pct
FROM food_prices
GROUP BY YEAR(date), MONTH(date), product_name
ORDER BY year DESC, month DESC, product_name;

-- ============================================================
-- 3. COST OF LIVING ANALYSIS QUERIES
-- ============================================================

-- City cost of living rankings
SELECT 
    city,
    date,
    total_cost_index,
    food_index,
    rent_index,
    transport_index,
    utilities_index,
    internet_index,
    RANK() OVER (ORDER BY total_cost_index DESC) as cost_rank,
    ROUND(
        ((total_cost_index - LAG(total_cost_index) OVER (
            PARTITION BY city 
            ORDER BY date
        )) / LAG(total_cost_index) OVER (
            PARTITION BY city 
            ORDER BY date
        )) * 100, 2
    ) as daily_pct_change
FROM cost_of_living
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY date DESC, total_cost_index DESC;

-- Component analysis: what drives cost of living?
SELECT 
    city,
    total_cost_index,
    ROUND(food_index / total_cost_index * 100, 2) as food_pct,
    ROUND(rent_index / total_cost_index * 100, 2) as rent_pct,
    ROUND(transport_index / total_cost_index * 100, 2) as transport_pct,
    ROUND(utilities_index / total_cost_index * 100, 2) as utilities_pct,
    ROUND(internet_index / total_cost_index * 100, 2) as internet_pct
FROM cost_of_living
WHERE date = (SELECT MAX(date) FROM cost_of_living)
ORDER BY total_cost_index DESC;

-- ============================================================
-- 4. TELECOM PRICING ANALYSIS QUERIES
-- ============================================================

-- Provider pricing comparison
SELECT 
    provider,
    package_type,
    city,
    AVG(package_price_usd) as avg_price_usd,
    MIN(package_price_usd) as min_price,
    MAX(package_price_usd) as max_price,
    AVG(data_gb) as avg_data,
    AVG(validity_days) as avg_validity,
    COUNT(*) as num_packages
FROM telecom_packages
WHERE date = (SELECT MAX(date) FROM telecom_packages)
GROUP BY provider, package_type, city
ORDER BY provider, avg_price_usd DESC;

-- Value-for-money ranking (price per GB)
SELECT 
    provider,
    city,
    AVG(package_price_usd / NULLIF(data_gb, 0)) as price_per_gb,
    AVG(package_price_usd) as avg_price,
    AVG(data_gb) as avg_data,
    RANK() OVER (PARTITION BY city ORDER BY AVG(package_price_usd / NULLIF(data_gb, 0))) as value_rank
FROM telecom_packages
WHERE data_gb > 0 
    AND date = (SELECT MAX(date) FROM telecom_packages)
GROUP BY provider, city
ORDER BY city, price_per_gb;

-- Price trends by provider over time
SELECT 
    provider,
    DATE_FORMAT(date, '%Y-%m-01') as month,
    AVG(package_price_usd) as avg_price,
    MIN(package_price_usd) as min_price,
    MAX(package_price_usd) as max_price,
    COUNT(DISTINCT city) as num_cities,
    RANK() OVER (PARTITION BY provider ORDER BY DATE_FORMAT(date, '%Y-%m-01')) as month_number
FROM telecom_packages
GROUP BY provider, DATE_FORMAT(date, '%Y-%m-01')
ORDER BY provider, month DESC;

-- ============================================================
-- 5. FUEL PRICE ANALYSIS QUERIES
-- ============================================================

-- Fuel price statistics by type and city
SELECT 
    city,
    fuel_type,
    AVG(fuel_price_usd) as avg_price_usd,
    MIN(fuel_price_usd) as min_price,
    MAX(fuel_price_usd) as max_price,
    STDDEV_POP(fuel_price_usd) as price_volatility,
    station_type,
    COUNT(*) as total_records
FROM fuel_prices
GROUP BY city, fuel_type, station_type
ORDER BY city, fuel_type;

-- Fuel price trends
SELECT 
    DATE_FORMAT(date, '%Y-%m-01') as month,
    fuel_type,
    AVG(fuel_price_usd) as avg_price_usd,
    LAG(AVG(fuel_price_usd)) OVER (
        PARTITION BY fuel_type 
        ORDER BY DATE_FORMAT(date, '%Y-%m-01')
    ) as prev_month_price,
    ROUND(
        ((AVG(fuel_price_usd) - LAG(AVG(fuel_price_usd)) OVER (
            PARTITION BY fuel_type 
            ORDER BY DATE_FORMAT(date, '%Y-%m-01')
        )) / LAG(AVG(fuel_price_usd)) OVER (
            PARTITION BY fuel_type 
            ORDER BY DATE_FORMAT(date, '%Y-%m-01')
        )) * 100, 2
    ) as month_over_month_pct
FROM fuel_prices
GROUP BY DATE_FORMAT(date, '%Y-%m-01'), fuel_type
ORDER BY fuel_type, month DESC;

-- ============================================================
-- 6. COMPREHENSIVE KPI DASHBOARD QUERIES
-- ============================================================

-- Overall market snapshot (latest date)
WITH latest_data AS (
    SELECT MAX(date) as max_date FROM exchange_rates
)
SELECT 
    'Exchange Rate' as metric,
    CAST(AVG(usd_sos_rate) as CHAR) as value,
    'SOS/USD' as unit
FROM exchange_rates, latest_data
WHERE date = latest_data.max_date

UNION ALL

SELECT 
    'Avg Food Inflation' as metric,
    ROUND(AVG(inflation_percent), 2) as value,
    '%' as unit
FROM food_prices
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)

UNION ALL

SELECT 
    'Avg Telecom Price' as metric,
    ROUND(AVG(package_price_usd), 2) as value,
    'USD' as unit
FROM telecom_packages
WHERE date = (SELECT MAX(date) FROM telecom_packages)

UNION ALL

SELECT 
    'Avg Cost of Living Index' as metric,
    ROUND(AVG(total_cost_index), 2) as value,
    'Index' as unit
FROM cost_of_living
WHERE date = (SELECT MAX(date) FROM cost_of_living);

-- ============================================================
-- 7. ANOMALY DETECTION - Extreme price spikes
-- ============================================================

SELECT 
    'Food' as category,
    date,
    city,
    product_name,
    price_usd,
    inflation_percent,
    AVG(price_usd) OVER (PARTITION BY city, product_name ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) as ma30_price,
    (price_usd - AVG(price_usd) OVER (PARTITION BY city, product_name ROWS BETWEEN 30 PRECEDING AND CURRENT ROW)) / 
    STDDEV_POP(price_usd) OVER (PARTITION BY city, product_name ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) as zscore
FROM food_prices
WHERE (price_usd - AVG(price_usd) OVER (PARTITION BY city, product_name ROWS BETWEEN 30 PRECEDING AND CURRENT ROW)) / 
      STDDEV_POP(price_usd) OVER (PARTITION BY city, product_name ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) > 2.5
ORDER BY date DESC
LIMIT 100;
