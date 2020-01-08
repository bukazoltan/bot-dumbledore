import discord
from discord.ext import commands
import json
import requests
import random
import difflib
import wikia
import os

api_key = "$2a$10$SejjtOVrY2l7cl.CZfBDJuzB5A/737aT0M8DDbdRr96.B8vx1IlNi"
url_base = "https://www.potterapi.com/v1"

spell_list = []

response = requests.get("https://www.potterapi.com/v1/spells?key=$2a$10$SejjtOVrY2l7cl.CZfBDJuzB5A/737aT0M8DDbdRr96.B8vx1IlNi")
spells = response.json()

d_file = open('d_quotes.txt', 'r')
d_quotes = d_file.readlines()
d_images = open('d_images.txt', 'r').readlines()

houses = [
    {"name": "Slytherin", "desc": "Slytherin house values ambition, cunning and resourcefulness and was founded by Salazar Slytherin. Its emblematic animal is the serpent, and its colours are emerald green and silver.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/d/d3/0.61_Slytherin_Crest_Transparent.png/revision/latest?cb=20161020182557", "color": 0x00c400},
    {"name": "Gryffindor", "desc": "Gryffindor values bravery, daring, nerve, and chivalry. Its emblematic animal is the lion and its colours are scarlet and gold.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/8/8e/0.31_Gryffindor_Crest_Transparent.png/revision/latest?cb=20161124074004", "color": 0xae0001},
    {"name": "Ravenclaw", "desc": "Ravenclaw values intelligence, knowledge, and wit. Its emblematic animal is the eagle, and its colours are blue and bronze.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/2/29/0.41_Ravenclaw_Crest_Transparent.png/revision/latest?cb=20161020182442", "color": 0x222f5b},
    {"name": "Hufflepuff", "desc":"Hufflepuff values hard work, dedication, patience, loyalty, and fair play. Its emblematic animal is the badger, and Yellow and Black are its colours.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/5/50/0.51_Hufflepuff_Crest_Transparent.png/revision/latest?cb=20161020182518", "color": 0xecb939}
    ]

sh_random = ["You should be in ", "You belong in ", "In my expert opinion, the best house for you would be ", "You could fit in well with the people in ", "The best house for you would be ", "It's a hard choice but probably ", "You might hate me for that but you belong in ", "Hmm... Hard choice... maybe "]

for spell in spells:
    spell_list.append(spell["spell"])
del spell_list[-1] #There is a double on the API for some reason.


def find_spell_by_name(spells, name):
    for spell in spells:
        if spell["spell"] == name:
            return spell



class Hp_api(commands.Cog, name='HP API'):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spells(self, ctx):
        spell_list_str = ', '.join(spell_list)
        embed=discord.Embed(title="List of spells", description=spell_list_str, color=0x6464db)
        embed.set_thumbnail(url="https://media1.tenor.com/images/c6778ec7f0af4c62075c771ae62288fc/tenor.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def sortinghat(self, ctx):
        house = random.choice(houses)
        title = random.choice(sh_random) + (house["name"]) + "."
        desc = house["desc"]
        url = house["url"]
        color = house["color"]
        house=discord.Embed(title=title, description=desc, color=color)
        house.set_thumbnail(url=url)
        await ctx.send(embed=house)

    @commands.command()
    async def quote(self, ctx):
        quote = random.choice(d_quotes)
        image = random.choice(d_images)
        embed = discord.Embed(title="A great quote from myself.", description=quote)
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)
        print(quote, image)

    @commands.command()
    async def spell(self, ctx, *spell):
        spell = " ".join(spell)
        spell_name = difflib.get_close_matches(spell, spell_list)[0]
        requested_spell = find_spell_by_name(spells, spell_name)
        spell_name = requested_spell["spell"]
        spell_type = requested_spell["type"]
        effect = requested_spell["effect"]
        print(type, effect)
        print(requested_spell)

        embed=discord.Embed(title=spell_name, color=0x6b93ed)
        embed.add_field(name="Type:", value=spell_type, inline=True)
        embed.add_field(name="Effect:", value=effect, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def hpwikia(self, ctx, *searchitems):
        searchitem = " ".join(searchitems)
        found = wikia.search("harrypotter", searchitem)[0]
        summary = wikia.summary("harrypotter", found)
        page = wikia.page("harrypotter", found)
        url = page.url
        clear_url = url.replace(' ', '_')
        image = page.images
        if image == []:
            image = "https://upload.wikimedia.org/wikipedia/commons/e/e5/Coat_of_arms_placeholder_with_question_mark_and_no_border.png"
        else:
            image = image[-1]
        title = page.title

        embed=discord.Embed(title=title, url=clear_url, description=summary)
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Hp_api(client))