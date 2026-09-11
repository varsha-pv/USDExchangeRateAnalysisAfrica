import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pathlib import Path

# TASK 4 — STREAMLIT DASHBOARD
# SET D CURRENCY WATCH

st.set_page_config(
    page_title="Currency Watch — Set D",
    page_icon="💱",
    layout="wide"
)

# TITLE

st.title("💱 Currency Watch — Set D")
st.markdown(
    "Interactive dashboard for ZAR, EGP, NGN and KES "
    "exchange-rate analysis."
)
st.divider()

# LOAD DATA

@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "cleaned_setD.csv"

    df = pd.read_csv(csv_path, parse_dates=["date"])

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(
        ["pair", "date"]
    ).reset_index(drop=True)

    # Daily returns
    df["daily_return"] = (
        df.groupby("pair")["close"].pct_change()
    )

    # 7-day rolling volatility
    df["vol_7d"] = (
        df.groupby("pair")["daily_return"]
          .transform(
              lambda x: x.rolling(7).std()
          )
    )

    # 30-day rolling volatility
    df["vol_30d"] = (
        df.groupby("pair")["daily_return"]
          .transform(
              lambda x: x.rolling(30).std()
          )
    )

    # Annualized volatility
    df["vol_7d_annualized"] = (
        df["vol_7d"] * np.sqrt(252)
    )

    df["vol_30d_annualized"] = (
        df["vol_30d"] * np.sqrt(252)
    )

    # Percent values
    df["vol_7d_percent"] = (
        df["vol_7d_annualized"] * 100
    )

    df["vol_30d_percent"] = (
        df["vol_30d_annualized"] * 100
    )

    # 30-day rolling mean
    df["close_30d_mean"] = (
        df.groupby("pair")["close"]
          .transform(
              lambda x: x.rolling(
                  30,
                  min_periods=1
              ).mean()
          )
    )

    return df

df = load_data()

# COUNTRY INFORMATION

country_info = {

    "USDZAR": {
        "country": "South Africa",
        "currency": "ZAR",
        "lat": -30.5595,
        "lon": 22.9375
    },

    "USDEGP": {
        "country": "Egypt",
        "currency": "EGP",
        "lat": 26.8206,
        "lon": 30.8025
    },

    "USDNGN": {
        "country": "Nigeria",
        "currency": "NGN",
        "lat": 9.0820,
        "lon": 8.6753
    },

    "USDKES": {
        "country": "Kenya",
        "currency": "KES",
        "lat": -0.0236,
        "lon": 37.9062
    }
}

# SIDEBAR

st.sidebar.header("⚙️ Dashboard Controls")
pairs = sorted(df["pair"].dropna().unique())
selected_pair = st.sidebar.selectbox(
    "Select Currency Pair",
    pairs
)
pair_data = df[
    df["pair"] == selected_pair
].copy()

# Date range

min_date = pair_data["date"].min().date()
max_date = pair_data["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Make sure two dates are selected
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_data = pair_data[
        (pair_data["date"] >= start_date) &
        (pair_data["date"] <= end_date)
    ].copy()

else:

    filtered_data = pair_data.copy()

# SELECTED COUNTRY

selected_country = country_info.get(
    selected_pair,
    {
        "country": "Unknown",
        "currency": selected_pair
    }
)

st.subheader(
    f"{selected_country['country']} — {selected_pair}"
)

# KEY METRICS

if len(filtered_data) > 0:

    current_rate = filtered_data["close"].iloc[-1]

    start_rate = filtered_data["close"].iloc[0]

    end_rate = filtered_data["close"].iloc[-1]

    period_change = (
        (end_rate - start_rate)
        / start_rate
    ) * 100

    avg_volatility = (
        filtered_data["vol_30d_annualized"]
        .mean()
        * 100
    )

    max_volatility = (
        filtered_data["vol_30d_annualized"]
        .max()
        * 100
    )

else:

    current_rate = 0
    period_change = 0
    avg_volatility = 0
    max_volatility = 0


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Latest Exchange Rate",
        f"{current_rate:.4f}"
    )

with col2:

    st.metric(
        "Period Change",
        f"{period_change:.2f}%"
    )

with col3:

    st.metric(
        "Average 30-Day Volatility",
        f"{avg_volatility:.2f}%"
    )

with col4:

    st.metric(
        "Maximum 30-Day Volatility",
        f"{max_volatility:.2f}%"
    )


st.divider()



# TABS


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Exchange Rate",
        "📊 Volatility",
        "🌍 Currency Comparison",
        "🗺️ Map"
    ]
)



# TAB 1 — EXCHANGE RATE


with tab1:

    st.subheader("Exchange Rate Trend")

    fig = px.line(
        filtered_data,
        x="date",
        y="close",
        title=f"{selected_pair} Exchange Rate",
        labels={
            "date": "Date",
            "close": "Local Currency per USD"
        }
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("30-Day Rolling Trend")

    fig_trend = px.line(
        filtered_data,
        x="date",
        y="close_30d_mean",
        title=f"{selected_pair} — 30-Day Rolling Mean",
        labels={
            "date": "Date",
            "close_30d_mean": "30-Day Rolling Mean"
        }
    )

    fig_trend.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )



