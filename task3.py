import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# ============================================
# SET D - TASK 3: VISUALIZATION
# ============================================

df = pd.read_csv(r"C:\Users\varsh\OneDrive\Desktop\HACK2\TASK1\cleaned_setD.csv", parse_dates=["date"])
df = df.sort_values(["pair", "date"]).reset_index(drop=True)

# --------------------------------------------
# A. MATPLOTLIB TREND LINES
# --------------------------------------------
# A 30-day rolling mean makes the long-term
# trend easier to see and reduces daily noise.
df["close_30d_mean"] = (
    df.groupby("pair")["close"]
      .transform(lambda x: x.rolling(30, min_periods=1).mean())
)

plt.figure(figsize=(14, 7))

for pair, g in df.groupby("pair"):
    plt.plot(
        g["date"],
        g["close_30d_mean"],
        label=pair,
        linewidth=2
    )

plt.title("Set D — 30-Day Rolling Mean of USD/Local-Currency Exchange Rates")
plt.xlabel("Date")
plt.ylabel("Exchange Rate (Local Currency per USD)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("setD_trend_chart.png", dpi=200, bbox_inches="tight")
plt.show()

# --------------------------------------------
# B. FOLIUM MAP
# --------------------------------------------
countries = {
    "USDZAR": {"country": "South Africa", "currency": "ZAR",
               "lat": -30.5595, "lon": 22.9375},
    "USDEGP": {"country": "Egypt", "currency": "EGP",
               "lat": 26.8206, "lon": 30.8025},
    "USDNGN": {"country": "Nigeria", "currency": "NGN",
               "lat": 9.0820, "lon": 8.6753},
    "USDKES": {"country": "Kenya", "currency": "KES",
               "lat": -0.0236, "lon": 37.9062}
}

marker_colors = {
    "USDZAR": "blue",
    "USDEGP": "green",
    "USDNGN": "red",
    "USDKES": "purple"
}

m = folium.Map(
    location=[8, 25],
    zoom_start=3,
    tiles="CartoDB positron"
)

for pair, g in df.groupby("pair"):
    start_rate = g.iloc[0]["close"]
    end_rate = g.iloc[-1]["close"]

    # Actual percentage change in local currency value in USD:
    local_value_change = (start_rate / end_rate - 1) * 100

    exchange_rate_change = (end_rate / start_rate - 1) * 100

    info = countries[pair]

    popup = f"""
    <b>{info['country']} ({info['currency']})</b><br>
    Pair: {pair}<br>
    Start rate: {start_rate:.4f}<br>
    End rate: {end_rate:.4f}<br>
    Exchange-rate change: {exchange_rate_change:.2f}%<br>
    Local currency value change: {local_value_change:.2f}%
    """

    folium.Marker(
        [info["lat"], info["lon"]],
        popup=folium.Popup(popup, max_width=350),
        tooltip=f"{info['country']} — {info['currency']}",
        icon=folium.Icon(
            color=marker_colors[pair],
            icon="usd",
            prefix="fa"
        )
    ).add_to(m)

m.save("setD_currency_map.html")
print("Created setD_currency_map.html")