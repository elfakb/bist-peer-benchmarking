from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

COMPANIES = {
    "BIMAS.IS": {"name": "BIM", "sector": "Food Retail"},
    "MGROS.IS": {"name": "Migros", "sector": "Food Retail"},
    "SOKM.IS": {"name": "Sok Marketler", "sector": "Food Retail"},
}

CURRENCY = "TRY"
SCALE = 1_000_000 
INFLATION_ACCOUNTING_FROM = 2023  

ITEM_MAP = {
    "income": {
        "net_sales": ["Total Revenue", "Operating Revenue"],
        "cost_of_sales": ["Cost Of Revenue"],
        "gross_profit": ["Gross Profit"],
        "operating_income": ["Operating Income"],
        "ebitda": ["EBITDA", "Normalized EBITDA"],
        "interest_expense": ["Interest Expense", "Interest Expense Non Operating"],
        "net_income": ["Net Income Common Stockholders", "Net Income"],
    },
    "balance": {
        "total_assets": ["Total Assets"],
        "current_assets": ["Current Assets"],
        "inventory": ["Inventory"],
        "cash": ["Cash And Cash Equivalents"],
        "current_liabilities": ["Current Liabilities"],
        "total_liabilities": ["Total Liabilities Net Minority Interest"],
        "total_debt": ["Total Debt"],
        "lease_liabilities": ["Capital Lease Obligations"],
        "equity": ["Stockholders Equity", "Common Stock Equity"],
    },
    "cashflow": {
        "operating_cash_flow": [
            "Operating Cash Flow",
            "Cash Flow From Continuing Operating Activities",
        ],
        "capex": ["Capital Expenditure"],
    },
}