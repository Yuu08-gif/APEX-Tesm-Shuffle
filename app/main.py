"""
import os
import discord
import dotenv
from server import server_thread

dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
print(f"TOKEN LOADED? {'Yes' if TOKEN else 'No'}")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
client.run(TOKEN)
"""


"""
import os
import dotenv
import discord
from server import server_thread
from bot import run_bot  # bot.pyからrun_bot関数をインポート

dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
print(f"TOKEN LOADED? {'Yes' if TOKEN else 'No'}")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
run_bot(TOKEN)
"""

"""
import os
import discord
import dotenv
import asyncio
from server import server_thread
from bot import run_bot

dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
print(f"TOKEN LOADED? {'Yes' if TOKEN else 'No'}")

# 非同期処理を使うためにclient.runではなく、run_botで実行
async def start_bot():
    # Webサーバーを非同期で起動
    asyncio.create_task(server_thread())  
    # Bot起動
    run_bot(TOKEN)

# メインスレッドで実行
asyncio.run(start_bot())
"""

import os
import dotenv
import asyncio
from server import server_thread
from bot import run_bot

# .envファイルを読み込む
dotenv.load_dotenv()

# 環境変数からトークンを取得
TOKEN = os.environ.get("TOKEN")
print(f"TOKEN LOADED? {'Yes' if TOKEN else 'No'}")

# 非同期処理を使うために、client.runではなくrun_botで実行
async def start_bot():
    # Webサーバーを非同期で起動
    asyncio.create_task(server_thread())  
    # Bot起動
    await run_bot(TOKEN)  # run_botをawaitで呼び出し

# メインスレッドで非同期タスクを実行
if __name__ == "__main__":
    asyncio.run(start_bot())  # 非同期タスクをrun
