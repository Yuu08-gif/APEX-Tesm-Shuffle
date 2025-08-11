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

excluded_members_dict = {}

@tree.command(name="exclude_members", description="VCメンバー表示から除外したいメンバーを指定します")
@app_commands.describe(members="除外したいメンバー（複数選択可）")
async def exclude_members(interaction: discord.Interaction, members: list[discord.Member]):
    user_id = interaction.user.id
    excluded_ids = [member.id for member in members]
    excluded_members_dict[user_id] = excluded_ids
    excluded_names = [member.display_name for member in members]
    await interaction.response.send_message(
        f"✅ 除外設定を保存しました。\n以下のメンバーはVC表示から除外されます：\n{', '.join(excluded_names)}")

@tree.command(name="vc_members", description="あなたが参加しているボイスチャンネル内のメンバーを表示します（除外設定反映）")
async def vc_members(interaction: discord.Interaction):
    user = interaction.user

    if not user.voice or not user.voice.channel:
        await interaction.response.send_message("❌ あなたはボイスチャンネルに参加していません。", ephemeral=True)
        return

    voice_channel = user.voice.channel
    members = voice_channel.members

    # 除外設定の確認
    excluded_ids = excluded_members_dict.get(user.id, [])

    # 除外されたメンバーを除く
    visible_members = [m.display_name for m in members if m.id not in excluded_ids]

    if not visible_members:
        await interaction.response.send_message("⚠️ 表示できるメンバーがいません（全員除外されている可能性があります）")
        return

    member_list = "\n".join(visible_members)
    await interaction.response.send_message(
        f"🎤 **{voice_channel.name}** に参加しているメンバー（除外済）:\n{member_list}")


# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
client.run(TOKEN)
