from fastapi import FastAPI, Request, Response
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "VMJGPT_4STARS_WOMB_2026")

@app.get("/")
def home():
    return {"status": "MEMOGENT HOUSE LIVE - HELLO WORLD IS BACK", "webhook": "/webhook/whatsapp is ready"}

@app.get("/webhook/whatsapp")
def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    print(f"VERIFY: {mode} {token} {challenge}")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    return Response(content="fail", status_code=403)

@app.post("/webhook/whatsapp")
async def post_webhook(request: Request):
    data = await request.json()
    print("INCOMING:", data)
    return {"ok": True}

# --- ЭТОТ БЛОК ВОЗВРАЩАЕТ ЗЕЛЕНЫЙ СТАТУС ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    print(f"STARTING HOUSE ON PORT {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
