import discord
from discord.ext import commands
import random

class Dice(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases=['주사위'])
    async def get_info(self, ctx):

        self.num_of_mem = 0
        self.nick_of_mem = []

        #현재 보이스 채널 선택
        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send('보이스 채널에 참가해야 주사위를 사용할 수 있습니다.')
            return 0

        #채널 내 멤버들 구하기
        in_channel = voice_channel.members

        #봇이 아닌 멤버들 구하기
        for member in in_channel:
            if member.bot:
                continue
            self.num_of_mem += 1
            self.nick_of_mem.append(member.name)
        
        await self.roll_dice(ctx)

    async def roll_dice(self, ctx):
        max_num = 0
        max_name = ' '
        dice_num = 6
        while dice_num < self.num_of_mem:
            dice_num += 2

        #인원수 만큼의 주사위
        num_list = [i for i in range(1, dice_num+1)]
        random.shuffle(num_list)
        
        embed = discord.Embed(title='주사위', description=f'{dice_num}면체 주사위를 굴립니다.')
        for i in range(self.num_of_mem):
            embed.add_field(name =f'{self.nick_of_mem[i]}', value = f'{num_list[i]}',inline=True)
            if num_list[i] > max_num:
                max_num = num_list[i]
                max_name = self.nick_of_mem[i]

        embed.set_footer(text=f'{max_name}님의 주사위가 가장 높습니다.')

        await ctx.send(embed=embed)

        self.nick_of_mem = []
        self.num_of_mem = 0
        

def setup(client):
    client.add_cog(Dice(client))