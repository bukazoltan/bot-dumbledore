import discord
from discord.ext import commands

class Reaction(commands.Cog, name='Reaction'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        author = message.author
        lowercase = message.content.lower()

        if 'PS1Hagrid' in message.content and message.author != 'Bot_Dumbledore&#352530':
            hagrid = self.client.get_emoji(496775536341942292)
            await message.add_reaction(hagrid)
            
        if 'LUL' in message.content:
            lul = self.client.get_emoji(517017058043494410)
            await message.add_reaction(lul)

        if '5rt' in message.content:
            fivert = self.client.get_emoji(519287519108661248)
            await message.add_reaction(fivert)

def setup(client):
    client.add_cog(Reaction(client))
