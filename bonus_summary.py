import pandas as pd


# ============================================================
# BONUS STEP 4 — FINAL SUMMARY
# ============================================================

df = pd.read_csv(
    "bonus_merged_analysis.csv"
)


# ============================================================
# 1. BASIC COUNTRY SUMMARY
# ============================================================

country_summary = (
    df.groupby("country")
    .agg(
        average_inflation=(
            "inflation_pct",
            "mean"
        ),

        average_gdp_growth=(
            "gdp_growth_pct",
            "mean"
        ),

        average_currency_change=(
            "local_currency_value_change_pct",
            "mean"
        ),

        average_volatility=(
            "annualized_volatility_pct",
            "mean"
        )
    )
    .reset_index()
)


print("\n")
print("=" * 75)
print("BONUS — COUNTRY SUMMARY")
print("=" * 75)

print(
    country_summary.round(2)
    .to_string(index=False)
)


# ============================================================
# 2. MOST VOLATILE COUNTRY
# ============================================================

most_volatile = country_summary.loc[
    country_summary[
        "average_volatility"
    ].idxmax()
]


print("\n")
print("=" * 75)
print("MOST VOLATILE COUNTRY")
print("=" * 75)

print(
    f"{most_volatile['country']} "
    f"→ "
    f"{most_volatile['average_volatility']:.2f}% "
    f"average annualized volatility"
)


# ============================================================
# 3. LARGEST CURRENCY DEPRECIATION
# ============================================================

largest_depreciation = country_summary.loc[
    country_summary[
        "average_currency_change"
    ].idxmin()
]


print("\n")
print("=" * 75)
print("LARGEST CURRENCY DEPRECIATION")
print("=" * 75)

print(
    f"{largest_depreciation['country']} "
    f"→ "
    f"{largest_depreciation['average_currency_change']:.2f}% "
    f"average local-currency value change"
)


# ============================================================
# 4. HIGHEST INFLATION
# ============================================================

highest_inflation = df.loc[
    df["inflation_pct"].idxmax()
]


print("\n")
print("=" * 75)
print("HIGHEST INFLATION OBSERVATION")
print("=" * 75)

print(
    f"{highest_inflation['country']} "
    f"({int(highest_inflation['year'])}) "
    f"→ "
    f"{highest_inflation['inflation_pct']:.2f}%"
)


# ============================================================
# 5. LOWEST GDP GROWTH
# ============================================================

lowest_gdp = df.loc[
    df["gdp_growth_pct"].idxmin()
]


print("\n")
print("=" * 75)
print("LOWEST GDP GROWTH OBSERVATION")
print("=" * 75)

print(
    f"{lowest_gdp['country']} "
    f"({int(lowest_gdp['year'])}) "
    f"→ "
    f"{lowest_gdp['gdp_growth_pct']:.2f}%"
)


# ============================================================
# 6. CORRELATION MATRIX
# ============================================================

columns = [

    "inflation_pct",

    "gdp_growth_pct",

    "local_currency_value_change_pct",

    "annualized_volatility_pct"
]

corr = df[columns].corr()


print("\n")
print("=" * 75)
print("CORRELATION MATRIX")
print("=" * 75)

print(
    corr.round(3)
    .to_string()
)


# ============================================================
# 7. FIND STRONGEST NON-SELF CORRELATION
# ============================================================

pairs = []

for i in range(len(columns)):

    for j in range(i + 1, len(columns)):

        pairs.append({

            "variable_1": columns[i],

            "variable_2": columns[j],

            "correlation":
                corr.iloc[i, j]

        })


correlation_pairs = pd.DataFrame(
    pairs
)

strongest = correlation_pairs.loc[
    correlation_pairs["correlation"]
    .abs()
    .idxmax()
]


print("\n")
print("=" * 75)
print("STRONGEST RELATIONSHIP")
print("=" * 75)

print(
    f"{strongest['variable_1']} "
    f"↔ "
    f"{strongest['variable_2']}"
)

print(
    f"Correlation: "
    f"{strongest['correlation']:.3f}"
)


# ============================================================
# 8. SAVE COUNTRY SUMMARY
# ============================================================

country_summary.to_csv(
    "bonus_country_summary.csv",
    index=False
)


# ============================================================
# 9. FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 75)
print("BONUS TRACK COMPLETED")
print("=" * 75)

print(
    "\nFinal output saved as:"
)

print(
    "bonus_country_summary.csv"
)