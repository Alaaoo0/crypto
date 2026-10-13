import time
import requests

# 廿毓丿丕丿丕鬲 丕賱鬲賱賷噩乇丕賲 丕賱禺丕氐 亘賰 (囟毓 丕賱賭 Token 丕賱禺丕氐 亘丕賱亘賵鬲 賵賲毓乇賮 丕賱卮丕鬲 賴賳丕)
TELEGRAM_BOT_TOKEN = "8807456899:AAHxdiwbesugwo91pELRwJS_M2H9-sslEW0"
TELEGRAM_CHAT_ID = "8743895023"

# 乇賵丕亘胤 亘賷賳丕賳爻 丕賱乇爻賲賷丞
BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"


def send_telegram_alert(message):
  """丿丕賱丞 賱廿乇爻丕賱 丕賱鬲賳亘賷賴丕鬲 丕賱賮賵乇賷丞 廿賱賶 亘賵鬲 鬲賱賷噩乇丕賲"""
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "HTML",
      "disable_web_page_preview": True,
  }
  try:
    response = requests.post(url, json=payload, timeout=10)
    return response.status_code == 200
  except Exception as e:
    print(f"禺胤兀 賮賷 廿乇爻丕賱 丕賱鬲賱賷噩乇丕賲: {e}")
    return False


def check_market_health():
  """賮丨氐 氐丨丞 丕賱爻賵賯 丕賱毓丕賲丞 毓亘乇 丕賱亘賷鬲賰賵賷賳 (BTCUSDT) 賰賲丐卮乇 乇卅賷爻賷"""
  try:
    res = requests.get(
        f"{BINANCE_KLINES_URL}?symbol=BTCUSDT&interval=1h&limit=5", timeout=10
    )
    candles = res.json()
    if isinstance(candles, list) and len(candles) >= 2:
      # 賲賯丕乇賳丞 爻毓乇 丕賱廿睾賱丕賯 丕賱丨丕賱賷 亘丌禺乇 爻丕毓丞 賱賲毓乇賮丞 丕鬲噩丕賴 丕賱亘賷鬲賰賵賷賳 丕賱毓丕賲
      close_current = float(candles[-1][4])
      close_prev = float(candles[-2][4])
      if close_current >= close_prev:
        return True  # 丕賱爻賵賯 賲爻鬲賯乇 兀賵 氐丕毓丿
  except Exception:
    pass
  return False  # 丕賮鬲乇丕囟 丕賱丨匕乇 廿匕丕 賮卮賱 丕賱丕鬲氐丕賱 兀賵 賰丕賳 賴丕亘胤丕賸


