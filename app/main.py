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



@tree.command(name="in?",description="イる？")
async def addition(interaction: discord.Interaction):
    members = [i.name for i in message.author.voice.channel.members]
    team = []
    for i in range(party_num):
        team.extend(members[i:len(members):party_num])
        #print ('\n'.join(team))
    
    await interaction.response.send_message('\n'.join(team))


# Webサーバー起動（別スレッド）
server_thread()

# Bot起動
client.run(TOKEN)
