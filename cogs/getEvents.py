import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random

class getEvents(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.Cog.listener()
    async def on_ready(self):
        print("{} is loaded Successfully!".format(self.__class__))

    @commands.command(aliases = ['이벤트'])
    async def getEventsInfo(self, message, index=None):
        url = "https://maplestory.nexon.com/News/Event"

        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")

        EventsLists = getEventsLists(bs_obj)
        if index==None:
            string = '```d\n'
            for i in range(int(len(EventsLists)/5)):
                if i<9:
                    string += '[# {}] {}\n'.format(i+1, EventsLists['title'+str(i)])
                else:
                    string += '[#{}] {}\n'.format(i+1, EventsLists['title'+str(i)])
            string += '```\n'

            embed = discord.Embed(
                title = '⭐진행중인 이벤트',
                description = string + '`;;이벤트 [번호]` 를 사용하여 자세한 내용을 확인합니다.\n예) `;;이벤트 1`',
                url = url,
                colour = discord.Colour.red()
            )
            await message.channel.send(embed=embed)
        else:
            number = int(index)-1
            embed = discord.Embed(
                colour = discord.Colour.red(),
            )
            embed.set_author(name='⭐진행중인 이벤트({}/{})'.format(number+1,int(len(EventsLists)/5)))

            embed.add_field(name='───────────────',
                value =
    """
    **#{}** **{}** [바로가기]({})
    [{} ~ {}]
    """.format(
                        number+1,
                        EventsLists['title'+str(number)],
                        EventsLists['link'+str(number)],
                        EventsLists['start'+str(number)],
                        EventsLists['end'+str(number)],

                        )
                , inline = False
            )
            embed.set_footer(text=url)
            
            img_fname = 'events'+str(number)+'.jpg'
            img_url = EventsLists['img'+str(number)]
            r = requests.get(img_url)
            
            open('data/img/'+img_fname,'wb').write(r.content)

            _file = discord.File('data/img/'+img_fname, filename=img_fname)
            embed.set_image(url='attachment://'+img_fname)

            await message.channel.send(file=_file, embed=embed)

def setup(client):
    client.add_cog(getEvents(client))

def getEventsLists(bs_obj):
    div = bs_obj.find("div", {"class" : "event_board"})
    ul = div.find("ul")
    lis = ul.findAll("li")

    EventsLists = {}

    for i in range(len(lis)):
        dd_data = lis[i].find("dd", {"class" : "data"})
        dd_date = lis[i].find("dd", {"class" : "date"})


        EventsLists['title'+str(i)] = dd_data.find("a").text
        EventsLists['link'+str(i)] = 'https://maplestory.nexon.com' + dd_data.find("a")['href']
        EventsLists['start'+str(i)] = dd_date.text.split(" ~ ")[0].split("\n")[1]
        EventsLists['end'+str(i)] = dd_date.text.split(" ~ ")[1].split("\n")[0]
        EventsLists['img'+str(i)] = lis[i].find("img")['src']

    return EventsLists