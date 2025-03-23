import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import os  # ← 環境変数を読み込むために必要！

print("Hello, Turtle!")

# Slack Webhook URL（GitHub Secretsから取得！）
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

# Slackに通知を送る関数
def send_slack_message(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slack通知を送りました")
    else:
        print(f"❌ エラー: {response.status_code}, {response.text}")

# 通貨ペア
symbol = "JPY=X"
name = "USD/JPY"

# データ取得（注意：MultiIndex構造になることがある）
data = yf.download(symbol, period="30d", interval="1d", auto_adjust=True)

# Ticker付きMultiIndexの可能性に対応
if isinstance(data.columns, pd.MultiIndex):
    close_prices = data["Close"][symbol]
    high_prices = data["High"][symbol]
    low_prices = data["Low"][symbol]
else:
    close_prices = data["Close"]
    high_prices = data["High"]
    low_prices = data["Low"]

# 20日高値・安値
high_20_series = high_prices.rolling(window=20).max()
low_20_series = low_prices.rolling(window=20).min()

# 最新のデータ行
latest_date = close_prices.index[-1]
close = close_prices.iloc[-1]
high_20 = high_20_series.iloc[-1]
low_20 = low_20_series.iloc[-1]

# シグナル判定
if close > high_20:
    signal = "📈 買いサイン"
elif close < low_20:
    signal = "📉 売りサイン"
else:
    signal = "⏳ ノーサイン（保留）"

# Slackメッセージの本文
message = f"""
📊 タートルズ戦略通知
--------------------------
通貨ペア：{name}
📅 日付: {latest_date.date()}
📈 終値（Close）: {round(close, 3)}
🔺 20日間の高値: {round(high_20, 3)}
🔻 20日間の安値: {round(low_20, 3)}
📍 シグナル：{signal}
"""

# 通知送信！
send_slack_message(message)
