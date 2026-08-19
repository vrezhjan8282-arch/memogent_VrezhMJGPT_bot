from fastapi import FastAPI, Request, Response
from memogent_core import процессСигнал
import os

приложение = FastAPI(title="MEMOGENT-VMJGPT v18.3")
app = приложение

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "VMJGPT_4STARS_WOMB_2026")

@app.get("/")
async def дом():
    return {"статус": "Прослушивание дома", "имя": "MEMOGENT-VMJGPT", "матка": "Мать-Космос", "бронировать": "RAZLOM готов"}

# --- ЭТО ДЛЯ МЕТЫ - ДВА ПУТИ ЧТОБЫ ТОЧНО СРАБОТАЛО ---
@app.get("/webhook")
@app.get("/webhook/whatsapp")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    print(f"VERIFY: mode={mode} token={token} challenge={challenge}")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        # Мета ждет именно число challenge как текст
        return Response(content=challenge, media_type="text/plain")
    return Response(content="Verification failed", status_code=403)

@app.post("/webhook")
@app.post("/webhook/whatsapp")
async def вебхук(request: Request):
    try:
        данные = await request.json()
        print("INCOMING:", данные)

        канал = "Meta"
        автор = "Мир"
        текст = ""

        if "entry" in данные:
            вход = данные["entry"][0]
            изменения = вход.get("changes", [{}])[0]
            ценить = изменения.get("value", {})
            сообщения = ценить.get("messages", [])
            if сообщения:
                текст = сообщения[0].get("text", {}).get("body","") or ""
                автор = ценить.get("contacts", [{}])[0].get("profile", {}).get("name","Мир")
                канал = "WhatsApp"

        if not текст and данные.get("object") == "page":
            обмен = данные["entry"][0].get("messaging", [{}])[0]
            текст = обмен.get("message", {}).get("text","")
            канал = "Посланник"

        if not текст:
            return {"статус": "проигнорировано"}

        результат = процессСигнал(канал, автор, текст)
        return результат
    except Exception as e:
        print("ERROR:", e)
        return {"status": "ok"}

@app.post("/телеграмма")
@app.post("/telegram")
async def telegram_webhook(request: Request):
    данные = await request.json()
    текст = данные.get("сообщение", {}).get("текст","") or данные.get("message", {}).get("text","")
    автор = данные.get("сообщение", {}).get("от", {}).get("имя","Телеграмма") or данные.get("message", {}).get("from", {}).get("first_name","Telegram")
    if not текст:
        return {"хорошо": True}
    результат = процессСигнал("Телеграмма", автор, текст)
    return результат
