from datetime import date

import pandas as pd
import yfinance as yf

from config import COMPANIES, RAW_DIR

RAW_DIR.mkdir(parents=True, exist_ok=True)

STATEMENTS = {
    "income": "financials",
    "balance": "balance_sheet",
    "cashflow": "cashflow",
}

frames = []
for ticker in COMPANIES:
    t = yf.Ticker(ticker)
    for statement, attr in STATEMENTS.items():
        df = getattr(t, attr)
        if df is None or df.empty:
            print(f"No data: {ticker} / {statement}")
            continue
        df = df.copy()
        df.index.name = "item"
        long = df.reset_index().melt(
            id_vars="item", var_name="period_end", value_name="value"
        )
        long["ticker"] = ticker
        long["statement"] = statement
        frames.append(long)

raw = pd.concat(frames, ignore_index=True)
raw["fetched_at"] = date.today().isoformat()
raw.to_csv(RAW_DIR / "raw_financials.csv", index=False)

print(raw.groupby(["ticker", "statement"])["period_end"].nunique())