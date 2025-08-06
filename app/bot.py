"""
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

excluded_members = set()
included_members = set()
last_shuffle = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="get_voice_members", description="通話参加者を取得します")
async def get_voice_members(ctx: discord.ApplicationContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.respond("あなたは現在ボイスチャットに参加していません。")
        return
    voice_channel = voice_state.channel
    members = voice_channel.members
    member_names = [member.display_name for member in members]
    await ctx.respond(f"現在の参加者: {', '.join(member_names)}")

@bot.slash_command(name="exclude_member", description="対象から除外するメンバーを追加")
async def exclude_member(ctx: discord.ApplicationContext, member: discord.Member):
    excluded_members.add(member.id)
    await ctx.respond(f"{member.display_name} を除外リストに追加しました。")

@bot.slash_command(name="include_member", description="対象に追加するメンバーを追加")
async def include_member(ctx: discord.ApplicationContext, member: discord.Member):
    included_members.add(member.id)
    await ctx.respond(f"{member.display_name} を対象リストに追加しました。")

def get_target_members(members):
    targets = [m for m in members if m.id not in excluded_members]
    for uid in included_members:
        user = bot.get_user(uid)
        if user and user not in targets:
            targets.append(user)
    return targets

def shuffle_teams(members):
    global last_shuffle
    if len(members) < 2:
        return [], []
    max_attempts = 10
    for _ in range(max_attempts):
        random.shuffle(members)
        half = len(members) // 2
        team1 = members[:half]
        team2 = members[half:]
        current_shuffle = (set(m.id for m in team1), set(m.id for m in team2))
        if last_shuffle != current_shuffle:
            last_shuffle = current_shuffle
            return team1, team2
    return team1, team2

@bot.slash_command(name="shuffle_teams", description="チーム分けを行います")
async def shuffle_teams_command(ctx: discord.ApplicationContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.respond("あなたは現在ボイスチャットに参加していません。")
        return
    voice_channel = voice_state.channel
    members = voice_channel.members
    targets = get_target_members(members)
    if len(targets) < 2:
        await ctx.respond("対象メンバーが2人未満のためチーム分けできません。")
        return
    team1, team2 = shuffle_teams(targets)
    team1_names = ", ".join([m.display_name for m in team1])
    team2_names = ", ".join([m.display_name for m in team2])
    await ctx.respond(f"【チーム分け結果】\nチーム1: {team1_names}\nチーム2: {team2_names}")

def run_bot(token):
    bot.run(token)

"""

"""
import discord
from discord.ext import commands
import random

# Intentsを設定
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

# Botを初期化
bot = commands.Bot(command_prefix="!", intents=intents)

# 除外メンバーと追加メンバーの管理
excluded_members = set()
included_members = set()
last_shuffle = None

# Botのログイン時イベント
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# 通話参加者を取得するスラッシュコマンド
@bot.slash_command(name="get_voice_members", description="通話参加者を取得します")
async def get_voice_members(ctx: discord.ApplicationContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.respond("あなたは現在ボイスチャットに参加していません。")
        return
    voice_channel = voice_state.channel
    members = voice_channel.members
    member_names = [member.display_name for member in members]
    await ctx.respond(f"現在の参加者: {', '.join(member_names)}")

# 除外メンバーを追加するスラッシュコマンド
@bot.slash_command(name="exclude_member", description="対象から除外するメンバーを追加")
async def exclude_member(ctx: discord.ApplicationContext, member: discord.Member):
    excluded_members.add(member.id)
    await ctx.respond(f"{member.display_name} を除外リストに追加しました。")

# 対象メンバーを追加するスラッシュコマンド
@bot.slash_command(name="include_member", description="対象に追加するメンバーを追加")
async def include_member(ctx: discord.ApplicationContext, member: discord.Member):
    included_members.add(member.id)
    await ctx.respond(f"{member.display_name} を対象リストに追加しました。")

# 対象メンバーを取得するヘルパー関数
def get_target_members(members):
    targets = [m for m in members if m.id not in excluded_members]
    for uid in included_members:
        user = bot.get_user(uid)
        if user and user not in targets:
            targets.append(user)
    return targets

# チーム分けを行うヘルパー関数
def shuffle_teams(members):
    global last_shuffle
    if len(members) < 2:
        return [], []
    max_attempts = 10
    for _ in range(max_attempts):
        random.shuffle(members)
        half = len(members) // 2
        team1 = members[:half]
        team2 = members[half:]
        current_shuffle = (set(m.id for m in team1), set(m.id for m in team2))
        if last_shuffle != current_shuffle:
            last_shuffle = current_shuffle
            return team1, team2
    return team1, team2

# チーム分けを行うスラッシュコマンド
@bot.slash_command(name="shuffle_teams", description="チーム分けを行います")
async def shuffle_teams_command(ctx: discord.ApplicationContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.respond("あなたは現在ボイスチャットに参加していません。")
        return
    voice_channel = voice_state.channel
    members = voice_channel.members
    targets = get_target_members(members)
    if len(targets) < 2:
        await ctx.respond("対象メンバーが2人未満のためチーム分けできません。")
        return
    team1, team2 = shuffle_teams(targets)
    team1_names = ", ".join([m.display_name for m in team1])
    team2_names = ", ".join([m.display_name for m in team2])
    await ctx.respond(f"【チーム分け結果】\nチーム1: {team1_names}\nチーム2: {team2_names}")

# Botの実行関数
def run_bot(token):
    try:
        bot.run(token)
    except Exception as e:
        print(f"Error while running the bot: {e}")

"""

