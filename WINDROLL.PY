import pandas as pd
import numpy as np

# ============================================================
# TASK 2 — ROLLING WINDOW + LONG-TERM TREND ANALYSIS
# SET D: ZAR, EGP, NGN, KES
# ============================================================

# ------------------------------------------------------------
# 1. LOAD CLEANED DATA
# ------------------------------------------------------------

df = pd.read_csv(r"C:\Users\varsh\OneDrive\Desktop\HACK2\TASK1\cleaned_setD.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by currency pair and date
df = df.sort_values(
    ["pair", "date"]
).reset_index(drop=True)

print("============================================================")
print("TASK 2 — ROLLING WINDOW ANALYSIS")
print("============================================================")

print("\nNumber of rows:", len(df))
print("Currency pairs:", df["pair"].unique())


# ------------------------------------------------------------
# 2. DAILY RETURNS
# ------------------------------------------------------------

df["daily_return"] = (
    df.groupby("pair")["close"].pct_change()
)

print("\nDaily returns calculated successfully.")


# ------------------------------------------------------------
# 3. 7-DAY ROLLING VOLATILITY
# ------------------------------------------------------------

df["vol_7d"] = (
    df.groupby("pair")["daily_return"]
      .transform(
          lambda x: x.rolling(7).std()
      )
)

print("7-day rolling volatility calculated.")


# ------------------------------------------------------------
# 4. 30-DAY ROLLING VOLATILITY
# ------------------------------------------------------------

df["vol_30d"] = (
    df.groupby("pair")["daily_return"]
      .transform(
          lambda x: x.rolling(30).std()
      )
)

print("30-day rolling volatility calculated.")


# ------------------------------------------------------------
# 5. ANNUALIZED VOLATILITY
# ------------------------------------------------------------

# Annualization uses sqrt(252)

df["vol_7d_annualized"] = (
    df["vol_7d"] * np.sqrt(252)
)

df["vol_30d_annualized"] = (
    df["vol_30d"] * np.sqrt(252)
)

# Percentage versions

df["vol_7d_percent"] = (
    df["vol_7d_annualized"] * 100
)

df["vol_30d_percent"] = (
    df["vol_30d_annualized"] * 100
)


# ------------------------------------------------------------
# 6. AVERAGE 30-DAY VOLATILITY
# ------------------------------------------------------------

average_volatility = (
    df.groupby("pair")["vol_30d_annualized"]
      .mean()
      .sort_values(ascending=False)
)

print("\n")
print("========== AVERAGE 30-DAY VOLATILITY ==========")

print(
    (average_volatility * 100).round(2)
)


# ------------------------------------------------------------
# 7. MAXIMUM 30-DAY VOLATILITY
# ------------------------------------------------------------

maximum_volatility = (
    df.groupby("pair")["vol_30d_annualized"]
      .max()
      .sort_values(ascending=False)
)

print("\n")
print("========== MAXIMUM 30-DAY VOLATILITY ==========")

print(
    (maximum_volatility * 100).round(2)
)


# ------------------------------------------------------------
# 8. BIGGEST 30-DAY VOLATILITY SPIKE
# ------------------------------------------------------------

idx_30 = (
    df.groupby("pair")[
        "vol_30d_annualized"
    ].idxmax()
)

spikes_30 = df.loc[
    idx_30,
    [
        "date",
        "pair",
        "vol_30d_annualized"
    ]
].sort_values(
    "vol_30d_annualized",
    ascending=False
)

print("\n")
print("========== BIGGEST 30-DAY VOLATILITY SPIKES ==========")

print(
    spikes_30.to_string(index=False)
)


# ------------------------------------------------------------
# 9. BIGGEST 7-DAY VOLATILITY SPIKE
# ------------------------------------------------------------

idx_7 = (
    df.groupby("pair")[
        "vol_7d_annualized"
    ].idxmax()
)

spikes_7 = df.loc[
    idx_7,
    [
        "date",
        "pair",
        "vol_7d_annualized"
    ]
].sort_values(
    "vol_7d_annualized",
    ascending=False
)

print("\n")
print("========== BIGGEST 7-DAY VOLATILITY SPIKES ==========")

print(
    spikes_7.to_string(index=False)
)


# ============================================================
# LONG-TERM TREND ANALYSIS
# ============================================================


# ------------------------------------------------------------
# 10. STARTING AND ENDING EXCHANGE RATE
# ------------------------------------------------------------

trend = (
    df.groupby("pair")
      .agg(
          start_date=("date", "first"),
          end_date=("date", "last"),
          start_rate=("close", "first"),
          end_rate=("close", "last")
      )
      .reset_index()
)


# ------------------------------------------------------------
# 11. EXCHANGE-RATE PERCENTAGE CHANGE
# ------------------------------------------------------------

trend["exchange_rate_change_pct"] = (
    (
        trend["end_rate"]
        - trend["start_rate"]
    )
    / trend["start_rate"]
) * 100


print("\n")
print("========== LONG-TERM TREND ==========")

print(
    trend.to_string(index=False)
)


# ------------------------------------------------------------
# 12. LOCAL CURRENCY VALUE CHANGE
# ------------------------------------------------------------

# Because our pairs are USD/local currency:
#
# USDNGN increasing means NGN is losing value.
#
# This formula estimates the change in the local
# currency's USD value.

trend["local_currency_value_change_pct"] = (
    (
        trend["start_rate"]
        / trend["end_rate"]
    ) - 1
) * 100


print("\n")
print("========== LOCAL CURRENCY VALUE CHANGE ==========")

print(
    trend[
        [
            "pair",
            "local_currency_value_change_pct"
        ]
    ].round(2).to_string(index=False)
)


# ------------------------------------------------------------
# 13. DAILY DIRECTION OF EXCHANGE-RATE MOVEMENT
# ------------------------------------------------------------

df["rate_change"] = (
    df.groupby("pair")["close"].diff()
)

trend_direction = (
    df.groupby("pair")
      .agg(
          positive_days=(
              "rate_change",
              lambda x: (x > 0).sum()
          ),

          negative_days=(
              "rate_change",
              lambda x: (x < 0).sum()
          ),

          unchanged_days=(
              "rate_change",
              lambda x: (x == 0).sum()
          )
      )
      .reset_index()
)


print("\n")
print("========== DIRECTION OF DAILY MOVEMENTS ==========")

print(
    trend_direction.to_string(index=False)
)


# ------------------------------------------------------------
# 14. 30-DAY ROLLING MEAN
# ------------------------------------------------------------

df["close_30d_mean"] = (
    df.groupby("pair")["close"]
      .transform(
          lambda x: x.rolling(
              30,
              min_periods=1
          ).mean()
      )
)

print("\n30-day rolling mean calculated.")


# ------------------------------------------------------------
# 15. CHANGE IN LONG-TERM TREND
# ------------------------------------------------------------

df["trend_change_pct"] = (
    df.groupby("pair")["close_30d_mean"]
      .pct_change() * 100
)


# ------------------------------------------------------------
# 16. SUMMARY TABLE
# ------------------------------------------------------------

summary = (
    trend.merge(
        trend_direction,
        on="pair"
    )
)

summary["average_30d_volatility_pct"] = (
    df.groupby("pair")["vol_30d_annualized"]
      .mean()
      .values * 100
)

summary["maximum_30d_volatility_pct"] = (
    df.groupby("pair")["vol_30d_annualized"]
      .max()
      .values * 100
)

summary["maximum_7d_volatility_pct"] = (
    df.groupby("pair")["vol_7d_annualized"]
      .max()
      .values * 100
)


# ------------------------------------------------------------
# 17. PRINT FINAL SUMMARY
# ------------------------------------------------------------

print("\n")
print("============================================================")
print("FINAL TASK 2 SUMMARY")
print("============================================================")

print(
    summary[
        [
            "pair",
            "start_rate",
            "end_rate",
            "exchange_rate_change_pct",
            "local_currency_value_change_pct",
            "average_30d_volatility_pct",
            "maximum_30d_volatility_pct",
            "maximum_7d_volatility_pct",
            "positive_days",
            "negative_days"
        ]
    ].round(2).to_string(index=False)
)


# ------------------------------------------------------------
# 18. SAVE ALL RESULTS
# ------------------------------------------------------------

df.to_csv(
    "setD_task2_rolling_results.csv",
    index=False
)

trend.to_csv(
    "setD_task2_long_term_trend.csv",
    index=False
)

trend_direction.to_csv(
    "setD_task2_direction.csv",
    index=False
)

summary.to_csv(
    "setD_task2_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 19. FINISHED
# ------------------------------------------------------------

print("\n")
print("============================================================")
print("TASK 2 COMPLETED SUCCESSFULLY")
print("============================================================")

print("\nFiles created:")

print("1. setD_task2_rolling_results.csv")
print("2. setD_task2_long_term_trend.csv")
print("3. setD_task2_direction.csv")
print("4. setD_task2_summary.csv")