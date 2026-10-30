DROP VIEW IF EXISTS v_ratios;

CREATE VIEW v_ratios AS
WITH base AS (
    SELECT
        i.ticker, c.name, i.year, p.growth_comparable,
        i.net_sales, i.gross_profit, i.operating_income, i.ebitda, i.net_income,
        b.total_assets, b.current_assets, b.inventory, b.cash,
        b.current_liabilities, b.total_liabilities, b.total_debt,
        b.lease_liabilities, b.equity,
        f.operating_cash_flow, ABS(f.capex) AS capex
    FROM fact_income_statement i
    JOIN fact_balance_sheet b ON b.ticker = i.ticker AND b.year = i.year
    JOIN fact_cash_flow f ON f.ticker = i.ticker AND f.year = i.year
    JOIN dim_company c ON c.ticker = i.ticker
    JOIN dim_period p ON p.year = i.year
),
lagged AS (
    SELECT *,
        LAG(year) OVER w AS prev_year,
        LAG(net_sales) OVER w AS prev_sales,
        LAG(operating_income) OVER w AS prev_op,
        LAG(net_income) OVER w AS prev_ni
    FROM base
    WINDOW w AS (PARTITION BY ticker ORDER BY year)
)
SELECT
    ticker, name, year,
    100.0 * gross_profit / NULLIF(net_sales, 0) AS gross_margin,
    100.0 * operating_income / NULLIF(net_sales, 0) AS operating_margin,
    100.0 * net_income / NULLIF(net_sales, 0) AS net_margin,
    100.0 * net_income / NULLIF(total_assets, 0) AS roa,
    100.0 * net_income / NULLIF(equity, 0) AS roe,
    1.0 * current_assets / NULLIF(current_liabilities, 0) AS current_ratio,
    1.0 * (current_assets - inventory) / NULLIF(current_liabilities, 0) AS quick_ratio,
    1.0 * total_liabilities / NULLIF(equity, 0) AS debt_to_equity,
    CASE WHEN ebitda > 0 THEN (total_debt - cash) / ebitda END AS net_debt_ebitda_incl_leases,
    CASE WHEN ebitda > 0 THEN (total_debt - lease_liabilities - cash) / ebitda END AS net_debt_ebitda_excl_leases,
    CASE WHEN growth_comparable = 1 AND year - prev_year = 1 AND prev_sales > 0
         THEN 100.0 * (net_sales - prev_sales) / prev_sales END AS revenue_growth,
    CASE WHEN growth_comparable = 1 AND year - prev_year = 1 AND prev_op <> 0
         THEN 100.0 * (operating_income - prev_op) / ABS(prev_op) END AS operating_profit_growth,
    CASE WHEN growth_comparable = 1 AND year - prev_year = 1 AND prev_ni <> 0
         THEN 100.0 * (net_income - prev_ni) / ABS(prev_ni) END AS net_income_growth,
    operating_cash_flow,
    operating_cash_flow - capex AS free_cash_flow,
    1.0 * operating_cash_flow / NULLIF(net_income, 0) AS cash_conversion,
    operating_cash_flow - net_income AS ocf_minus_net_income
FROM lagged;