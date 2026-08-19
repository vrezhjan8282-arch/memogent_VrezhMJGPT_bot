from fastapi import FastAPI, Request, Response
import os
app = FastAPI()
VERIFY_TOKEN = "VMJGPT_4STARS_WOMB_2026"
@app.get("/")
def home():
    return {"ok": True}
@app.get("/webhook/whatsapp")
def verify(request: Request):
    m = request.query_params.get("hub.mode")
    t = request.query_params.get("hub.verify_token")
    c = request.query_params.get("hub.challenge")
    if m == "subscribe" and t == VERIFY_TOKEN:
        return Response(content=c, media_type="text/plain")
    return Response(content="fail", status_code=403)
@app.post("/webhook/whatsapp")
async def incoming(request: Request):
    print(await request.json())
    return {"ok": True}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
