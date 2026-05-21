-- Somalia Market Intelligence - Market Queries
-- Use these queries for region comparison and market intelligence reporting

-- 1. Fuel Price and Volatility Analysis
SELECT
    city,
    fuel_type,
    station_type,
    AVG(fuel_price_usd) AS avg_usd_price,
    AVG(fuel_price_sos) AS avg_sos_price,
    STDDEV_POP(fuel_price_usd) AS volatility_usd,
    COUNT(*) AS observations
FROM fuel_prices
GROUP BY city, fuel_type, station_type
ORDER BY city, fuel_type, avg_usd_price DESC;

-- Top cities for price volatility
SELECT
    city,
    fuel_type,
    STDDEV_POP(fuel_price_usd) AS price_volatility,
    AVG(fuel_price_usd) AS avg_price_usd
FROM fuel_prices
GROUP BY city, fuel_type
ORDER BY price_volatility DESC
LIMIT 20;

-- 2. Telecom Regional Comparison
SELECT
    city,
    provider,
    package_type,
    AVG(package_price_usd) AS avg_price_usd,
    AVG(data_gb) AS avg_data_gb,
    AVG(validity_days) AS avg_validity_days
FROM telecom_packages
GROUP BY city, provider, package_type
ORDER BY city, provider, avg_price_usd;

-- Telecom package ranking within cities
SELECT
    city,
    provider,
    AVG(package_price_usd / NULLIF(data_gb, 0)) AS avg_price_per_gb,
    RANK() OVER (PARTITION BY city ORDER BY AVG(package_price_usd / NULLIF(data_gb, 0)) ASC) AS value_rank
FROM telecom_packages
WHERE data_gb > 0
GROUP BY city, provider
ORDER BY city, value_rank;

-- 3. Regional Cost of Living Comparison
SELECT
    city,
    AVG(total_cost_index) AS avg_cost_index,
    AVG(food_index) AS avg_food_index,
    AVG(rent_index) AS avg_rent_index,
    AVG(transport_index) AS avg_transport_index,
    AVG(utilities_index) AS avg_utilities_index,
    AVG(internet_index) AS avg_internet_index
FROM cost_of_living
GROUP BY city
ORDER BY avg_cost_index DESC;

-- 4. Price Change and Trend Detection
WITH monthly_fuel AS (
    SELECT
        DATE_FORMAT(date, '%Y-%m-01') AS month,
        city,
        fuel_type,
        AVG(fuel_price_usd) AS avg_price
    FROM fuel_prices
    GROUP BY DATE_FORMAT(date, '%Y-%m-01'), city, fuel_type
)
SELECT
    month,
    city,
    fuel_type,
    avg_price,
    LAG(avg_price) OVER (PARTITION BY city, fuel_type ORDER BY month) AS prev_avg_price,
    ROUND((avg_price - LAG(avg_price) OVER (PARTITION BY city, fuel_type ORDER BY month)) / NULLIF(LAG(avg_price) OVER (PARTITION BY city, fuel_type ORDER BY month), 0) * 100, 2) AS mom_pct_change
FROM monthly_fuel
ORDER BY city, fuel_type, month DESC;
