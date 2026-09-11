import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# BONUS STEP 3 — VISUALIZATION
# ============================================================

# ------------------------------------------------------------
# 1. LOAD BONUS MERGED DATA
# ------------------------------------------------------------

df = pd.read_csv(
    "bonus_merged_analysis.csv"
)

print("Bonus merged data loaded.")
print("Rows:", len(df))


# ============================================================
# 2. INFLATION VS CURRENCY VALUE CHANGE
# ============================================================

plt.figure(figsize=(10, 6))

for country, group in df.groupby("country"):

    plt.scatter(
        group["inflation_pct"],
        group["local_currency_value_change_pct"],
        label=country,
        s=60
    )

plt.axhline(
    0,
    linewidth=1
)

plt.xlabel("Inflation (%)")

plt.ylabel(
    "Local Currency Value Change (%)"
)

plt.title(
    "Inflation vs Currency Value Change"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "bonus_inflation_vs_currency.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 3. GDP GROWTH VS CURRENCY VALUE CHANGE
# ============================================================

plt.figure(figsize=(10, 6))

for country, group in df.groupby("country"):

    plt.scatter(
        group["gdp_growth_pct"],
        group["local_currency_value_change_pct"],
        label=country,
        s=60
    )

plt.axhline(
    0,
    linewidth=1
)

plt.xlabel(
    "GDP Growth (%)"
)

plt.ylabel(
    "Local Currency Value Change (%)"
)

plt.title(
    "GDP Growth vs Currency Value Change"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "bonus_gdp_vs_currency.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 4. INFLATION VS CURRENCY VOLATILITY
# ============================================================

plt.figure(figsize=(10, 6))

for country, group in df.groupby("country"):

    plt.scatter(
        group["inflation_pct"],
        group["annualized_volatility_pct"],
        label=country,
        s=60
    )

plt.xlabel(
    "Inflation (%)"
)

plt.ylabel(
    "Annualized Currency Volatility (%)"
)

plt.title(
    "Inflation vs Currency Volatility"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "bonus_inflation_vs_volatility.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 5. GDP GROWTH VS CURRENCY VOLATILITY
# ============================================================

plt.figure(figsize=(10, 6))

for country, group in df.groupby("country"):

    plt.scatter(
        group["gdp_growth_pct"],
        group["annualized_volatility_pct"],
        label=country,
        s=60
    )

plt.xlabel(
    "GDP Growth (%)"
)

plt.ylabel(
    "Annualized Currency Volatility (%)"
)

plt.title(
    "GDP Growth vs Currency Volatility"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "bonus_gdp_vs_volatility.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 6. CORRELATION MATRIX
# ============================================================

correlation_columns = [

    "inflation_pct",

    "gdp_growth_pct",

    "local_currency_value_change_pct",

    "annualized_volatility_pct"
]

correlation_matrix = df[
    correlation_columns
].corr()


print("\n")
print("=" * 70)
print("BONUS CORRELATION MATRIX")
print("=" * 70)

print(
    correlation_matrix.round(3)
)


# ============================================================
# 7. SAVE CORRELATION MATRIX
# ============================================================

correlation_matrix.to_csv(
    "bonus_correlation_matrix.csv"
)


# ============================================================
# 8. FINISHED
# ============================================================

print("\n")
print("=" * 70)
print("BONUS STEP 3 COMPLETED")
print("=" * 70)

print("\nCreated files:")

print("1. bonus_inflation_vs_currency.png")

print("2. bonus_gdp_vs_currency.png")

print("3. bonus_inflation_vs_volatility.png")

print("4. bonus_gdp_vs_volatility.png")

print("5. bonus_correlation_matrix.csv")