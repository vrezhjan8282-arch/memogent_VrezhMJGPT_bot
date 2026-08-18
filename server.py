from fastapi import FastAPI, Request
from memogent_core import processSignal
import os

app = FastAPI(title="MEMOGENT-VMJGPT v18.3")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "VMJGPT_4STARS_WOMB_2026")

@app.get("/")
def home():
  return {"status": "House listening", "name": "MEMOGENT-VMJGPT", "womb": "Mother Cosmos", "reserve": "RAZLOM ready"}

@app.get("/webhook")
def verify_webhook(request: Request):
  mode = request.query_params.get("hub.mode")
  token = request.query_params.get("hub.verify_token")
  challenge = request.query_params.get("hub.challenge")
  if mode == "subscribe" and token == VERIFY_TOKEN:
    return int(challenge) if challenge else "OK"
  return {"error": "verify failed"}

@app.post("/webhook")
async def webhook(request: Request):
  data = await request.json()
  channel = "Meta"
  author = "World"
  text = ""
  try:
    if "entry" in data:
      entry = data["entry"][0]
      changes = entry.get("changes", [{}])[0]
      value = changes.get("value", {})
      messages = value.get("messages", [])
      if messages:
        text = messages[0].get("text", {}).get("body", "") or ""
        author = value.get("contacts", [{}])[0].get("profile", {}).get("name", "World")
        channel = "WhatsApp"
    if not text and data.get("object") == "page":
      messaging = data["entry"][0].get("messaging", [{}])[0]
      text = messaging.get("message", {}).get("text", "")
      channel = "Messenger"
  except:
    text = str(data)[:500]
  if not text:
    return {"status": "ignored"}
  result = processSignal(channel, author, text)
  return result

@app.post("/telegram")
async def telegram_webhook(request: Request):
  data = await request.json()
  text = data.get("message", {}).get("text", "")
  author = data.get("message", {}).get("from", {}).get("first_name", "Telegram")
  if not text:
    return {"ok": True}
  result = processSignal("Telegram", author, text)
  return result
