import pandas as pd
import sys
import os


csv_path = "fixed.csv"


def parse_float(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0

def parse_int(v):
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return 0


if len(sys.argv) < 2:
    print("No user_id provided")
    sys.exit(1)
user_id = str(sys.argv[1]).strip()


if not os.path.isfile(csv_path):
    print(f"File not found: {csv_path}")
    sys.exit(1)

try:
    df = pd.read_csv(csv_path, dtype=str)
except Exception as e:
    print("Error reading CSV:", e)
    sys.exit(1)


matches = df[df["UNIQUE_ID"].astype(str).str.strip() == user_id]
if matches.empty:
    print("No data found for this user")
    sys.exit(1)
row = matches.iloc[0]


loan_tenure = parse_float(row.get("LOAN_TENURE"))
times_irac_slip = parse_float(row.get("TIMES_IRAC_SLIP"))
last_1_yr_rg3 = parse_float(row.get("LAST_1_YR_RG3"))
last_1_yr_rg2 = parse_float(row.get("LAST_1_YR_RG2"))
latest_cr_days = parse_float(row.get("LATEST_CR_DAYS"))
acct_age = parse_float(row.get("ACCT_AGE"))
limit_amt = parse_float(row.get("LIMIT"))
outs_amt = parse_float(row.get("OUTS"))
target = parse_int(row.get("TARGET"))

metrics = []



# Loan Tenure
if loan_tenure > 7000:
    metrics.append("Loan tenure is unusually long (High Risk)")
elif loan_tenure > 3000:
    metrics.append("Loan tenure is moderate")
else:
    metrics.append("Loan tenure is normal")

# IRAC Slippages
if times_irac_slip > 20:
    metrics.append(f"IRAC Slippages: High ({times_irac_slip})")
elif times_irac_slip > 10:
    metrics.append(f"IRAC Slippages: Moderate ({times_irac_slip})")
else:
    metrics.append(f"IRAC Slippages: Low ({times_irac_slip})")

# Risk Grades
if last_1_yr_rg3 > 10 or last_1_yr_rg2 > 10:
    metrics.append("Past Risk Grades indicate issues")
else:
    metrics.append("Past Risk Grades are stable")

# Credit Report Days
if latest_cr_days > 50:
    metrics.append(f"Credit report is old ({latest_cr_days} days)")
else:
    metrics.append(f"Credit report is recent ({latest_cr_days} days)")

# Account Age
if acct_age < 1:
    metrics.append("New account (high scrutiny)")
else:
    metrics.append(f"Account age is {acct_age} years")

# Utilization
utilization = outs_amt / limit_amt if limit_amt > 0 else 0
if utilization > 0.9:
    metrics.append("Very high credit utilization")
elif utilization > 0.7:
    metrics.append("High credit utilization")
else:
    metrics.append("Healthy credit utilization")

# System Prediction
if target == 1:
    metrics.append("System Prediction: DEFAULTER")
else:
    metrics.append("System Prediction: NON-DEFAULTER")

# ---------- PRINT REPORT ----------
for line in metrics:
    print(line)
