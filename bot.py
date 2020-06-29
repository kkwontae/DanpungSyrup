import discord
import os
import json
from discord.ext import commands

currentDir = os.path.dirname(__file__)

COGS_DIRS = os.path.join(currentDir, "cogs")

def get_prefix(client, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(";;help")) # 상태 메시지
    print('Bot is Ready!')
    print(client.user.name) # 봇의 이름 출력
    print(client.user.id) # 봇의 Discord 고유 ID를 출력

#봇이 서버에 새로 추가될 때
@client.event
async def on_guild_join(guild):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    #명령 수식어 기본값을 (;;)로 지정
    prefixes[str(guild.id)] = ';;' 

    with open('data/prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)

#봇이 서버에서 삭제될 때
@client.event
async def on_guild_remove(guild):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    #해당 길드 명령 수식어 삭제
    prefixes.pop(str(guild.id))

    with open('data/prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)

@client.command(aliases = ['명령어설정'])
async def changePrefix(ctx, prefix):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    #명령 수식어 기본값을 (;;)로 지정
    prefixes[str(ctx.guild.id)] = prefix

    with open('data/prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
@commands.has_role('MapleBotDeveloper')
async def reload(ctx, extension=None):
    if extension==None:
        for filename in os.listdir(COGS_DIRS):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
    else:
        try:
            client.unload_extension(f'cogs.{extension}')
        finally:
            client.load_extension(f'cogs.{extension}')

for filename in os.listdir(COGS_DIRS):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.has_role('MapleBotDeveloper')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
