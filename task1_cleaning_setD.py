import pandas as pd
import numpy as np
import re

INPUT = "day2_currency_setD.csv"
OUTPUT = "cleaned_setD.csv"

df = pd.read_csv(INPUT)

def clean_pair(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip().upper().replace("=X", "").replace("/", "")
    mapping = {
        "USDZAR": "USDZAR",
        "USDEGP": "USDEGP",
        "USDNGN": "USDNGN",
        "USDKES": "USDKES",
    }
    return mapping.get(x, x)

df["pair"] = df["pair"].apply(clean_pair)

def parse_mixed_date(x):
    s = str(x).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} 00:00:00", s):
        return pd.to_datetime(s, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s):
        return pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", s):
        return pd.to_datetime(s, format="%m-%d-%Y", errors="coerce")
    if re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", s):
        return pd.to_datetime(s, format="%Y.%m.%d", errors="coerce")
    return pd.to_datetime(s, errors="coerce")

df["date"] = df["date"].apply(parse_mixed_date)

df["close"] = (
    df["close"].astype("string")
    .str.replace(",", "", regex=False)
    .str.strip()
)
df["close"] = pd.to_numeric(df["close"], errors="coerce")

# Remove duplicate observations after normalizing pair/date.
df = df.drop_duplicates(subset=["date", "pair"], keep="first")

df = df.sort_values(["pair", "date"]).reset_index(drop=True)

# Detect obvious one-day ~10x fat-finger errors.
df["prev_close"] = df.groupby("pair")["close"].shift(1)
df["next_close"] = df.groupby("pair")["close"].shift(-1)

outlier_mask = (
    df["close"].notna()
    & df["prev_close"].notna()
    & df["next_close"].notna()
    & (
        ((df["close"] > 5 * df["prev_close"]) & (df["close"] > 5 * df["next_close"]))
        | ((df["close"] < df["prev_close"] / 5) & (df["close"] < df["next_close"] / 5))
    )
)

df.loc[outlier_mask, "close"] = (
    df.loc[outlier_mask, "prev_close"] + df.loc[outlier_mask, "next_close"]
) / 2

# Do not invent missing closing prices.
# Drop rows whose close is still missing because close is required for
# daily-return and volatility calculations.
df = df.loc[df["close"].notna()].copy()

df = df.drop(columns=["prev_close", "next_close"])
df = df.sort_values(["pair", "date"]).reset_index(drop=True)
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

df.to_csv(OUTPUT, index=False)
print("Cleaned dataset saved as:", OUTPUT)
print("Rows:", len(df))
print("Pairs:", df["pair"].unique())