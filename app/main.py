import os
import discord
import dotenv
from server import server_thread
from discord import app_commands
import re

dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
print(f"TOKEN LOADED? {'Yes' if TOKEN else 'No'}")

intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'✅ Bot logged in as {client.user}')
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tree.command(name="test",description="シます")
async def addition(interaction: discord.Interaction,formula:str):
    await interaction.response.send_message(f"シました")

@tree.command(name="vc_members", description="あなたが参加しているボイスチャンネル内のメンバーを表示します")
async def vc_members(interaction: discord.Interaction):
    user = interaction.user

    # ユーザーがVCに入っていない場合
    if not user.voice or not user.voice.channel:
        await interaction.response.send_message("❌ あなたはボイスチャンネルに参加していません。", ephemeral=True)
        return

    voice_channel = user.voice.channel
    members = voice_channel.members  # VC内のメンバー一覧
    member_names = [member.display_name for member in members]

    member_list = "\n".join(member_names)
    await interaction.response.send_message(f"🎤 **{voice_channel.name}** に参加しているメンバー:\n{member_list}")




# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
client.run(TOKEN)
