import discord
from discord.ext import commands
import requests
import json
from bs4 import BeautifulSoup
import random

class simulateGoldapple(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))


    @commands.Cog.listener()
    async def on_ready(self):
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases=['골드애플업데이트'])
    async def updateGoldapple(self):
        getGoldAppleLists()
        
    @commands.command(aliases=['골드애플'])
    async def simulate_Goldapple(self, message, amount=None):
        if amount == None:
            amount = 1
        try:
            amount = int(amount)
        except:
            await message.channel.send("```Error!\n올바른 명령어를 사용해주세요\n;;골드애플 [1~50]```")
            return
            
        if amount > 50 or amount < 0:
            await message.channel.send('부하를 방지하여 동시에 1 ~ 50개 까지 사용 가능합니다.')
        else:            
            json_obj = open('data/goldapple.json').read()
            py_obj = json.loads(json_obj)
            
            result = py_obj
            constsList = [0]
            
            for i in range(1,len(py_obj)+1):
                constsList.append(py_obj[str(i)]['consts'])
            for i in range(amount):
                r = random.randrange(1,result[str(len(result))]['consts']+1)
                constsList.append(r)
                constsList.sort()
                number = constsList.index(r) #뽑은 아이템의 인덱스
                result[str(number)]['count'] += 1
                constsList.remove(r)

            string = ""
            string += "```d\n"
            for i in range(1, len(result)):
                if result[str(i)]['count'] > 0:
                    string += "{} {} {}개\n".format(result[str(i)]['chances'], result[str(i)]['itemname'], result[str(i)]['count'])
            string += "```\n"

            #명령어설명
            string += "`명령어 : ;;골드애플 [1~50]`"

            embed = discord.Embed(
                title = '골드애플 x {} 회 결과'.format(amount),
                colour = discord.Colour.blue(),
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/722768492863946753.png')
            embed.add_field(name="총 가격 {:,.0f} 캐시(대량구매 할인x)".format(int(amount)*550), value=string)
            await message.channel.send(embed=embed)

def getGoldAppleLists():
    url = 'https://maplestory.nexon.com/Guide/CashShop/Probability/GoldApple'
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    table = bs_obj.find("table", {"class" : "my_page_tb2"})
    trs = table.findAll("tr")
    
    GoldAppleLists = {}
    
    for item in trs:
        if trs.index(item) == 0:
            continue
        elif trs.index(item) == 1:            
            _itemname = item.findAll("td")[1].text
            _chances = item.findAll("td")[2].text
            _consts = int(("").join(item.findAll("td")[2].text.split("%")[0].split(".")))
        else:  
            _itemname = item.findAll("td")[0].text
            _chances = item.findAll("td")[1].text
            _consts = GoldAppleLists[str(trs.index(item)-1)]['consts'] + int(("").join(item.findAll("td")[1].text.split("%")[0].split(".")))

        GoldAppleLists[str(trs.index(item))] = {"itemname" : _itemname, "chances" : _chances, "consts" : _consts, "count" : 0}

    json_obj = json.dumps(GoldAppleLists, indent=4)

    file = open("data/goldapple.json",'w')
    file.write(json_obj)
    file.close()

    return GoldAppleLists

def setup(client):
    client.add_cog(simulateGoldapple(client))

