import discord
from discord.ext import commands
import json
import requests
from bs4 import BeautifulSoup
import urllib3

class getCharacterInfo(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.Cog.listener()
    async def on_ready(self):
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases=['검색'])
    async def Search(self, message, nickname="!0"):
        if nickname == "!0":
            embed = discord.Embed(
                description = "**Error!\n\n**검색할 닉네임을 입력해주세요\n",
                colour = discord.Colour.red()
            )
            await message.channel.send(embed=embed)
            return
        char_default = {}
        char_add = {}
        char_img = {}
        char_union = {}
        char_muleung = {}

        _url = "https://maple.gg/u/" + str(nickname)

        result = requests.get(_url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
                
        try:
            defaultInfo = getDefaultInfo(bs_obj)
            addInfo = getAdditionalInfo(bs_obj)
            unionInfo = getUnionInfo(str(nickname))
            muleungInfo = getMuleungInfo(bs_obj)
        except:
            embed = discord.Embed(
                description = "**Error!\n\n[{}]** 은(는) 존재하지 __않는__ 닉네임입니다.".format(str(nickname)),
                colour = discord.Colour.red()
            )
            await message.channel.send(embed=embed)
        else:
            isReboot = False
            char_default['nickname'] = getNickname(bs_obj)
            char_default['servername'] = getServername(bs_obj)
            if char_default['servername'][:3] == '리부트':
                isReboot = True
            char_default['level'] = defaultInfo[0].split(".")[1]
            char_default['job'] = defaultInfo[1]
            char_default['like'] = defaultInfo[2].split("\n")[1]
            char_default['exp'] = getExp(nickname, isReboot)

            char_union['unionlevel'] = unionInfo[0]
            char_union['uniongrade'] = unionInfo[1]
            char_union['unionpower'] = unionInfo[2]

            char_muleung['recordLevel'] = muleungInfo[0]
            char_muleung['recordTime'] = muleungInfo[1]
            char_muleung['wRank'] = muleungInfo[2]
            char_muleung['aRank'] = muleungInfo[3]

            char_add['guild'] = addInfo[0]
            char_add['a_rank'] = addInfo[1]
            char_add['w_rank'] = addInfo[2]
            char_add['w_job_rank'] = addInfo[3]
            char_add['a_job_rank'] = addInfo[4]

            char_img['profile'] = getProfileImageURL(bs_obj)
            char_img['server'] = getServerImageURL(bs_obj)

            """
            char_info = {"default" : char_default, "union" : char_union, "muleung" : char_muleung, "additional" : char_add, "img" : char_img}
            
            json_obj = json.dumps(char_info, indent=4)

            file = open("data/char.json",'w')
            file.write(json_obj)
            file.close()
            """

            json_obj = open('data/lvexp.json').read()
            py_obj = json.loads(json_obj)

            embed = discord.Embed(
                colour = discord.Colour.red(),
            )
            
            embed.set_footer(text=_url, icon_url=char_img['profile'])
            embed.set_author(name='{} :: {}'.format(char_default['servername'],char_default['nickname']), icon_url='{}'.format(char_img['server']))
            
            embed.add_field(name='{}'.format(getRecentUpdate(bs_obj)),
                value = 
                    """
```fix
{}님 반가워요!
```
**#기본정보───────**
```ini
[레벨] : {}
[경험치] : {:,.0f} ({:.2f}%)
[직업] : {}
[길드] : {}
```
**#랭킹정보───────**
```ini
[종합랭킹] : {}위
[월드랭킹] : {}위
[직업랭킹] : {}위
[월드 내 직업랭킹] : {}위
```
**#유니온정보──────**
`월드 내 최고레벨 캐릭터에게만 표시됩니다.`
```ini
[유니온레벨] : {:,.0f}
[유니온등급] : {}
[공격대 전투력] : {:,.0f}
[시간당 획득코인] : {:.2f}개
```
**#무릉정보──────**
```ini
[최대층수] : {}
[소요시간] : {}
[종합랭킹] : {}
[월드랭킹] : {}
```
                    """.format(
                        char_default['nickname'],

                        char_default['level'],
                        int(char_default['exp']),
                        int(char_default['exp']) / int(py_obj[char_default['level']]) * 100,
                        char_default['job'],
                        char_add['guild'],

                        char_add['a_rank'],
                        char_add['w_rank'],
                        char_add['a_job_rank'],
                        char_add['w_job_rank'],

                        int(char_union['unionlevel']),
                        char_union['uniongrade'],
                        int(char_union['unionpower']),
                        int(char_union['unionpower']) * 3600 / 100000000000,

                        char_muleung['recordLevel'],
                        char_muleung['recordTime'],
                        char_muleung['wRank'],
                        char_muleung['aRank']
                        )
                , inline = True
            )

            img_data = requests.get(char_img['profile']).content
            with open('data/img/profile.png', 'wb') as handler:
                handler.write(img_data)
                
            _file = discord.File("data/img/profile.png", filename="profile.png")
            embed.set_thumbnail(url="attachment://profile.png")

            await message.channel.send(file = _file, embed=embed)

def setup(client):
    client.add_cog(getCharacterInfo(client))

def getNickname(bs_obj):
    basic_div = bs_obj.find("div", {"class": "col-lg-8"})
    nickname = basic_div.find("h3").find("b").text
    return nickname

def getServername(bs_obj):
    basic_div = bs_obj.find("div", {"class": "col-lg-8"})
    h3 = basic_div.find("h3")
    servername = h3.find("img")['alt']
    return servername

def getDefaultInfo(bs_obj):
    basic_div = bs_obj.find("div", {"class": "col-lg-8"})
    default_div = basic_div.find("div", {"class" : "user-summary"})
    default_ul = default_div.find("ul")
    default_lis = default_ul.findAll("li")
    result = [i.text for i in default_lis]
    return result

def getAdditionalInfo(bs_obj):
    result = []
    basic_div = bs_obj.find("div", {"class": "col-lg-8"})
    add_div = basic_div.find("div", {"class" : "row row-normal user-additional"})
    add_divs = add_div.findAll("div")

    for item in add_divs:
        span = item.find("span")
        if span:
            result.append("".join(span.text.split(" "))[:-1].split("\n")[0])
        else:
            result.append(add_divs[0].find("a").text) # Guild
    return result

def getProfileImageURL(bs_obj):
    basic_div = bs_obj.find("div", {"class" : "col-6 col-md-8 col-lg-6"})
    img = basic_div.find("img")
    src = img["src"]
    return src    

def getServerImageURL(bs_obj):
    basic_div = bs_obj.find("div", {"class": "col-lg-8"})
    src = basic_div.find("h3").find("img")['src']
    return src

def getExp(nickname, isReboot):
    try:
        if isReboot == True:
            _url = "https://maplestory.nexon.com/Ranking/World/Total?c=" + str(nickname) + "&w=254"
        else:
            _url = "https://maplestory.nexon.com/Ranking/World/Total?c=" + str(nickname)
        result = requests.get(_url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        tr = bs_obj.find("tr", {"class" : "search_com_chk"})
        strexp = tr.findAll("td")[3].text
        iexp = "".join(strexp.split(","))
        return iexp
    except:
        return -1

def getUnionInfo(nickname):
    url = "https://maplestory.nexon.com/Ranking/Union?c=" + nickname
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    json_obj = open('data/uniongrade.json').read()
    py_obj = json.loads(json_obj)

    tr = bs_obj.find("tr", {"class" : "search_com_chk"})
    try:
        unionLevel = int(("").join(tr.findAll("td")[2].text.split(",")))
    except AttributeError:
        return [0,0,0]
    else:
        v = list(py_obj.values())
        k = list(py_obj.keys())
        
        for i in range(len(v)):
            if unionLevel > int(v[i]):
                unionGrade = k[i]

        unionPower = ("").join(tr.findAll("td")[3].text.split(","))

        return [unionLevel, unionGrade, unionPower]

def getMuleungInfo(bs_obj):
    basic_div = bs_obj.find("div", {"class":"col-lg-3 col-6 mt-3 px-1"})
    try:
        recordLevel = ("").join(("").join(basic_div.find("h1").text.split(" ")).split("\n"))
        recordTime = basic_div.find("small").text
        wRank = basic_div.find("footer").find("div", {"class" : "mb-2"}).findAll("span")[0].text
        aRank = basic_div.find("footer").find("div", {"class" : "mb-2"}).findAll("span")[1].text
    except AttributeError:
        recordLevel = recordTime = wRank = aRank = "정보없음"
    
    result = [recordLevel, recordTime, wRank, aRank]

    return result

def getRecentUpdate(bs_obj):
    basic_div = bs_obj.find("div", {"class":"float-left font-size-12 text-left"})
    date = ("").join(("").join(basic_div.find("span").text.split(" ")).split("\n"))
    return date
