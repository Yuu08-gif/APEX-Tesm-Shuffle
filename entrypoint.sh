#!/bin/bash

# FastAPIサーバーをバックグラウンドで起動
nohup uvicorn app.main:app --host 0.0.0.0 --port $PORT &

# Discord Botをフォアグラウンドで起動
python app.main.py