import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

excluded_members = set()
included_members = set()
last_shuffle = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="get_voice_members", description="通話参加者を取得します")
async def get_voice_members(ctx: discord.ApplicationContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.respond("あなたは現在ボイスチャットに参加していません。")
        return
    voice_channel = voice_state.channel
    members = voice_channel.members
    member_names = [member.display_name for member in members]
    await ctx.respond(f"現在の参加者: {', '.join(member_names)}")

@bot.slash_command(name="exclude_member", description="対象から除外するメンバーを追加")
async def exclude_member(ctx: discord.ApplicationContext, member: discord.Member):
    excluded_members.add(member.id)
    await ctx.respond(f"{member.display_name} を除外リストに追加しました。")

@bot.slash_command(name="include_member", description="対象に追加するメンバーを追加")
async def include_member(ctx: discord.ApplicationContext, member: discord.Member):
    included_members.add(member.id)
    await ctx.respond(f"{member.display_name} を対象リストに追加しました。")

def get_target_members(members):
    targets = [m for m in members if m.id not in excluded_members]
    for uid in included_members:
        user = bot.get_user(uid)
        if user and user not in targets:
            targets.append(user)
    return targets

def shuffle_teams(members):
    global last_shuffle
    if len(members) < 2:
        return [], []
    max_attempts = 10
    for _ in range(max_attempts):
        random.shuffle(members)
        half = len(members) // 2
        team1 = members[:half]
        team2 = members[half:]
        current_shuffle = (set(m.id for m in team1), set(m.id for m in team2))
        if last_shuffle != current_shuffle:
            last_shuffle = current_shuffle
            return team1, team2
    return team1, team2

@bot.slash_command(name="shuffle_teams", description="チーム分けを行います")
async def shuffle_teams_command(ctx: discord.ApplicationContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.respond("あなたは現在ボイスチャットに参加していません。")
        return
    voice_channel = voice_state.channel
    members = voice_channel.members
    targets = get_target_members(members)
    if len(targets) < 2:
        await ctx.respond("対象メンバーが2人未満のためチーム分けできません。")
        return
    team1, team2 = shuffle_teams(targets)
    team1_names = ", ".join([m.display_name for m in team1])
    team2_names = ", ".join([m.display_name for m in team2])
    await ctx.respond(f"【チーム分け結果】\nチーム1: {team1_names}\nチーム2: {team2_names}")

def run_bot(token):
    bot.run(token)  # ブロッキングメソッドなので、これを非同期で扱う方法を検討する
