CREATE DATABASE retail_db;
USE retail_db;

CREATE TABLE sales_transactions (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    date                DATE,
    store_id            VARCHAR(10),
    product_id          VARCHAR(10),
    category            VARCHAR(50),
    region              VARCHAR(50),
    inventory_level     INT,
    units_sold          INT,
    units_ordered       INT,
    demand_forecast     DECIMAL(10,2),
    price               DECIMAL(10,2),
    discount            DECIMAL(5,2),
    weather_condition   VARCHAR(50),
    holiday_promotion   TINYINT,          
    competitor_pricing  DECIMAL(10,2),
    seasonality         VARCHAR(50)
);

CREATE TABLE inventory_risk_metrics (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    date                DATE,
    product_id          VARCHAR(10),
    category            VARCHAR(50),
    region              VARCHAR(50),
    inventory_level     INT,
    turnover_rate       DECIMAL(10,2),
    stockout_risk       TINYINT DEFAULT 0,
    overstock_risk      TINYINT DEFAULT 0,
    risk_level          VARCHAR(50)
);

CREATE TABLE generated_demand_forecasts (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    date                DATE,
    product_id          VARCHAR(10),
    forecasted_units    INT,
    model_used          VARCHAR(50),
    confidence_score    DECIMAL(5,2)
);