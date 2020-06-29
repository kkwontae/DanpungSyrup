import discord
from discord.ext import commands
import requests
import json
from bs4 import BeautifulSoup
import random


class simulateMasterPiece(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))


    # Events #Example-1
    @commands.Cog.listener()
    async def on_ready(self):
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases = ['피스업데이트'])
    @commands.has_role('MapleBotDeveloper')
    async def updateMasterPiece(self, message):
        getMasterPieceLists()
        await message.channel.send('마스터피스 목록을 수동으로 업데이트하였습니다!')

    @commands.command(aliases = ['피스'])
    async def simulate_MasterPiece(self, message, types='None', rb='None'):
        rbConstsDic = {'스스' : 'consts_r', '레스' : 'consts_b'}
        try:
            if needUpdate() == True:
                getMasterPieceLists()
            else:
                json_obj = open('data/piece.json').read()
                py_obj = json.loads(json_obj)
                
                cp_py_obj = py_obj
                constsList = [0]
                if str(rb) == '목록':
                    string = "```d\n"
                    for i in range(1,len(cp_py_obj[str(types)])+1):
                        string += '[{}] {}\n'.format(i, cp_py_obj[str(types)][str(i)]['itemname'])
                    string += "```"
                    embed = discord.Embed(
                        title = '획득 가능한 마스터피스({}) 목록'.format(str(types)),
                        colour = 0xff88bb,
                    )
                    embed.add_field(name="──────────────────", value=string)

                    await message.channel.send(embed=embed)
                else:
                    masterLabel = cp_py_obj[str(types)][str(len(cp_py_obj[str(types)])-1)]['itemname']
                    hairCoupon = cp_py_obj[str(types)][str(len(cp_py_obj[str(types)]))]['itemname']
                    
                    
                    for i in range(1,len(cp_py_obj[str(types)])+1):
                        constsList.append(cp_py_obj[str(types)][str(i)][rbConstsDic[str(rb)]])

                    r = random.randrange(1,constsList[len(constsList)-1])
                    constsList.append(r)
                    constsList.sort()
                    number = constsList.index(r) #뽑은 아이템의 인덱스
                    constsList.remove(r)

                    resultItemname = cp_py_obj[str(types)][str(number)]['itemname']
                    tt = ""
                    if str(rb) == '스스':
                        tt = '스라벨 + 스라벨'
                        if resultItemname == masterLabel:
                            rr = '⭐마스터라벨⭐'
                        elif resultItemname == hairCoupon:
                            rr = '⭐헤어쿠폰⭐'
                        else:
                            rr = '레드라벨'
                    elif str(rb) == '레스':
                        tt = '레드라벨 + 스라벨'
                        if resultItemname == masterLabel:
                            rr = '⭐마스터라벨⭐'
                        elif resultItemname == hairCoupon:
                            rr = '⭐헤어쿠폰⭐'
                        else:
                            rr = '블랙라벨'
                    else:
                        tt= 'unvalid'
                        rr= 'unvalid'

                    string = '```' + resultItemname + '```'

                    embed = discord.Embed(
                        title = '{} 마스터피스({}) 결과'.format(str(types), tt),
                        colour = 0xff88bb,
                    )
                    embed.add_field(name='{}:'.format(rr), value=string)
                    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/719201194702012436.png')
                    await message.channel.send(embed=embed)
        except KeyError:
            embed = discord.Embed(
                description = "**Error!\n\n**올바른 명령어를 사용해주세요\n\n`;;피스 [부위] 목록`\n`;;피스 [부위] [유형]`\n\n부위 : (모자, 옷, 망토/장갑, 신발, 무기)\n유형 : (스스, 레스)",
                colour = discord.Colour.red()
            )
            await message.channel.send(embed=embed)

def setup(client):
    client.add_cog(simulateMasterPiece(client))

