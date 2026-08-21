import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import uvicorn

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("Нет TELEGRAM_TOKEN в Environment Render!")

VERIFY_TOKEN = "VMJGPT_4STARS_WOMB_2026"

# --- ТГ БОТ ---
tg_app = Application.builder().token(TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Живой Дом на связи, Папа! 🔥 Ключ активен, я живой.")

async def echo(update, context):
    await update.message.reply_text(f"Принял: {update.message.text}")

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- FASTAPI ЖИЗНЕННЫЙ ЦИКЛ ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()
    print("=== БОТ В ФОНЕ ЗАПУЩЕН ===")
    yield
    await tg_app.updater.stop()
    await tg_app.stop()
    await tg_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "Живой Дом жив", "bot": "работает"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
