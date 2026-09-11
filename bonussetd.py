import pandas as pd
import numpy as np

# ============================================================
# BONUS TRACK — SET D
# WORLD BANK + CURRENCY ANALYSIS
# ============================================================

# ============================================================
# 1. LOAD DATA
# ============================================================

wb = pd.read_csv(r"C:\Users\varsh\OneDrive\Desktop\HACK2\day2_wb_setD.csv")

currency = pd.read_csv(r"C:\Users\varsh\OneDrive\Desktop\HACK2\day2_currency_setD.csv")

print("World Bank data loaded:", wb.shape)
print("Currency data loaded:", currency.shape)


# ============================================================
# 2. CLEAN WORLD BANK DATA
# ============================================================

wb["country"] = (
    wb["country"]
    .astype(str)
    .str.strip()
)

wb["country"] = wb["country"].replace({
    "SA": "South Africa"
})

wb["year"] = pd.to_numeric(
    wb["year"],
    errors="coerce"
)

wb["inflation_pct"] = pd.to_numeric(
    wb["inflation_pct"],
    errors="coerce"
)

wb["gdp_growth_pct"] = pd.to_numeric(
    wb["gdp_growth_pct"],
    errors="coerce"
)


# ============================================================
# 3. CLEAN CURRENCY DATA
# ============================================================

currency["pair"] = (
    currency["pair"]
    .astype(str)
    .str.upper()
    .str.strip()
)

currency["pair"] = (
    currency["pair"]
    .str.replace("=X", "", regex=False)
)


# Standardize all pair names
currency["pair"] = currency["pair"].replace({

    "USD/EGP": "USDEGP",

    "USD/NGN": "USDNGN",

    "USDEGP": "USDEGP",

    "USDNGN": "USDNGN",

    "USDZAR": "USDZAR",

    "USDKES": "USDKES"
})


# ============================================================
# 4. CONVERT DATE
# ============================================================

currency["date"] = pd.to_datetime(
    currency["date"],
    errors="coerce"
)

currency = currency.dropna(
    subset=["date"]
).copy()


# ============================================================
# 5. CREATE YEAR
# ============================================================

currency["year"] = (
    currency["date"].dt.year
)


# ============================================================
# 6. REMOVE INVALID NUMERIC VALUES
# ============================================================

numeric_columns = [
    "open",
    "high",
    "low",
    "close"
]

for column in numeric_columns:

    currency[column] = pd.to_numeric(
        currency[column],
        errors="coerce"
    )


currency = currency.dropna(
    subset=["close"]
).copy()


# ============================================================
# 7. DISPLAY STANDARDIZED PAIRS
# ============================================================

print("\nStandardized currency pairs:")

print(
    currency["pair"].value_counts()
)


# ============================================================
# 8. CALCULATE DAILY RETURNS
# ============================================================

currency = currency.sort_values(
    ["pair", "date"]
).reset_index(drop=True)

currency["daily_return"] = (
    currency
    .groupby("pair")["close"]
    .pct_change()
)


# ============================================================
# 9. CALCULATE YEARLY CURRENCY PERFORMANCE
# ============================================================

yearly_currency = []

for (pair, year), group in currency.groupby(
    ["pair", "year"]
):

    group = group.sort_values("date")

    if len(group) < 2:
        continue

    start_rate = group["close"].iloc[0]

    end_rate = group["close"].iloc[-1]

    # Change in exchange rate
    exchange_rate_change = (
        (end_rate - start_rate)
        / start_rate
    ) * 100

    # Change in local currency value
    local_currency_change = (
        (start_rate / end_rate) - 1
    ) * 100

    # Annualized volatility
    volatility = (
        group["daily_return"].std()
        * np.sqrt(252)
        * 100
    )

    yearly_currency.append({

        "pair": pair,

        "year": year,

        "start_rate": start_rate,

        "end_rate": end_rate,

        "exchange_rate_change_pct":
            exchange_rate_change,

        "local_currency_value_change_pct":
            local_currency_change,

        "annualized_volatility_pct":
            volatility,

        "observations":
            len(group)

    })


yearly_currency = pd.DataFrame(
    yearly_currency
)


# ============================================================
# 10. MAP CURRENCY TO COUNTRY
# ============================================================

pair_to_country = {

    "USDZAR": "South Africa",

    "USDEGP": "Egypt",

    "USDNGN": "Nigeria",

    "USDKES": "Kenya"
}

yearly_currency["country"] = (
    yearly_currency["pair"]
    .map(pair_to_country)
)


# ============================================================
# 11. DISPLAY YEARLY CURRENCY RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("YEARLY CURRENCY PERFORMANCE")
print("=" * 70)

print(
    yearly_currency[
        [
            "country",
            "pair",
            "year",
            "start_rate",
            "end_rate",
            "exchange_rate_change_pct",
            "local_currency_value_change_pct",
            "annualized_volatility_pct"
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ============================================================
# 12. MERGE WITH WORLD BANK DATA
# ============================================================

merged = pd.merge(

    yearly_currency,

    wb,

    on=["country", "year"],

    how="inner"

)


# ============================================================
# 13. DISPLAY MERGED DATA
# ============================================================

print("\n")
print("=" * 70)
print("BONUS — MERGED ECONOMIC + CURRENCY DATA")
print("=" * 70)

print(
    merged[
        [
            "country",
            "year",
            "inflation_pct",
            "gdp_growth_pct",
            "exchange_rate_change_pct",
            "local_currency_value_change_pct",
            "annualized_volatility_pct"
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ============================================================
# 14. CORRELATION ANALYSIS
# ============================================================

print("\n")
print("=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)


inflation_corr = merged[
    [
        "inflation_pct",
        "local_currency_value_change_pct"
    ]
].corr().iloc[0, 1]


gdp_corr = merged[
    [
        "gdp_growth_pct",
        "local_currency_value_change_pct"
    ]
].corr().iloc[0, 1]


inflation_vol_corr = merged[
    [
        "inflation_pct",
        "annualized_volatility_pct"
    ]
].corr().iloc[0, 1]


gdp_vol_corr = merged[
    [
        "gdp_growth_pct",
        "annualized_volatility_pct"
    ]
].corr().iloc[0, 1]


print(
    f"Inflation vs Currency Value Change: "
    f"{inflation_corr:.3f}"
)

print(
    f"GDP Growth vs Currency Value Change: "
    f"{gdp_corr:.3f}"
)

print(
    f"Inflation vs Currency Volatility: "
    f"{inflation_vol_corr:.3f}"
)

print(
    f"GDP Growth vs Currency Volatility: "
    f"{gdp_vol_corr:.3f}"
)


# ============================================================
# 15. SAVE RESULTS
# ============================================================

yearly_currency.to_csv(
    "bonus_yearly_currency.csv",
    index=False
)

merged.to_csv(
    "bonus_merged_analysis.csv",
    index=False
)


# ============================================================
# 16. FINISHED
# ============================================================

print("\n")
print("=" * 70)
print("BONUS STEP 2 COMPLETED")
print("=" * 70)