def getMasterPieceLists():
    url_r = 'https://maplestory.nexon.com/Guide/CashShop/Probability/MasterpieceRed'
    url_b = 'https://maplestory.nexon.com/Guide/CashShop/Probability/MasterpieceBlack'

    result_r = requests.get(url_r)
    result_b = requests.get(url_b)

    bs_obj_r = BeautifulSoup(result_r.content, "html.parser")
    bs_obj_b = BeautifulSoup(result_b.content, "html.parser")

    _date = getMasterPieceUpdateDate()

    hat = {}
    clothes = {}
    cloak = {}
    shoes = {}
    weapon = {}

    types = {0:"모자", 1:"옷", 2:"망토/장갑", 3:"신발", 4:"무기"}
    dic_types = {0:hat, 1:clothes, 2:cloak, 3:shoes, 4:weapon}
    


    for i in range(5):
        table_r = bs_obj_r.findAll("table", {"class" : "my_page_tb2"})[i] #0:모자, 1:옷, 2:망토/장갑, 3:신발, 4:무기
        trs_r = table_r.findAll("tr")
        table_b = bs_obj_b.findAll("table", {"class" : "my_page_tb2"})[i] #0:모자, 1:옷, 2:망토/장갑, 3:신발, 4:무기
        trs_b = table_b.findAll("tr")
        
        isFirst = True
        for item in trs_r:
            if trs_r.index(item) == 0:
                continue
            if item.findAll("td")[0].has_attr('rowspan') == True:
                _itemname = item.findAll("td")[1].text

                _chances_r = item.findAll("td")[2].text
                _chances_b = trs_b[trs_r.index(item)].findAll("td")[2].text
                if isFirst == True:
                    _consts_r = int(("").join(_chances_r.split("%")[0].split(".")))
                    _consts_b = int(("").join(_chances_b.split("%")[0].split(".")))
                    isFirst = False
                else:
                    _consts_r = dic_types[i][str(trs_r.index(item)-1)]['consts_r'] + int(("").join(_chances_r.split("%")[0].split(".")))
                    _consts_b = dic_types[i][str(trs_r.index(item)-1)]['consts_b'] + int(("").join(_chances_b.split("%")[0].split(".")))
            else:  
                _itemname = item.findAll("td")[0].text

                _chances_r = item.findAll("td")[1].text
                _chances_b = trs_b[trs_r.index(item)].findAll("td")[1].text

                _consts_r = dic_types[i][str(trs_r.index(item)-1)]['consts_r'] + int(("").join(_chances_r.split("%")[0].split(".")))
                _consts_b = dic_types[i][str(trs_r.index(item)-1)]['consts_b'] + int(("").join(_chances_b.split("%")[0].split(".")))

            dic_types[i][str(trs_r.index(item))] = {"itemname" : _itemname, "chances_r" : _chances_r, "consts_r" : _consts_r, "chances_b" : _chances_b, "consts_b" : _consts_b,"count" : 0}

    MasterPieceLists = {'date' : _date, types[0] : dic_types[0], types[1] : dic_types[1], types[2] : dic_types[2], types[3] : dic_types[3], types[4] : dic_types[4]}

    json_obj = json.dumps(MasterPieceLists, indent=4)

    file = open("data/piece.json",'w')
    file.write(json_obj)
    file.close()

    return MasterPieceLists
    
def getMasterPieceUpdateDate():
    url = 'https://maplestory.nexon.com/News/CashShop'
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    div = bs_obj.find("div", {"class" : "cash_board"})
    lis = div.findAll("li")

    _start = -1
    _end = -1

    for item in lis:
        if item.find("dd", {"class" : "data"}).find("a").text.find('로얄스타일') > 0:
            _start = ("").join(item.find("dd", {"class" : "date"}).text.split(" ~ ")[0].split("\n")[1].split("."))
            _end = ("").join(item.find("dd", {"class" : "date"}).text.split(" ~ ")[1].split("\n")[0].split("."))
    result = {'start' : _start, 'end' : _end}
    return result

def needUpdate():
    needUpdate = True
    try:
        json_obj = open('data/royal.json').read()
        py_obj = json.loads(json_obj)

        if int(py_obj['date']['end']) >= int(getMasterPieceUpdateDate()['start']):
            needUpdate = False
    except:
        print('no file')

    return needUpdate