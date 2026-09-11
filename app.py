import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit.components.v1 import html
from pathlib import Path

# CURRENCY WATCH — SET D
# Streamlit Dashboard


st.set_page_config(
    page_title="Currency Watch — Set D",
    page_icon="💱",
    layout="wide"
)

# ---------- Load data ----------
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "cleaned_setD.csv"

    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df.sort_values(["pair", "date"]).reset_index(drop=True)

    df["daily_return"] = (
        df.groupby("pair")["close"].pct_change()
    )

    df["vol_7d"] = (
        df.groupby("pair")["daily_return"]
        .transform(lambda x: x.rolling(7).std())
    )

    df["vol_30d"] = (
        df.groupby("pair")["daily_return"]
        .transform(lambda x: x.rolling(30).std())
    )

    df["vol_30d_annualized"] = df["vol_30d"] * np.sqrt(252)

    return df


@st.cache_data
def make_summary(df):
    rows = []

    for pair, g in df.groupby("pair"):
        returns = g["daily_return"].dropna()
        start_close = g["close"].iloc[0]
        end_close = g["close"].iloc[-1]

        rows.append({
            "pair": pair,
            "start_close": start_close,
            "end_close": end_close,
            "pair_change": (end_close / start_close - 1) * 100,
            "currency_value_change":
                (start_close / end_close - 1) * 100,
            "annualized_volatility":
                returns.std() * np.sqrt(252),
            "avg_30d_volatility":
                g["vol_30d_annualized"].mean() * 100,
            "max_30d_volatility":
                g["vol_30d_annualized"].max() * 100
        })

    return pd.DataFrame(rows)


df = load_data()
summary = make_summary(df)

# ---------- Country metadata ----------
country_info = {
    "USDZAR": {
        "country": "South Africa",
        "currency": "ZAR",
        "flag": "🇿🇦",
        "lat": -30.5595,
        "lon": 22.9375,
        "color": "blue"
    },
    "USDEGP": {
        "country": "Egypt",
        "currency": "EGP",
        "flag": "🇪🇬",
        "lat": 26.8206,
        "lon": 30.8025,
        "color": "green"
    },
    "USDNGN": {
        "country": "Nigeria",
        "currency": "NGN",
        "flag": "🇳🇬",
        "lat": 9.0820,
        "lon": 8.6753,
        "color": "red"
    },
    "USDKES": {
        "country": "Kenya",
        "currency": "KES",
        "flag": "🇰🇪",
        "lat": -0.0236,
        "lon": 37.9062,
        "color": "purple"
    }
}


# HEADER


st.title("💱 Currency Watch")
st.subheader("Set D — Africa: ZAR • EGP • NGN • KES")

st.markdown(
    "### Focus question\n"
    "**Which currency shows a steady long-term slide versus sudden shocks, "
    "and what is the practical difference for a business holding that currency?**"
)

st.divider()


# TOP-LEVEL FINDINGS


most_volatile = summary.loc[
    summary["annualized_volatility"].idxmax()
]
least_volatile = summary.loc[
    summary["annualized_volatility"].idxmin()
]
best = summary.loc[
    summary["currency_value_change"].idxmax()
]
worst = summary.loc[
    summary["currency_value_change"].idxmin()
]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Most Volatile",
        most_volatile["pair"],
        f'{most_volatile["annualized_volatility"]:.2f}%'
    )

with c2:
    st.metric(
        "Least Volatile",
        least_volatile["pair"],
        f'{least_volatile["annualized_volatility"]:.2f}%'
    )

with c3:
    st.metric(
        "Best Currency",
        best["pair"],
        f'{best["currency_value_change"]:.2f}% value change'
    )

with c4:
    st.metric(
        "Worst Currency",
        worst["pair"],
        f'{worst["currency_value_change"]:.2f}% value change'
    )


# SIDEBAR


st.sidebar.header("Dashboard Controls")

pair = st.sidebar.selectbox(
    "Select currency",
    list(country_info.keys()),
    format_func=lambda x:
        f'{country_info[x]["flag"]} {country_info[x]["currency"]} — {country_info[x]["country"]}'
)

window = st.sidebar.radio(
    "Volatility window",
    ["7-day", "30-day"],
    index=1
)

selected = df[df["pair"] == pair].copy()
info = country_info[pair]
selected_summary = summary[summary["pair"] == pair].iloc[0]


# SELECTED CURRENCY


st.header(
    f'{info["flag"]} {info["currency"]} — {info["country"]}'
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Starting Rate",
        f'{selected_summary["start_close"]:,.4f}'
    )

with m2:
    st.metric(
        "Ending Rate",
        f'{selected_summary["end_close"]:,.4f}'
    )

with m3:
    st.metric(
        "Exchange-rate Change",
        f'{selected_summary["pair_change"]:.2f}%'
    )

with m4:
    st.metric(
        "Currency Value Change",
        f'{selected_summary["currency_value_change"]:.2f}%'
    )


# TREND CHART


