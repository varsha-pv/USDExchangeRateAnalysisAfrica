import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# TASK 3 — VISUALIZATION
# SET D: ZAR, EGP, NGN, KES

# 1. LOAD CLEANED DATA

df = pd.read_csv(r"C:\Users\varsh\OneDrive\Desktop\HACK2\TASK1\cleaned_setD.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(
    ["pair", "date"]
).reset_index(drop=True)
print("Data loaded successfully.")

# 2. CREATE 30-DAY ROLLING MEAN

df["close_30d_mean"] = (
    df.groupby("pair")["close"]
      .transform(
          lambda x: x.rolling(
              30,
              min_periods=1
          ).mean()
      )
)
print("30-day rolling mean calculated.")

# 3. MATPLOTLIB — EXCHANGE RATE TREND

plt.figure(figsize=(14, 7))
for pair, group in df.groupby("pair"):
    plt.plot(
        group["date"],
        group["close_30d_mean"],
        linewidth=2,
        label=pair
    )

plt.title(
    "Set D — 30-Day Rolling Mean of USD/Local-Currency Exchange Rates"
)

plt.xlabel("Date")

plt.ylabel(
    "Exchange Rate (Local Currency per USD)"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "setD_trend_chart.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print("Trend chart saved as setD_trend_chart.png")


# ============================================================
# 4. CREATE 30-DAY VOLATILITY
# ============================================================

df["daily_return"] = (
    df.groupby("pair")["close"].pct_change()
)

df["vol_30d"] = (
    df.groupby("pair")["daily_return"]
      .transform(
          lambda x: x.rolling(30).std()
      )
)

df["vol_30d_annualized"] = (
    df["vol_30d"] * np.sqrt(252)
)

df["vol_30d_percent"] = (
    df["vol_30d_annualized"] * 100
)


# ============================================================
# 5. MATPLOTLIB — VOLATILITY CHART
# ============================================================

plt.figure(figsize=(14, 7))

for pair, group in df.groupby("pair"):

    plt.plot(
        group["date"],
        group["vol_30d_percent"],
        linewidth=1.8,
        label=pair
    )

plt.title(
    "Set D — 30-Day Rolling Annualized Volatility"
)

plt.xlabel("Date")

plt.ylabel(
    "Annualized Volatility (%)"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "setD_volatility_chart.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print(
    "Volatility chart saved as setD_volatility_chart.png"
)


# ============================================================
# 6. COUNTRY INFORMATION FOR MAP
# ============================================================

countries = {

    "USDZAR": {
        "country": "South Africa",
        "currency": "ZAR",
        "lat": -30.5595,
        "lon": 22.9375,
        "color": "blue"
    },

    "USDEGP": {
        "country": "Egypt",
        "currency": "EGP",
        "lat": 26.8206,
        "lon": 30.8025,
        "color": "green"
    },

    "USDNGN": {
        "country": "Nigeria",
        "currency": "NGN",
        "lat": 9.0820,
        "lon": 8.6753,
        "color": "red"
    },

    "USDKES": {
        "country": "Kenya",
        "currency": "KES",
        "lat": -0.0236,
        "lon": 37.9062,
        "color": "purple"
    }
}


# ============================================================
# 7. CALCULATE CURRENCY PERFORMANCE
# ============================================================

map_results = []

for pair, group in df.groupby("pair"):

    start_rate = group["close"].iloc[0]

    end_rate = group["close"].iloc[-1]

    # Change in USD/local-currency exchange rate
    exchange_rate_change = (
        (end_rate - start_rate)
        / start_rate
    ) * 100

    # Change in local currency's value relative to USD
    local_currency_change = (
        (start_rate / end_rate) - 1
    ) * 100

    # Maximum 30-day volatility
    max_volatility = (
        group["vol_30d_annualized"].max()
        * 100
    )

    info = countries[pair]

    map_results.append({

        "pair": pair,

        "country": info["country"],

        "currency": info["currency"],

        "start_rate": start_rate,

        "end_rate": end_rate,

        "exchange_rate_change_pct":
            exchange_rate_change,

        "local_currency_value_change_pct":
            local_currency_change,

        "maximum_30d_volatility_pct":
            max_volatility,

        "lat": info["lat"],

        "lon": info["lon"]

    })


map_df = pd.DataFrame(map_results)


# ============================================================
# 8. PRINT MAP SUMMARY
# ============================================================

print("\n")
print("============================================================")
print("TASK 3 — CURRENCY PERFORMANCE")
print("============================================================")

print(
    map_df[
        [
            "pair",
            "country",
            "currency",
            "start_rate",
            "end_rate",
            "exchange_rate_change_pct",
            "local_currency_value_change_pct",
            "maximum_30d_volatility_pct"
        ]
    ].round(2).to_string(index=False)
)


# ============================================================
# 9. CREATE FOLIUM MAP
# ============================================================

currency_map = folium.Map(

    location=[8, 25],

    zoom_start=3,

    tiles="CartoDB positron"

)


# ============================================================
# 10. ADD CURRENCY MARKERS
# ============================================================

for _, row in map_df.iterrows():

    pair = row["pair"]

    info = countries[pair]

    popup_text = f"""
    <b>{info['country']} — {info['currency']}</b><br><br>

    Currency Pair: {pair}<br>

    Starting Rate:
    {row['start_rate']:.4f}<br>

    Ending Rate:
    {row['end_rate']:.4f}<br>

    Exchange Rate Change:
    {row['exchange_rate_change_pct']:.2f}%<br>

    Local Currency Value Change:
    {row['local_currency_value_change_pct']:.2f}%<br>

    Maximum 30-Day Volatility:
    {row['maximum_30d_volatility_pct']:.2f}%
    """

    folium.Marker(

        location=[
            info["lat"],
            info["lon"]
        ],

        tooltip=(
            f"{info['country']} "
            f"({info['currency']})"
        ),

        popup=folium.Popup(
            popup_text,
            max_width=350
        ),

        icon=folium.Icon(

            color=info["color"],

            icon="usd",

            prefix="fa"

        )

    ).add_to(currency_map)


# ============================================================
# 11. SAVE MAP
# ============================================================

currency_map.save(
    "setD_currency_map.html"
)

print(
    "\nFolium map saved as setD_currency_map.html"
)


# ============================================================
# 12. SAVE MAP DATA
# ============================================================

map_df.to_csv(
    "setD_map_summary.csv",
    index=False
)

print(
    "Map summary saved as setD_map_summary.csv"
)


# ============================================================
# 13. FINISHED
# ============================================================

print("\n")
print("============================================================")
print("TASK 3 COMPLETED SUCCESSFULLY")
print("============================================================")

print("\nFiles created:")

print("1. setD_trend_chart.png")
print("2. setD_volatility_chart.png")
print("3. setD_currency_map.html")
print("4. setD_map_summary.csv")