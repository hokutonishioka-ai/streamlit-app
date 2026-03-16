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
    "Dollar Index": "DX-Y.NYB",
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
    data[name] = df["Close"]

def plot(name):
    st.subheader(name)
    st.line_chart(data[name])

col1, col2, col3 = st.columns(3)

with col1:
    plot("Emerging Markets ETF")
    plot("Emerging Market Bonds")
    plot("VIX")

with col2:
    plot("Dollar Index")
    plot("Copper")
    plot("Oil")

with col3:
    plot("Gold")
    plot("Caterpillar")
    plot("Freeport")

st.header("Crisis Risk Meter")

score = 0

if data["Dollar Index"].pct_change().mean() > 0:
    score += 1

if data["Emerging Markets ETF"].pct_change().mean() < 0:
    score += 1

if data["Emerging Market Bonds"].pct_change().mean() < 0:
    score += 1

if data["VIX"].mean() > 25:
    score += 1

if data["Copper"].pct_change().mean() < 0:
    score += 1

if score <= 2:
    st.success(f"Crisis Risk Score: {score} — Normal")

elif score <= 4:
    st.warning(f"Crisis Risk Score: {score} — Stress Building")

else:
    st.error(f"Crisis Risk Score: {score} — High Crisis Risk")