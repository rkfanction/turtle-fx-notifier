# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OcumFWSeb-geZ5i8ZKcpb4xQgxkyrn7H
"""

print("Hello, Turtle!")

# 必要なライブラリをインストール（初回だけ必要）
#!pip install yfinance pandas matplotlib

# ライブラリを読み込み
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# USDJPY（ドル円）の過去30日分のデータを取得
data = yf.download("JPY=X", period="30d", interval="1d")

# データの最初の5行を表示
print(data.head())

# 終値（Close）のチャートを描画
data["Close"].plot(title="USD/JPY - 過去30日間の終値チャート")
plt.xlabel("日付")
plt.ylabel("円")
plt.grid(True)
plt.show()

# 20日間の最高値と最安値を計算して、データに追加
data["20日高値"] = data["High"].rolling(window=20).max()
data["20日安値"] = data["Low"].rolling(window=20).min()

# 最新のローソク足と、20日高値・安値を表示
latest = data.iloc[-1]
print("📅 日付:", latest.name.date())
print("📈 終値（Close）:", latest["Close"])
print("🔺 20日間の高値:", latest["20日高値"])
print("🔻 20日間の安値:", latest["20日安値"])

import requests

# あなたのWebhook URLに置き換えてください（""の中だけ）
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Slackに通知を送る関数
def send_slack_message(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slackに通知を送りました！")
    else:
        print(f"❌ エラー: {response.status_code}, {response.text}")

# テスト通知を送ってみる
send_slack_message("📢 テスト通知です！ColabからSlackに送信成功！")

# 必要なライブラリをインストール（初回のみ）
!pip install yfinance pandas requests

# ライブラリ読み込み
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# Slack Webhook URL（あなたのに差し替えてください）
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Slackに通知を送る関数
def send_slack_message(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slack通知を送りました")
    else:
        print(f"❌ 通知失敗: {response.status_code} - {response.text}")

# 通貨ペア設定（Yahoo FinanceでUSD/JPYは "JPY=X"）
symbol = "JPY=X"
name = "USD/JPY"

# データ取得（過去30日、1日足）
data = yf.download(symbol, period="30d", interval="1d")
data.dropna(inplace=True)  # 欠損値を削除

# 高値・安値のブレイク判定
data["20日高値"] = data["High"].rolling(window=20).max()
data["20日安値"] = data["Low"].rolling(window=20).min()

latest = data.iloc[-1]
today = latest.name.date()
close = latest["Close"]
high_20 = latest["20日高値"]
low_20 = latest["20日安値"]

# シグナル判定
signal = None
if close > high_20:
    signal = "📈 買いサイン"
elif close < low_20:
    signal = "📉 売りサイン"
else:
    signal = "⏳ ノーサイン（保留）"

# Slack通知本文作成
message = f"""
📊 タートルズ戦略通知
--------------------------
通貨ペア：{name}
日付：{today}
現在価格：{round(close, 3)}
20日高値：{round(high_20, 3)}
20日安値：{round(low_20, 3)}
シグナル：{signal}
"""

# 通知送信
send_slack_message(message)

# 必要なライブラリをインストール（初回のみ）
!pip install yfinance pandas requests

# ライブラリ読み込み
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# Slack Webhook URL（あなたのに差し替えてください）
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Slackに通知を送る関数
def send_slack_message(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slack通知を送りました")
    else:
        print(f"❌ 通知失敗: {response.status_code} - {response.text}")

# 通貨ペア設定（Yahoo FinanceでUSD/JPYは "JPY=X"）
symbol = "JPY=X"
name = "USD/JPY"

# データ取得（過去30日、1日足）
data = yf.download(symbol, period="30d", interval="1d")
data.dropna(inplace=True)  # 欠損値を削除

# 高値・安値のブレイク判定
data["20日高値"] = data["High"].rolling(window=20).max()
data["20日安値"] = data["Low"].rolling(window=20).min()

latest = data.iloc[-1]
today = latest.name.date()
close = latest["Close"]
high_20 = latest["20日高値"]
low_20 = latest["20日安値"]

# シグナル判定
signal = None
if close > high_20:
    signal = "📈 買いサイン"
elif close < low_20:
    signal = "📉 売りサイン"
else:
    signal = "⏳ ノーサイン（保留）"

# Slack通知本文作成
message = f"""
📊 タートルズ戦略通知
--------------------------
通貨ペア：{name}
日付：{today}
現在価格：{round(close, 3)}
20日高値：{round(high_20, 3)}
20日安値：{round(low_20, 3)}
シグナル：{signal}
"""

# 通知送信
send_slack_message(message)

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# Slack Webhook（←自分のに差し替えてね！）
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_message(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slackに通知を送りました")
    else:
        print(f"❌ 通知失敗: {response.status_code} - {response.text}")

# 通貨ペア：USD/JPY（Yahoo Financeは JPY=X）
symbol = "JPY=X"
name = "USD/JPY"

# データ取得
data = yf.download(symbol, period="30d", interval="1d")
data.dropna(inplace=True)

# 20日高値・安値を計算
data["20日高値"] = data["High"].rolling(window=20).max()
data["20日安値"] = data["Low"].rolling(window=20).min()

# 最新行だけ取得（20日目以降でないと値がNaN）
latest = data.dropna().iloc[-1]
today = latest.name.date()
close = latest["Close"]
high_20 = latest["20日高値"]
low_20 = latest["20日安値"]

# シグナル判定
if close > high_20:
    signal = "📈 買いサイン"
elif close < low_20:
    signal = "📉 売りサイン"
else:
    signal = "⏳ ノーサイン（保留）"

# Slack通知の本文
message = f"""
📊 タートルズ戦略通知
--------------------------
通貨ペア：{name}
日付：{today}
現在価格：{round(close, 3)}
20日高値：{round(high_20, 3)}
20日安値：{round(low_20, 3)}
シグナル：{signal}
"""

# 通知を送信！
send_slack_message(message)

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# Slack Webhook（自分のに変えてね）
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_message(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slackに通知を送りました")
    else:
        print(f"❌ 通知失敗: {response.status_code} - {response.text}")

# 通貨ペア設定
symbol = "JPY=X"
name = "USD/JPY"

# データ取得（30日分）
data = yf.download(symbol, period="30d", interval="1d")
data.dropna(inplace=True)

# 高値・安値の計算
data["20日高値"] = data["High"].rolling(window=20).max()
data["20日安値"] = data["Low"].rolling(window=20).min()

# 最新の行（20日分揃った最終行）
latest_row = data.dropna().iloc[-1]
today = latest_row.name.date()
close = latest_row["Close"]
high_20 = latest_row["20日高値"]
low_20 = latest_row["20日安値"]

# 数値に変換（←ここがポイント！）
close = float(close)
high_20 = float(high_20)
low_20 = float(low_20)

# シグナル判定
if close > high_20:
    signal = "📈 買いサイン"
elif close < low_20:
    signal = "📉 売りサイン"
else:
    signal = "⏳ ノーサイン（保留）"

# Slack通知メッセージ
message = f"""
📊 タートルズ戦略通知
--------------------------
通貨ペア：{name}
日付：{today}
現在価格：{round(close, 3)}
20日高値：{round(high_20, 3)}
20日安値：{round(low_20, 3)}
シグナル：{signal}
"""

# 通知送信
send_slack_message(message)