def analyze_coins():
  """賲丨乇賰 丕賱賮丨氐 丕賱卮丕賲賱 賱賱毓賲賱丕鬲 賵鬲胤亘賷賯 卮乇賵胤 丕賱賳禺亘丞"""
  print(
      "馃攳 [丕賱爻賷乇賮乇 丕賱爻丨丕亘賷] 噩丕乇賷 賮丨氐 丕賱爻賵賯 賵丕賱亘丨孬 毓賳 廿卮丕乇丕鬲 丕賱賳禺亘丞 丕賱丨賯賷賯賷丞..."
  )

  # 1. 丕賱鬲丨賯賯 兀賵賱丕賸 賲賳 氐丨丞 丕賱爻賵賯 丕賱毓丕賲丞
  is_market_healthy = check_market_health()
  if not is_market_healthy:
    print(
        "鈿狅笍 丕賱爻賵賯 丕賱毓丕賲 (丕賱亘賷鬲賰賵賷賳) 賴丕亘胤 兀賵 睾賷乇 賲爻鬲賯乇. 鬲賲 鬲禺胤賷 丕賱廿乇爻丕賱 丨賲丕賷丞賸"
        " 賱賱賲丨賮馗丞."
    )
    return

  try:
    response = requests.get(BINANCE_TICKER_URL, timeout=15)
    data = response.json()

    if not isinstance(data, list):
      return

    for t in data:
      symbol = t.get("symbol", "")

      # 鬲氐賮賷丞 丕賱毓賲賱丕鬲 (賮賯胤 夭賵噩 USDT 賵丕爻鬲亘毓丕丿 丕賱毓賲賱丕鬲 丕賱賲賰乇乇丞 兀賵 丕賱賲乇賮賵毓丞)
      if not symbol.endswith("USDT"):
        continue
      if any(
          x in symbol
          for x in ["UP", "DOWN", "BULL", "BEAR", "USDC", "FDUSD", "TUSD"]
      ):
        continue

      volume = float(t.get("quoteVolume", 0))
      change = float(t.get("priceChangePercent", 0))
      price = float(t.get("lastPrice", 0))

      # 卮乇賵胤 丕賱賮賱鬲乇丞 丕賱賲鬲賯丿賲丞 (鬲卮丕亘賴 卮乇賵胤 丕賱賳禺亘丞 賮賷 丕賱兀丿丕丞)
      # 丨噩賲 鬲丿丕賵賱 賯賵賷 + 氐毓賵丿 廿賷噩丕亘賷 囟賲賳 丕賱丨丿賵丿 丕賱丌賲賳丞 (賱賷爻 賲鬲囟禺賲丕賸 亘卮賰賱 賵賴賲賷)
      if volume > 5000000 and 1.5 <= change <= 10.0:

        # 丨爻丕亘 丕賱兀賴丿丕賮 賵賵賯賮 丕賱禺爻丕乇丞 亘賳丕亍賸 毓賱賶 丕爻鬲乇丕鬲賷噩賷鬲賳丕 丕賱匕賴亘賷丞
        entry_price = price
        target_1 = entry_price * 1.03  # 丕賱賴丿賮 丕賱兀賵賱 +3%
        target_2 = entry_price * 1.15  # 丕賱賴丿賮 丕賱孬丕賳賷 +15%
        stop_loss = entry_price * (1 - 0.018)  # 賵賯賮 丕賱禺爻丕乇丞 -1.8%

        # 乇爻丕賱丞 丕賱鬲賳亘賷賴 丕賱鬲賷 爻鬲氐賱賰 賮賵乇丕賸 毓賱賶 鬲賱賷噩乇丕賲
        alert_message = (
            f"馃拵 <b>廿卮丕乇丞 賳禺亘丞 爻丨丕亘賷丞 賲丐賰丿丞 (24/7)!</b>\n\n"
            f"馃敼 <b>丕賱毓賲賱丞:</b> <code>{symbol}</code>\n"
            f"馃挵 <b>爻毓乇 丕賱丿禺賵賱:</b> ${entry_price:.6f}\n\n"
            f"馃幆 <b>丕賱賴丿賮 丕賱兀賵賱 (+3%):</b> ${target_1:.6f}\n"
            f"馃殌 <b>丕賱賴丿賮 丕賱孬丕賳賷 (+15%):</b> ${target_2:.6f}\n"
            f"馃洃 <b>賵賯賮 丕賱禺爻丕乇丞 (-1.8%):</b> ${stop_loss:.6f}\n\n"
            f"馃敟 <i>鬲賲 賮丨氐 丕賱卮乇賵胤 賵鬲兀賰賷丿 氐丨丞 丕賱爻賵賯 亘賳噩丕丨.</i>"
        )

        # 廿乇爻丕賱 丕賱鬲賳亘賷賴 毓亘乇 亘賵鬲 鬲賱賷噩乇丕賲
        success = send_telegram_alert(alert_message)
        if success:
          print(f"鉁� 鬲賲 廿乇爻丕賱 鬲賳亘賷賴 丕賱賳禺亘丞 賱賱毓賲賱丞: {symbol}")

        # 丕賱丕賳鬲馗丕乇 賯賱賷賱丕賸 亘賷賳 丕賱毓賲賱丕鬲 賱鬲賮丕丿賷 丕賱丨馗乇 賲賳 亘賷賳丕賳爻
        time.sleep(1)

  except Exception as e:
    print(f"鉂� 禺胤兀 兀孬賳丕亍 賮丨氐 丕賱毓賲賱丕鬲: 爻賷乇賮乇 丕賱賮丨氐: {e}")


# 丨賱賯丞 丕賱鬲賰乇丕乇 丕賱賲爻鬲賲乇丞 賱賷毓賲賱 丕賱爻賷乇賮乇 毓賱賶 賲丿丕乇 丕賱爻丕毓丞 (24/7)
if __name__ == "__main__":
  print("馃殌 鬲賲 鬲卮睾賷賱 賳馗丕賲 丕賱鬲丿丕賵賱 丕賱爻丨丕亘賷 丕賱丌賱賷 24/7 亘賳噩丕丨!")
  while True:
    analyze_coins()
    # 賷賮丨氐 丕賱爻賵賯 亘丕賱賰丕賲賱 賰賱 3 丿賯丕卅賯 賱鬲噩賳亘 丕賱丨馗乇 (Rate Limit) 賵賱賱丨賮丕馗 毓賱賶 丿賯丞 丕賱兀丿丕亍
    time.sleep(180)
