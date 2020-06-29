import discord
from discord.ext import commands

class SampleCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("{} is loaded Successfully!".format(self.__class__))


    # Events #Example-1
    @commands.Cog.listener()
    async def on_ready(self):
        print("{} is loaded Successfully!".format(self.__class__))

    # Commands Example-1
    @commands.command()
    @commands.has_role('MapleBotDeveloper')
    async def sample_one(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)

    # Commands Example-2
    @commands.command()
    async def sample_two(self, ctx):
        await ctx.send('ping')

def setup(client):
    client.add_cog(SampleCog(client))