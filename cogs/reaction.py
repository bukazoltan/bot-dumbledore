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

        if 'gay' in lowercase and message.author != 'Bot_Dumbledore&#352530':
            kappa_pride = self.client.get_emoji(500340007266025483)
            await message.add_reaction(kappa_pride)

        if 'tedder' in lowercase and message.author != 'Bot_Dumbledore&#352530':
            dans_game = self.client.get_emoji(500340007593050112)
            await  message.add_reaction(dans_game)

        if 'hp4' in lowercase and message.author != 'Bot_Dumbledore&#352530':
            dans_game = self.client.get_emoji(500340007593050112)
            await message.add_reaction(dans_game)

        if 'raman' in lowercase and message.author != 'Bot_Dumbledore&#352530':
            ramaneyes = self.client.get_emoji(515189353648226347)
            await message.add_reaction(ramaneyes)

        if 'cat' in lowercase and message.author != 'Bot_Dumbledore&#352530':
            cat = self.client.get_emoji(553890018792570880)
            await message.add_reaction(cat)

        if 'kurwa' in lowercase:
            letter_k = "\U0001F1F0"
            letter_u = "\U0001F1FA"
            letter_r = "\U0001F1F7"
            letter_w = "\U0001F1FC"
            letter_a = "\U0001F1E6"

            await message.add_reaction(letter_k)
            await message.add_reaction(letter_u)
            await message.add_reaction(letter_r)
            await message.add_reaction(letter_w)
            await message.add_reaction(letter_a)

        if 'LUL' in message.content:
            lul = self.client.get_emoji(517017058043494410)
            await message.add_reaction(lul)

        if '5rt' in message.content:
            fivert = self.client.get_emoji(519287519108661248)
            await message.add_reaction(fivert)

def setup(client):
    client.add_cog(Reaction(client))