st.subheader("Exchange-rate Trend")

fig, ax = plt.subplots(figsize=(12, 5))

rolling_mean = selected["close"].rolling(30, min_periods=1).mean()

ax.plot(
    selected["date"],
    selected["close"],
    linewidth=0.8,
    alpha=0.35,
    label="Daily close"
)

ax.plot(
    selected["date"],
    rolling_mean,
    linewidth=2,
    label="30-day rolling mean"
)

ax.set_xlabel("Date")
ax.set_ylabel("Local currency per USD")
ax.set_title(f"{pair} — Exchange Rate")
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


# VOLATILITY CHART


st.subheader("Rolling Volatility")

vol_col = "vol_7d" if window == "7-day" else "vol_30d"

fig2, ax2 = plt.subplots(figsize=(12, 4))

ax2.plot(
    selected["date"],
    selected[vol_col] * np.sqrt(252) * 100,
    linewidth=1.5
)

ax2.set_xlabel("Date")
ax2.set_ylabel("Annualized volatility (%)")
ax2.set_title(f"{pair} — {window} Rolling Annualized Volatility")
ax2.grid(True, alpha=0.3)

fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)


# COMPARISON TABLE


st.subheader("Set D — Currency Comparison")

display_summary = summary.copy()
display_summary["Country"] = display_summary["pair"].map(
    lambda x: country_info[x]["country"]
)
display_summary["Currency"] = display_summary["pair"].map(
    lambda x: country_info[x]["currency"]
)

display_summary = display_summary[
    [
        "Country",
        "Currency",
        "pair",
        "annualized_volatility",
        "avg_30d_volatility",
        "currency_value_change"
    ]
].rename(columns={
    "pair": "Pair",
    "annualized_volatility": "Annualized Volatility (%)",
    "avg_30d_volatility": "Avg 30D Volatility (%)",
    "currency_value_change": "Currency Value Change (%)"
})

display_summary["Annualized Volatility (%)"] = (
    display_summary["Annualized Volatility (%)"].round(2)
)
display_summary["Avg 30D Volatility (%)"] = (
    display_summary["Avg 30D Volatility (%)"].round(2)
)
display_summary["Currency Value Change (%)"] = (
    display_summary["Currency Value Change (%)"].round(2)
)

st.dataframe(
    display_summary,
    use_container_width=True,
    hide_index=True
)


# FOLIUM MAP


st.subheader("Africa Currency Performance Map")

m = folium.Map(
    location=[8, 25],
    zoom_start=3,
    tiles="CartoDB positron"
)

for _, row in summary.iterrows():
    p = row["pair"]
    info2 = country_info[p]

    popup = f"""
    <b>{info2['country']} ({info2['currency']})</b><br>
    Pair: {p}<br>
    Starting rate: {row['start_close']:.4f}<br>
    Ending rate: {row['end_close']:.4f}<br>
    Exchange-rate change: {row['pair_change']:.2f}%<br>
    Local currency value change: {row['currency_value_change']:.2f}%<br>
    Annualized volatility: {row['annualized_volatility']:.2f}%
    """

    folium.Marker(
        location=[info2["lat"], info2["lon"]],
        tooltip=f'{info2["flag"]} {info2["country"]} — {info2["currency"]}',
        popup=folium.Popup(popup, max_width=350),
        icon=folium.Icon(
            color=info2["color"],
            icon="usd",
            prefix="fa"
        )
    ).add_to(m)

html(
    m.get_root().render(),
    height=500,
    scrolling=False
)


# FOCUS QUESTION


st.subheader("What the Data Suggests")

st.markdown(
    f"""
**Most volatile:** {most_volatile["pair"]} at
**{most_volatile["annualized_volatility"]:.2f}% annualized volatility.**

**Least volatile:** {least_volatile["pair"]} at
**{least_volatile["annualized_volatility"]:.2f}% annualized volatility.

**Largest depreciation:** {worst["pair"]}, whose USD/local-currency
exchange rate increased by **{abs(worst["pair_change"]):.2f}%** over the
period.

**Smallest depreciation:** {best["pair"]}, whose exchange rate increased
by **{abs(best["pair_change"]):.2f}%**.

For a business, a **steady depreciation** makes imported goods, foreign
currency payments and USD-denominated costs progressively more expensive.
**Sudden shocks** create a different problem: the business has less time
to adjust prices, hedge exposure, renegotiate contracts or convert cash.
"""
)


# DATA QUALITY NOTE


with st.expander("Data cleaning decisions — Task 1"):
    st.write(
        "The raw Set D file contained 3,013 rows. The cleaning process "
        "standardized mixed date formats and currency-pair names, converted "
        "close values to numeric, removed 6 duplicate observations, corrected "
        "5 obvious approximately 10× fat-finger errors using neighboring valid "
        "prices, and removed 60 rows with missing close values. The resulting "
        "dataset contains 2,947 observations."
    )

st.caption(
    "Currency Watch — Set D | Built for the Evaluated Hackathon"
)