import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

st.title("🌍 Global Debt Crisis Monitoring System")

tickers = {
    "Emerging Markets ETF": "EEM",
    "Emerging Market Bonds": "EMB",
    "S&P 500": "^GSPC",
    "VIX": "^VIX",
    "Dollar Index Proxy": "UUP",
    "Copper": "HG=F",
    "Oil": "CL=F",
    "Gold": "GC=F",
    "Caterpillar": "CAT",
    "Boeing": "BA",
    "Freeport": "FCX"
}

period = "6mo"
data = {}

for name, ticker in tickers.items():
    df = yf.download(ticker, period=period)

    if df.empty:
        st.warning(f"No data for {name}")
        continue

    # Force series
    price = df["Close"].squeeze()

    data[name] = price

def plot(name):
    if name in data:
        st.subheader(name)
        st.line_chart(data[name])

col1, col2, col3 = st.columns(3)

with col1:
    plot("Emerging Markets ETF")
    plot("Emerging Market Bonds")
    plot("VIX")

with col2:
    plot("Dollar Index Proxy")
    plot("Copper")
    plot("Oil")

with col3:
    plot("Gold")
    plot("Caterpillar")
    plot("Freeport")

st.header("🚨 Crisis Risk Meter")

score = 0

def trend(series):
    pct = series.pct_change().dropna()
    if len(pct) == 0:
        return 0
    return float(pct.tail(5).mean())

if "Dollar Index Proxy" in data and trend(data["Dollar Index Proxy"]) > 0:
    score += 1

if "Emerging Markets ETF" in data and trend(data["Emerging Markets ETF"]) < 0:
    score += 1

if "Emerging Market Bonds" in data and trend(data["Emerging Market Bonds"]) < 0:
    score += 1

if "VIX" in data and float(data["VIX"].tail(5).mean()) > 25:
    score += 1

if "Copper" in data and trend(data["Copper"]) < 0:
    score += 1

if score <= 2:
    st.success(f"Crisis Risk Score: {score} — Normal")

elif score <= 4:
    st.warning(f"Crisis Risk Score: {score} — Stress Building")

else:
    st.error(f"Crisis Risk Score: {score} — High Crisis Risk")
