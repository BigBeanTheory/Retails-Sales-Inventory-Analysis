INSERT INTO inventory_risk_metrics
(date, product_id, category, region, inventory_level,
 turnover_rate, stockout_risk, overstock_risk, risk_level)

SELECT 
    date,
    product_id,
    category,
    region,
    inventory_level,
    
    -- Basic turnover (sold / current inventory)
    ROUND(COALESCE(units_sold / NULLIF(inventory_level, 0), 0), 2) AS turnover_rate,
    
    -- Stockout risk: low inventory + reasonably high sales today
    CASE 
        WHEN inventory_level <= 40          -- adjust threshold after seeing data
             AND units_sold >= 25 
        THEN 1 
        ELSE 0 
    END AS stockout_risk,
    
    -- Overstock risk: high inventory + low sales today
    CASE 
        WHEN inventory_level >= 350         -- adjust threshold
             AND units_sold <= 8 
        THEN 1 
        ELSE 0 
    END AS overstock_risk,
    
    CASE 
        WHEN inventory_level <= 40 AND units_sold >= 25 
            THEN 'High Stockout Risk'
        WHEN inventory_level >= 350 AND units_sold <= 8 
            THEN 'High Overstock Risk'
        ELSE 'Normal'
    END AS risk_level

FROM sales_transactions

-- Optional: start with recent data only if full insert is slow
-- WHERE date >= '2023-01-01'
;

-- After running, check results
SELECT COUNT(*) AS total_rows_loaded FROM inventory_risk_metrics;

SELECT risk_level, COUNT(*) AS count
FROM inventory_risk_metrics
GROUP BY risk_level;

-- Look at actual risky items
SELECT * 
FROM inventory_risk_metrics 
WHERE stockout_risk = 1 OR overstock_risk = 1
ORDER BY date DESC
LIMIT 20;