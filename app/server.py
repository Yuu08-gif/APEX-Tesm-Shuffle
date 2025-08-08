from threading import Thread
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is Online."}

@app.head("/")
async def head_root():
    return

def start():
    port = int(os.environ.get("PORT", 8080))  # 🔧 環境変数 PORT を使用
    uvicorn.run(app, host="0.0.0.0", port=port)

def server_thread():
    t = Thread(target=start)
    t.start()
