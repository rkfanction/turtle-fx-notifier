import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

print("Hello, Turtle!")

# Slack Webhook
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

# Google Sheets Credentials from GitHub Secrets
sheet_json = os.environ["GOOGLE_SHEET_CREDENTIALS_JSON"]
creds_dict = json.loads(sheet_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Spreadsheet and worksheet
SPREADSHEET_ID = "1k-WLklz6SuC2Jv9ON5XsVhNXi9hWjNtbmX_PQi3xqvE"
worksheet = client.open_by_key(SPREADSHEET_ID).worksheet("turtle_fx_log")

# Symbol settings
symbol = "JPY=X"
name = "USD/JPY"

# Download data
data = yf.download(symbol, period="30d", interval="1d", auto_adjust=True)

# Handle MultiIndex (for multiple symbols)
if isinstance(data.columns, pd.MultiIndex):
    close_prices = data["Close"][symbol]
    high_prices = data["High"][symbol]
    low_prices = data["Low"][symbol]
else:
    close_prices = data["Close"]
    high_prices = data["High"]
    low_prices = data["Low"]

# Calculate rolling highs/lows
high_20_series = high_prices.rolling(window=20).max()
low_20_series = low_prices.rolling(window=20).min()
low_10_series = low_prices.rolling(window=10).min()
high_10_series = high_prices.rolling(window=10).max()

# Calculate N (20-day average range)
range_series = high_prices - low_prices
N = range_series.rolling(window=20).mean().iloc[-1]

# Get latest data
latest_date = close_prices.index[-1]
close = close_prices.iloc[-1]
high_20 = high_20_series.iloc[-1]
low_20 = low_20_series.iloc[-1]
low_10 = low_10_series.iloc[-1]
high_10 = high_10_series.iloc[-1]

# Signal detection
signal = "⏳ ノーサイン（保留）"
exit_price = "-"
stop_loss = "-"

if close > high_20:
    signal = "📈 買いサイン"
    stop_loss = round(close - 2 * N, 3)
    exit_price = round(low_10, 3)
elif close < low_20:
    signal = "📉 売りサイン"
    stop_loss = round(close + 2 * N, 3)
    exit_price = round(high_10, 3)

# Build Slack message
message = f"""
📊 タートルズ戦略通知
--------------------------
通貨ペア：{name}
📅 日付: {latest_date.date()}
📈 終値（Close）: {round(close, 3)}
🔺 20日間の高値: {round(high_20, 3)}
🔻 20日間の安値: {round(low_20, 3)}
📍 シグナル：{signal}

🛑 損切りライン（2N逆行）: {stop_loss}
🎯 脱出ライン（トレンド終了）: {exit_price}
"""

# Send Slack
def send_slack_message(msg):
    payload = {"text": msg}
    res = requests.post(SLACK_WEBHOOK_URL, json=payload)
    print("Slack送信結果:", res.status_code)

send_slack_message(message)

# Record to Google Sheets
worksheet.append_row([
    latest_date.strftime("%Y/%m/%d"),
    name,
    round(close, 3),
    round(high_20, 3),
    round(low_20, 3),
    signal,
    stop_loss,
    exit_price
])

print("✅ スプレッドシートに記録しました！")
