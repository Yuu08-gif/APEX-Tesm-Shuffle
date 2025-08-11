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
client = discord.Client(intents=intents,status=discord.Status.online)

@client.event
async def on_ready():
    print(f'✅ Bot logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@bot.command(name="ping", description="pingを返します")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("pong")

# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
client.run(TOKEN)
