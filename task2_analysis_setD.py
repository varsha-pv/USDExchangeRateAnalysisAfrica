import pandas as pd
import numpy as np

# ============================================
# SET D - TASK 2: RETURNS & VOLATILITY
# ============================================

df = pd.read_csv("cleaned_setD.csv", parse_dates=["date"])

# Sort by currency and date before calculating returns
df = df.sort_values(["pair", "date"]).reset_index(drop=True)

# 1. Daily return
df["daily_return"] = (
    df.groupby("pair")["close"].pct_change()
)

# 2. 7-day rolling volatility
df["vol_7d"] = (
    df.groupby("pair")["daily_return"]
      .transform(lambda x: x.rolling(7).std())
)

# 3. 30-day rolling volatility
df["vol_30d"] = (
    df.groupby("pair")["daily_return"]
      .transform(lambda x: x.rolling(30).std())
)

# 4. Annualized rolling volatility
df["vol_7d_annualized"] = df["vol_7d"] * np.sqrt(252)
df["vol_30d_annualized"] = df["vol_30d"] * np.sqrt(252)

# 5. Full-period summary
summary = []

for pair, g in df.groupby("pair"):
    returns = g["daily_return"].dropna()

    start_close = g["close"].iloc[0]
    end_close = g["close"].iloc[-1]

    summary.append({
        "pair": pair,
        "start_date": g["date"].min(),
        "end_date": g["date"].max(),
        "start_close": start_close,
        "end_close": end_close,

        # Change in the USD/local-currency pair
        "pair_total_return": end_close / start_close - 1,

        # Since USD/local rises when the local currency weakens,
        # local currency value change has the opposite sign.
        "currency_value_change": 1 - end_close / start_close,

        "annualized_daily_volatility":
            returns.std() * np.sqrt(252),

        "average_30d_annualized_volatility":
            g["vol_30d_annualized"].mean(),

        "maximum_30d_annualized_volatility":
            g["vol_30d_annualized"].max(),

        "maximum_7d_annualized_volatility":
            g["vol_7d_annualized"].max()
    })

summary = pd.DataFrame(summary)

print("\n========== TASK 2 SUMMARY ==========")
print(summary.round(4).to_string(index=False))

print("\nMost volatile:")
print(summary.loc[
    summary["annualized_daily_volatility"].idxmax(), "pair"
])

print("\nLeast volatile:")
print(summary.loc[
    summary["annualized_daily_volatility"].idxmin(), "pair"
])

print("\nBest currency performer (least depreciation):")
print(summary.loc[
    summary["currency_value_change"].idxmax(), "pair"
])

print("\nWorst currency performer (most depreciation):")
print(summary.loc[
    summary["currency_value_change"].idxmin(), "pair"
])

# Save results
summary.to_csv("setD_task2_summary.csv", index=False)
df.to_csv("setD_task2_with_returns_volatility.csv", index=False)

print("\nFiles saved:")
print("setD_task2_summary.csv")
print("setD_task2_with_returns_volatility.csv")