# TAB 2 — VOLATILITY


with tab2:

    st.subheader("Rolling Volatility")

    volatility_data = filtered_data[
        [
            "date",
            "vol_7d_percent",
            "vol_30d_percent"
        ]
    ].copy()

    volatility_data = volatility_data.dropna()

    fig_vol = px.line(
        volatility_data,
        x="date",
        y=[
            "vol_7d_percent",
            "vol_30d_percent"
        ],
        title=f"{selected_pair} — Rolling Volatility",
        labels={
            "date": "Date",
            "value": "Annualized Volatility (%)",
            "variable": "Window"
        }
    )

    fig_vol.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_vol,
        use_container_width=True
    )


    # Biggest volatility spike

    st.subheader("Largest Volatility Spike")

    max_row = filtered_data.loc[
        filtered_data["vol_7d_annualized"].idxmax()
    ]

    spike_col1, spike_col2 = st.columns(2)

    with spike_col1:

        st.metric(
            "Maximum 7-Day Volatility",
            f"{max_row['vol_7d_percent']:.2f}%"
        )

    with spike_col2:

        st.metric(
            "Spike Date",
            max_row["date"].strftime("%Y-%m-%d")
        )



# TAB 3 — CURRENCY COMPARISON


with tab3:

    st.subheader(
        "30-Day Volatility Comparison"
    )

    comparison = (
        df.groupby("pair")[
            "vol_30d_annualized"
        ]
        .mean()
        .reset_index()
    )

    comparison["volatility_percent"] = (
        comparison["vol_30d_annualized"] * 100
    )

    comparison["country"] = (
        comparison["pair"].map(
            lambda x:
            country_info[x]["country"]
        )
    )

    fig_compare = px.bar(
        comparison,
        x="pair",
        y="volatility_percent",
        hover_data=["country"],
        title="Average 30-Day Annualized Volatility",
        labels={
            "pair": "Currency Pair",
            "volatility_percent":
                "Volatility (%)"
        }
    )

    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )


    st.subheader(
        "Currency Performance Summary"
    )

    summary_rows = []

    for pair, group in df.groupby("pair"):

        start = group["close"].iloc[0]

        end = group["close"].iloc[-1]

        exchange_change = (
            (end - start) / start
        ) * 100

        local_change = (
            (start / end) - 1
        ) * 100

        avg_vol = (
            group["vol_30d_annualized"]
            .mean() * 100
        )

        max_vol = (
            group["vol_30d_annualized"]
            .max() * 100
        )

        summary_rows.append({

            "Pair": pair,

            "Country":
                country_info[pair]["country"],

            "Start Rate":
                round(start, 4),

            "End Rate":
                round(end, 4),

            "Exchange Rate Change (%)":
                round(exchange_change, 2),

            "Local Currency Value Change (%)":
                round(local_change, 2),

            "Average 30D Volatility (%)":
                round(avg_vol, 2),

            "Maximum 30D Volatility (%)":
                round(max_vol, 2)
        })


    summary_df = pd.DataFrame(
        summary_rows
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )



# TAB 4 — FOLIUM MAP


with tab4:

    st.subheader(
        "🌍 Currency Performance Map"
    )

    currency_map = folium.Map(

        location=[8, 25],

        zoom_start=3,

        tiles="CartoDB positron"
    )


    for pair, info in country_info.items():

        pair_data_map = df[
            df["pair"] == pair
        ].copy()

        if len(pair_data_map) == 0:
            continue

        start = pair_data_map[
            "close"
        ].iloc[0]

        end = pair_data_map[
            "close"
        ].iloc[-1]

        exchange_change = (
            (end - start) / start
        ) * 100

        local_change = (
            (start / end) - 1
        ) * 100

        avg_vol = (
            pair_data_map[
                "vol_30d_annualized"
            ].mean()
            * 100
        )

        popup = f"""
        <b>{info['country']}</b><br>
        Currency: {info['currency']}<br>
        Pair: {pair}<br><br>

        Start Rate: {start:.4f}<br>
        End Rate: {end:.4f}<br>

        Exchange Rate Change:
        {exchange_change:.2f}%<br>

        Local Currency Value Change:
        {local_change:.2f}%<br>

        Average 30-Day Volatility:
        {avg_vol:.2f}%
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
                popup,
                max_width=350
            ),

            icon=folium.Icon(
                icon="usd",
                prefix="fa"
            )
        ).add_to(currency_map)


    st_folium(
        currency_map,
        width=1200,
        height=600
    )



# BOTTOM INFORMATION


st.divider()

st.caption(
    "Set D Currency Watch | "
    "Rolling volatility is annualized using √252."
)