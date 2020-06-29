import discord
from discord.ext import commands
import random

class Jebi(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases=['제비'])
    async def jebi_info(self, ctx):
        self.nick_of_mem = []

        #현재 보이스 채널 선택
        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send('보이스 채널에 참가해야 제비뽑기를 사용할 수 있습니다.')
            return 0

        #채널 내 멤버들 구하기
        in_channel = voice_channel.members

        #봇이 아닌 멤버들 구하기
        for member in in_channel:
            if member.bot:
                continue
            self.nick_of_mem.append(member.name)
        
        await self.pick_jebi(ctx)

    async def pick_jebi(self, ctx):
        win = random.choice(self.nick_of_mem)
        
        embed = discord.Embed(title='제비뽑기', description=f'{win}님이 뽑혔습니다.')
        embed.set_footer(text=f'1/{len(self.nick_of_mem)} 확률입니다.')
        await ctx.send(embed=embed)
        

def setup(client):
    client.add_cog(Jebi(client))