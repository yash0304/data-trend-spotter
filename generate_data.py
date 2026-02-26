import pandas as pd
import numpy as np
import random

np.random.seed(42)

entities = ["ABC Tech Inc", "ABC India Pvt Ltd", "ABC UK Ltd"]
countries = ["USA", "India", "UK"]
cost_centers = ["CC1001", "CC1002", "CC2001", "CC3001", "CC4001"]
profit_centers = ["PC_B2B", "PC_Retail", "PC_Digital"]
gl_codes = ["600101", "600202", "600303", "600404", "600505", "600606"]
expense_heads = ["Marketing", "Software", "Travel", "Consulting", "Rent", "Cloud"]
functions = ["Banking", "AP", "O2C", "Payroll", "Taxation"]
budget_heads = ["IT", "HR", "Admin", "Sales", "Operations"]
vendors = [
    "Google", "Microsoft", "AWS", "Deloitte", "KPMG",
    "Oracle", "SAP", "Infosys", "TCS", "Accenture",
    "Meta", "Adobe", "Salesforce", "Stripe", "HSBC"
]

rows = []

for i in range(1000):
    date = pd.Timestamp("2024-01-01") + pd.to_timedelta(random.randint(0, 180), unit="d")

    row = {
        "Date": date,
        "Company_Entity": random.choice(entities),
        "Country": random.choice(countries),
        "Cost_Center": random.choice(cost_centers),
        "Profit_Center": random.choice(profit_centers),
        "GL_Code": random.choice(gl_codes),
        "Expense_Head": random.choice(expense_heads),
        "Function": random.choice(functions),
        "Budget_Head": random.choice(budget_heads),
        "PO_Number": f"PO{10000+i}",
        "Vendor": random.choice(vendors),
        "Actual_Amount_USD": random.randint(1000, 50000)
    }

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv("data/fpa_actual_1000.csv", index=False)

print("File generated successfully.")