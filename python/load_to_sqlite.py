import sqlite3

import pandas as pd

from config import BASE_DIR, PROCESSED_DIR

SQL_DIR = BASE_DIR / "sql"
db_path = BASE_DIR / "data" / "peer.db"
if db_path.exists():
    db_path.unlink()

con = sqlite3.connect(db_path)
con.executescript((SQL_DIR / "create_tables.sql").read_text())

for table in [
    "dim_company", "dim_period", "fact_income_statement",
    "fact_balance_sheet", "fact_cash_flow",
]:
    pd.read_csv(PROCESSED_DIR / f"{table}.csv").to_sql(
        table, con, if_exists="append", index=False
    )

con.executescript((SQL_DIR / "ratio_views.sql").read_text())

check = pd.read_sql("SELECT ticker, year, net_margin, roe, current_ratio FROM v_ratios ORDER BY ticker, year", con)
print(check)
con.close()