import os
import requests

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

ORIGINS = ["OPO", "LCG", "SCQ", "VGO"]
DESTINATIONS = ["SAO", "DXB"]


def search_flights():
  url = "https://skyscanner-api.p.rapidapi.com/v3/flights/live/search/create"
  headers = {
      "content-type": "application/json",
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com",
  }

  for origin in ORIGINS:
    for destination in DESTINATIONS:
      payload = {
          "query": {
              "market": "ES",
              "locale": "es-ES",
              "currency": "EUR",
              "queryLegs": [{
                  "originPlaceId": {"iata": origin},
                  "destinationPlaceId": {"iata": destination},
                  "date": {"year": 2026, "month": 11, "day": 15},
              }],
              "adults": 1,
          }
      }
      try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
          process_results(response.json(), origin, destination)
      except requests.exceptions.RequestException:
        pass


def process_results(data, origin, destination):
  message = (
      f"✈️ **Alerta de Voo Encontrado!**\n\n"
      f"🟢 **De:** {origin}\n"
      f"🎯 **Para:** {destination}\n"
      f"💶 **Status:** Oportunidade rastreada com sucesso via Skyscanner.\n\n"
      f"🔗 [Clique aqui para acessar o rastreio no"
      f" Skyscanner](https://www.skyscanner.es)"
  )
  send_telegram(message)


def send_telegram(text):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": text,
      "parse_mode": "Markdown",
  }
  try:
    requests.post(url, json=payload, timeout=10)
  except requests.exceptions.RequestException:
    pass


if __name__ == "__main__":
  search_flights()
