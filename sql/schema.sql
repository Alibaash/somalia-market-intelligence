-- Somalia Market Intelligence - Database Schema
-- Production-ready table definitions

-- ============================================================
-- EXCHANGE RATES TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS exchange_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    usd_sos_rate DECIMAL(10, 4) NOT NULL,
    daily_change_percent DECIMAL(8, 4),
    market_type VARCHAR(50),
    source VARCHAR(100),
    rate_ma7 DECIMAL(10, 4),
    rate_ma30 DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_date_city (date, city),
    INDEX idx_market_type (market_type),
    UNIQUE KEY unique_record (date, city, market_type)
);

-- ============================================================
-- FUEL PRICES TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS fuel_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    fuel_price_usd DECIMAL(10, 4) NOT NULL,
    fuel_price_sos DECIMAL(12, 2) NOT NULL,
    station_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_date_city_fuel (date, city, fuel_type),
    INDEX idx_station_type (station_type)
);

-- ============================================================
-- FOOD PRICES TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS food_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit VARCHAR(20),
    price_usd DECIMAL(10, 4) NOT NULL,
    price_sos DECIMAL(12, 2),
    inflation_percent DECIMAL(8, 4),
    supplier_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_date_city_product (date, city, product_name),
    INDEX idx_category (category),
    INDEX idx_inflation (inflation_percent)
);

-- ============================================================
-- TELECOM PACKAGES TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS telecom_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    provider VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    package_type VARCHAR(100) NOT NULL,
    data_gb DECIMAL(5, 2),
    validity_days INT,
    package_price_usd DECIMAL(10, 4) NOT NULL,
    package_price_sos DECIMAL(12, 2),
    price_per_gb_usd DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_date_provider_city (date, provider, city),
    INDEX idx_package_type (package_type),
    INDEX idx_price_per_gb (price_per_gb_usd)
);

-- ============================================================
-- COST OF LIVING TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS cost_of_living (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    rent_index DECIMAL(10, 2) NOT NULL,
    food_index DECIMAL(10, 2) NOT NULL,
    transport_index DECIMAL(10, 2) NOT NULL,
    utilities_index DECIMAL(10, 2) NOT NULL,
    internet_index DECIMAL(10, 2) NOT NULL,
    total_cost_index DECIMAL(10, 2) NOT NULL,
    month_year VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_date_city (date, city),
    INDEX idx_total_cost_index (total_cost_index),
    UNIQUE KEY unique_daily_record (date, city)
);

-- ============================================================
-- MATERIALIZED VIEWS / ANALYTICS TABLES
-- ============================================================

-- Daily KPI Summary Table (for dashboard performance)
CREATE TABLE IF NOT EXISTS daily_kpi_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    city VARCHAR(50),
    avg_exchange_rate DECIMAL(10, 4),
    avg_food_inflation DECIMAL(8, 4),
    avg_fuel_price_usd DECIMAL(10, 4),
    avg_telecom_price_usd DECIMAL(10, 4),
    avg_cost_of_living_index DECIMAL(10, 2),
    exchange_rate_volatility DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_date_city (date, city)
);

-- Regional Comparison Table
CREATE TABLE IF NOT EXISTS regional_comparison (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(12, 4),
    comparison_period VARCHAR(20),
    rank_in_category INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_city_metric (city, metric_name)
);

-- ============================================================
-- AUDIT AND METADATA TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS data_quality_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    check_date DATETIME,
    table_name VARCHAR(100),
    total_records INT,
    null_records INT,
    outlier_records INT,
    quality_score DECIMAL(5, 2),
    notes TEXT,
    
    INDEX idx_check_date (check_date)
);

CREATE TABLE IF NOT EXISTS data_import_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_date DATETIME,
    source_file VARCHAR(255),
    table_name VARCHAR(100),
    records_imported INT,
    records_failed INT,
    status VARCHAR(50),
    error_message TEXT,
    
    INDEX idx_import_date (import_date)
);

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

DELIMITER //

-- Procedure to refresh daily KPI summary
CREATE PROCEDURE refresh_daily_kpi_summary()
BEGIN
    INSERT INTO daily_kpi_summary (date, city, avg_exchange_rate, avg_food_inflation, 
                                   avg_fuel_price_usd, avg_telecom_price_usd, 
                                   avg_cost_of_living_index, exchange_rate_volatility)
    SELECT 
        CURDATE(),
        COALESCE(er.city, fp.city, fuel.city, tp.city),
        AVG(er.usd_sos_rate),
        AVG(fp.inflation_percent),
        AVG(fuel.fuel_price_usd),
        AVG(tp.package_price_usd),
        AVG(col.total_cost_index),
        STDDEV_POP(er.usd_sos_rate)
    FROM 
        exchange_rates er
        LEFT JOIN food_prices fp ON er.date = fp.date AND er.city = fp.city
        LEFT JOIN fuel_prices fuel ON er.date = fuel.date AND er.city = fuel.city
        LEFT JOIN telecom_packages tp ON er.date = tp.date AND er.city = tp.city
        LEFT JOIN cost_of_living col ON er.date = col.date AND er.city = col.city
    WHERE er.date = CURDATE()
    GROUP BY COALESCE(er.city, fp.city, fuel.city, tp.city);
END //

-- Procedure to identify anomalies
CREATE PROCEDURE identify_market_anomalies(IN lookback_days INT)
BEGIN
    SELECT 
        'Exchange Rate Spike' as anomaly_type,
        date,
        city,
        usd_sos_rate as value,
        ROUND((usd_sos_rate - AVG(usd_sos_rate) OVER (
            PARTITION BY city 
            ORDER BY date 
            ROWS BETWEEN lookback_days PRECEDING AND CURRENT ROW
        )) / STDDEV_POP(usd_sos_rate) OVER (
            PARTITION BY city 
            ORDER BY date 
            ROWS BETWEEN lookback_days PRECEDING AND CURRENT ROW
        ), 2) as zscore
    FROM exchange_rates
    WHERE date >= DATE_SUB(CURDATE(), INTERVAL lookback_days DAY)
        AND (usd_sos_rate - AVG(usd_sos_rate) OVER (
            PARTITION BY city 
            ORDER BY date 
            ROWS BETWEEN lookback_days PRECEDING AND CURRENT ROW
        )) / STDDEV_POP(usd_sos_rate) OVER (
            PARTITION BY city 
            ORDER BY date 
            ROWS BETWEEN lookback_days PRECEDING AND CURRENT ROW
        ) > 2
    ORDER BY date DESC;
END //

DELIMITER ;

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

CREATE INDEX idx_exchange_rate_time_series ON exchange_rates(city, date);
CREATE INDEX idx_food_prices_time_series ON food_prices(city, date, product_name);
CREATE INDEX idx_telecom_provider_city ON telecom_packages(provider, city, date);
CREATE INDEX idx_col_city_time ON cost_of_living(city, date);
CREATE INDEX idx_fuel_price_city_type ON fuel_prices(city, fuel_type, date);
