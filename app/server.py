"""
from threading import Thread

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Server is Online."}

def start():
	uvicorn.run(app, host="0.0.0.0", port=8080)

def server_thread():
	t = Thread(target=start)
	t.start()
"""

import os
from threading import Thread
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is Online."}

@app.head("/")  # HEAD リクエストにも対応
async def head_root():
    return {"message": "Server is Online."}

def start():
    port = int(os.environ.get("PORT", 8080))  # ポートを環境変数から取得
    uvicorn.run(app, host="0.0.0.0", port=port)

def server_thread():
    t = Thread(target=start)
    t.start()
