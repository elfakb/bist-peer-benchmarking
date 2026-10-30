import pandas as pd

from config import PROCESSED_DIR

df = pd.read_csv(PROCESSED_DIR / "fact_ratios.csv")
log_path = PROCESSED_DIR / "data_quality_log.csv"
log = pd.read_csv(log_path)
new = []


def flag(r, item, issue):
    new.append({
        "ticker": r["ticker"], "year": r["year"], "statement": "check",
        "item": item, "issue": issue,
    })


for _, r in df.iterrows():
    if pd.notna(r["total_assets"]) and pd.notna(r["total_liabilities"]) and pd.notna(r["equity"]):
        gap = abs(r["total_assets"] - r["total_liabilities"] - r["equity"]) / r["total_assets"]
        if gap > 0.05:
            flag(r, "balance_identity", f"assets != liabilities + equity (gap {gap:.1%}, possibly minority interest)")

    if pd.notna(r["net_sales"]) and pd.notna(r["cost_of_sales"]) and pd.notna(r["gross_profit"]):
        gap = abs(r["net_sales"] - r["cost_of_sales"] - r["gross_profit"]) / r["net_sales"]
        if gap > 0.01:
            flag(r, "gross_profit", f"gross profit differs from sales - cost of sales ({gap:.1%})")

    if pd.notna(r["current_ratio"]) and not 0.1 <= r["current_ratio"] <= 5:
        flag(r, "current_ratio", f"unusual value {r['current_ratio']:.2f}")

    if pd.notna(r["net_margin"]) and abs(r["net_margin"]) > 30:
        flag(r, "net_margin", f"unusual value {r['net_margin']:.1f}%")

counts = df.groupby("ticker")["year"].nunique()
for ticker, n in counts.items():
    if n < 4:
        new.append({
            "ticker": ticker, "year": None, "statement": "check",
            "item": "coverage", "issue": f"only {n} years available",
        })

log = pd.concat([log, pd.DataFrame(new)], ignore_index=True).drop_duplicates()
log.to_csv(log_path, index=False)

print(f"New issues flagged: {len(new)}")
print(log.groupby(["ticker", "issue"]).size().head(30))