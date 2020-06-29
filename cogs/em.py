import discord
from discord.ext import commands

class emoji_test(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Commands Example-1
    @commands.command()
    async def emojiinfo(self, ctx, emoji: discord.Emoji = None):
        """Outputs info about the emoji."""
        
        # emoID = int(emoji.split(":")[2][:-1])
        emo = emoji
        
        embed = discord.Embed(title = "")
        embed.set_author(name = emo.name, icon_url = emo.url)
        embed.set_thumbnail(url = emo.url)
        embed.add_field(name = "ID", value = emo.id, inline = True)
        embed.add_field(name = "Guild", value = str(emo.guild), inline = True)
        embed.add_field(name = "Guild ID", value = str(emo.guild_id), inline = True)
        embed.add_field(name = "user", value = emo.user, inline = True)
        embed.add_field(name = "user", value = emo, inline = True)

        
        await ctx.send(embed = embed)
    
    @commands.command()
    async def getemoji(self, ctx):
        await ctx.send('<:{}:{}>'.format('royalstyle', 718488543764414506))

def setup(client):
    client.add_cog(emoji_test(client))
