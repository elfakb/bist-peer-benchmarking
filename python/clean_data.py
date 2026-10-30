import numpy as np
import pandas as pd

from config import (
    COMPANIES, CURRENCY, INFLATION_ACCOUNTING_FROM,
    ITEM_MAP, PROCESSED_DIR, RAW_DIR, SCALE,
)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(RAW_DIR / "raw_financials.csv", parse_dates=["period_end"])
raw["value"] = pd.to_numeric(raw["value"], errors="coerce")

log = []


def standardize(statement):
    df = raw[raw["statement"] == statement]
    wide = df.pivot_table(
        index=["ticker", "period_end"], columns="item",
        values="value", aggfunc="first",
    )
    out = pd.DataFrame(index=wide.index)
    for std, aliases in ITEM_MAP[statement].items():
        s = pd.Series(np.nan, index=wide.index)
        for alias in aliases:
            if alias in wide.columns:
                s = s.fillna(wide[alias])
        out[std] = s / SCALE
    out = out.reset_index()
    out["year"] = out["period_end"].dt.year
    return out


def log_missing(df, statement):
    for _, r in df.iterrows():
        for col in ITEM_MAP[statement]:
            if pd.isna(r[col]):
                log.append({
                    "ticker": r["ticker"], "year": r["year"],
                    "statement": statement, "item": col,
                    "issue": "missing value",
                })


income = standardize("income")
balance = standardize("balance")
cashflow = standardize("cashflow")

derived = income["gross_profit"].isna() & income["net_sales"].notna() & income["cost_of_sales"].notna()
income.loc[derived, "gross_profit"] = income["net_sales"] - income["cost_of_sales"]
for _, r in income[derived].iterrows():
    log.append({
        "ticker": r["ticker"], "year": r["year"], "statement": "income",
        "item": "gross_profit", "issue": "derived as net_sales - cost_of_sales",
    })

log_missing(income, "income")
log_missing(balance, "balance")
log_missing(cashflow, "cashflow")

years = sorted(set(income["year"]) | set(balance["year"]) | set(cashflow["year"]))
for ticker in COMPANIES:
    for y in years:
        if y == INFLATION_ACCOUNTING_FROM:
            log.append({
                "ticker": ticker, "year": y, "statement": "all", "item": "growth",
                "issue": "TMS 29 transition: growth vs prior year not comparable",
            })
        if y == INFLATION_ACCOUNTING_FROM + 1:
            log.append({
                "ticker": ticker, "year": y, "statement": "all", "item": "growth",
                "issue": "TMS 29: check that prior-year figures are restated to the same purchasing power",
            })

dim_company = pd.DataFrame([
    {"ticker": t, "name": v["name"], "sector": v["sector"], "currency": CURRENCY}
    for t, v in COMPANIES.items()
])
dim_period = pd.DataFrame({"year": years})
dim_period["inflation_accounting"] = (dim_period["year"] >= INFLATION_ACCOUNTING_FROM).astype(int)
dim_period["growth_comparable"] = (dim_period["year"] != INFLATION_ACCOUNTING_FROM).astype(int)

for df in (income, balance, cashflow):
    df["period_end"] = df["period_end"].dt.strftime("%Y-%m-%d")

dim_company.to_csv(PROCESSED_DIR / "dim_company.csv", index=False)
dim_period.to_csv(PROCESSED_DIR / "dim_period.csv", index=False)
income.to_csv(PROCESSED_DIR / "fact_income_statement.csv", index=False)
balance.to_csv(PROCESSED_DIR / "fact_balance_sheet.csv", index=False)
cashflow.to_csv(PROCESSED_DIR / "fact_cash_flow.csv", index=False)
pd.DataFrame(log).to_csv(PROCESSED_DIR / "data_quality_log.csv", index=False)

print(f"Years found: {years}")
print(f"Quality log entries: {len(log)}")