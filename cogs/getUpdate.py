import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class getUpdate(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.Cog.listener()
    async def on_ready(self):
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases=['업데이트'])
    async def LoadsUpdateInfo(self, message):
        url = "https://maplestory.nexon.com/News/Update"

        number = 0
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")

        patchnotes = getUpdateLists(bs_obj)

        embed = discord.Embed(
            colour = discord.Colour.red(),
        )
        embed.set_author(name='패치 내역', icon_url='https://ssl.nx.com/s2/game/maplestory/renewal/common/category_icon01.png')

        embed.add_field(name='───────────────',
            value =
"""

**#{}** [{}] [바로가기]({}) \n**{}**

**#{}** [{}] [바로가기]({}) \n**{}**

**#{}** [{}] [바로가기]({}) \n**{}**

**#{}** [{}] [바로가기]({}) \n**{}**

**#{}** [{}] [바로가기]({}) \n**{}**

""".format(
                    str(number+1),
                    patchnotes['date'+str(number)],
                    patchnotes['link'+str(number)],
                    patchnotes['title'+str(number)],

                    str(number+2),
                    patchnotes['date'+str(number+1)],
                    patchnotes['link'+str(number+1)],
                    patchnotes['title'+str(number+1)],
                    
                    str(number+3),
                    patchnotes['date'+str(number+2)],
                    patchnotes['link'+str(number+2)],
                    patchnotes['title'+str(number+2)],

                    str(number+4),
                    patchnotes['date'+str(number+3)],
                    patchnotes['link'+str(number+3)],
                    patchnotes['title'+str(number+3)],

                    str(number+5),
                    patchnotes['date'+str(number+4)],
                    patchnotes['link'+str(number+4)],
                    patchnotes['title'+str(number+4)],
                    )
            , inline = False
        )
        embed.set_footer(text=url)
        
        embed.set_image(url='https://ssl.nx.com/s2/game/maplestory/renewal/common/test_world_icon_on.png')
        await message.channel.send(embed=embed)

def setup(client):
    client.add_cog(getUpdate(client))

def getUpdateLists(bs_obj):
    div = bs_obj.find("div", {"class" : "update_board"})
    ul = div.find("ul")
    lis = ul.findAll("li")

    patchnotes = {}

    for i in range(len(lis)):
        patchnotes['title'+str(i)] = lis[i].find("span").text
        patchnotes['link'+str(i)] = "https://maplestory.nexon.com" + lis[i].find("a")['href']
        patchnotes['date'+str(i)] = lis[i].find("dd").text

    return patchnotes