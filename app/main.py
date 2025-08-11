import os
import discord
import dotenv
from server import server_thread
from discord import app_commands
import re
import random

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

@tree.command(name="test", description="シます")
async def addition(interaction: discord.Interaction, formula: str):
    # 0〜99の乱数を生成し、5未満なら5%
    if random.randint(0, 99) < 5:
        await interaction.response.send_message("膣内射精感謝")
    else:
        await interaction.response.send_message("シました")


excluded_members_dict = {}
@tree.command(name="除外切り替え", description="VCメンバー表示からの除外状態を切り替えます")
@app_commands.describe(member="除外状態を切り替えたいメンバー")
async def toggle_exclude_member(interaction: discord.Interaction, member: discord.Member):
    user_id = interaction.user.id
    if user_id not in excluded_members_dict:
        excluded_members_dict[user_id] = []

    if member.id in excluded_members_dict[user_id]:
        # 既に除外されている → 除外解除（適応）
        excluded_members_dict[user_id].remove(member.id)
        await interaction.response.send_message(f"✅ {member.display_name} の除外を解除しました。")
    else:
        # 除外されていない → 除外に追加
        excluded_members_dict[user_id].append(member.id)
        await interaction.response.send_message(f"🚫 {member.display_name} を除外リストに追加しました。")


team_settings_dict = {}
@tree.command(name="チーム数の設定", description="チーム数を設定します（デフォルト2）")
@app_commands.describe(team_count="チーム数（1以上の整数）")
async def set_team_count(interaction: discord.Interaction, team_count: int):
    if team_count < 1:
        await interaction.response.send_message("❌ チーム数は1以上で指定してください。", ephemeral=True)
        return

    user_id = interaction.user.id
    team_settings_dict[user_id] = team_count
    await interaction.response.send_message(f"✅ チーム数を {team_count} に設定しました。")


@tree.command(name="メンバー表示", description="あなたが参加しているボイスチャンネル内のメンバーを表示します（除外設定とBot除外）")
async def vc_members(interaction: discord.Interaction):
    user = interaction.user

    if not user.voice or not user.voice.channel:
        await interaction.response.send_message("❌ あなたはボイスチャンネルに参加していません。", ephemeral=True)
        return

    voice_channel = user.voice.channel
    members = voice_channel.members

    # 除外設定の確認
    excluded_ids = excluded_members_dict.get(user.id, [])

    # 除外リストおよびBotを除外
    visible_members = [
        m.display_name
        for m in members
        if m.id not in excluded_ids and not m.bot
    ]

    if not visible_members:
        await interaction.response.send_message("⚠️ 表示できるメンバーがいません（全員除外・Bot・自分自身のみの可能性があります）")
        return

    member_list = "\n".join(visible_members)
    await interaction.response.send_message(f"🎤 **{voice_channel.name}** に参加しているメンバー（除外済＋Bot除外）:\n{member_list}")


@tree.command(name="チーム分け", description="設定されたチーム数でVCメンバーを分けます")
async def team_divide(interaction: discord.Interaction):
    user = interaction.user
    team_count = team_settings_dict.get(user.id, 2)  # デフォルトは2

    if not user.voice or not user.voice.channel:
        await interaction.response.send_message("❌ あなたはボイスチャンネルに参加していません。", ephemeral=True)
        return

    voice_channel = user.voice.channel
    members = voice_channel.members

    excluded_ids = excluded_members_dict.get(user.id, [])

    valid_members = [m for m in members if m.id not in excluded_ids and not m.bot]

    if not valid_members:
        await interaction.response.send_message("⚠️ 除外済みまたはBotを除いたメンバーがいません。", ephemeral=True)
        return

    import random
    random.shuffle(valid_members)

    teams = [[] for _ in range(team_count)]

    for i, member in enumerate(valid_members):
        teams[i % team_count].append(member.display_name)

    msg_lines = [f"🎯 **{voice_channel.name}** のメンバーを {team_count} チームに分けました："]
    for idx, team_members in enumerate(teams, start=1):
        if team_members:
            msg_lines.append(f"**チーム {idx}**:\n- " + "\n- ".join(team_members))
        else:
            msg_lines.append(f"**チーム {idx}**: メンバーなし")

    await interaction.response.send_message("\n\n".join(msg_lines))
    

# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
client.run(TOKEN)
