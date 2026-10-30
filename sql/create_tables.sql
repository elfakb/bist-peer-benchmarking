DROP TABLE IF EXISTS dim_company;
DROP TABLE IF EXISTS dim_period;
DROP TABLE IF EXISTS fact_income_statement;
DROP TABLE IF EXISTS fact_balance_sheet;
DROP TABLE IF EXISTS fact_cash_flow;

CREATE TABLE dim_company (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    currency TEXT
);

CREATE TABLE dim_period (
    year INTEGER PRIMARY KEY,
    inflation_accounting INTEGER,
    growth_comparable INTEGER
);

CREATE TABLE fact_income_statement (
    ticker TEXT,
    period_end TEXT,
    year INTEGER,
    net_sales REAL,
    cost_of_sales REAL,
    gross_profit REAL,
    operating_income REAL,
    ebitda REAL,
    interest_expense REAL,
    net_income REAL,
    PRIMARY KEY (ticker, year)
);

CREATE TABLE fact_balance_sheet (
    ticker TEXT,
    period_end TEXT,
    year INTEGER,
    total_assets REAL,
    current_assets REAL,
    inventory REAL,
    cash REAL,
    current_liabilities REAL,
    total_liabilities REAL,
    total_debt REAL,
    lease_liabilities REAL,
    equity REAL,
    PRIMARY KEY (ticker, year)
);

CREATE TABLE fact_cash_flow (
    ticker TEXT,
    period_end TEXT,
    year INTEGER,
    operating_cash_flow REAL,
    capex REAL,
    PRIMARY KEY (ticker, year)
);