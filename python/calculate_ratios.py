import numpy as np
import pandas as pd

from config import PROCESSED_DIR

KEYS = ["ticker", "year"]

inc = pd.read_csv(PROCESSED_DIR / "fact_income_statement.csv")
bal = pd.read_csv(PROCESSED_DIR / "fact_balance_sheet.csv")
cf = pd.read_csv(PROCESSED_DIR / "fact_cash_flow.csv")
company = pd.read_csv(PROCESSED_DIR / "dim_company.csv")
period = pd.read_csv(PROCESSED_DIR / "dim_period.csv")

df = (
    inc.merge(bal.drop(columns="period_end"), on=KEYS, how="outer")
    .merge(cf.drop(columns="period_end"), on=KEYS, how="outer")
    .merge(company[["ticker", "name"]], on="ticker")
    .merge(period, on="year")
    .sort_values(KEYS)
    .reset_index(drop=True)
)


def div(a, b):
    return a / b.where(b != 0)


df["gross_margin"] = 100 * div(df["gross_profit"], df["net_sales"])
df["operating_margin"] = 100 * div(df["operating_income"], df["net_sales"])
df["net_margin"] = 100 * div(df["net_income"], df["net_sales"])
df["roa"] = 100 * div(df["net_income"], df["total_assets"])
df["roe"] = 100 * div(df["net_income"], df["equity"])

df["current_ratio"] = div(df["current_assets"], df["current_liabilities"])
df["quick_ratio"] = div(df["current_assets"] - df["inventory"], df["current_liabilities"])

df["debt_to_equity"] = div(df["total_liabilities"], df["equity"])
ebitda_pos = df["ebitda"].where(df["ebitda"] > 0)
df["net_debt_incl_leases"] = df["total_debt"] - df["cash"]
df["net_debt_excl_leases"] = df["total_debt"] - df["lease_liabilities"] - df["cash"]
df["net_debt_ebitda_incl_leases"] = df["net_debt_incl_leases"] / ebitda_pos
df["net_debt_ebitda_excl_leases"] = df["net_debt_excl_leases"] / ebitda_pos

for col, name in [
    ("net_sales", "revenue_growth"),
    ("operating_income", "operating_profit_growth"),
    ("net_income", "net_income_growth"),
]:
    prev = df.groupby("ticker")[col].shift(1)
    prev_year = df.groupby("ticker")["year"].shift(1)
    growth = 100 * (df[col] - prev) / prev.abs().where(prev != 0)
    valid = (df["growth_comparable"] == 1) & ((df["year"] - prev_year) == 1)
    df[name] = growth.where(valid)

df["capex_abs"] = df["capex"].abs()
df["free_cash_flow"] = df["operating_cash_flow"] - df["capex_abs"]
df["cash_conversion"] = div(df["operating_cash_flow"], df["net_income"])
df["ocf_minus_net_income"] = df["operating_cash_flow"] - df["net_income"]

df.to_csv(PROCESSED_DIR / "fact_ratios.csv", index=False)

cols = [
    "gross_margin", "operating_margin", "net_margin", "roa", "roe",
    "current_ratio", "quick_ratio", "debt_to_equity",
    "net_debt_ebitda_incl_leases", "net_debt_ebitda_excl_leases",
    "revenue_growth", "operating_profit_growth", "net_income_growth",
    "operating_cash_flow", "free_cash_flow", "cash_conversion",
]

latest = df[df["year"] == df["year"].max()].set_index("name")[cols].T.add_suffix("_latest")
average = df.groupby("name")[cols].mean().T.add_suffix("_avg")
peer = pd.concat([latest, average], axis=1).round(2)
peer.index.name = "metric"
peer.to_csv(PROCESSED_DIR / "peer_comparison_table.csv")

print(peer)