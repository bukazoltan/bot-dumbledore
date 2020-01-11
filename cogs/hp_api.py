import discord
from discord.ext import commands
import json
import requests
import random
import difflib
import wikia
import os
from pathlib import Path

text_folder = Path("assets/text/")


d_quotes = open(text_folder / "d_quotes.txt", 'r').readlines()
d_images = open(text_folder / "d_images.txt",'r').readlines()

houses = [
    {"name": "Slytherin", "desc": "Slytherin house values ambition, cunning and resourcefulness and was founded by Salazar Slytherin. Its emblematic animal is the serpent, and its colours are emerald green and silver.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/d/d3/0.61_Slytherin_Crest_Transparent.png/revision/latest?cb=20161020182557", "color": 0x00c400},
    {"name": "Gryffindor", "desc": "Gryffindor values bravery, daring, nerve, and chivalry. Its emblematic animal is the lion and its colours are scarlet and gold.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/8/8e/0.31_Gryffindor_Crest_Transparent.png/revision/latest?cb=20161124074004", "color": 0xae0001},
    {"name": "Ravenclaw", "desc": "Ravenclaw values intelligence, knowledge, and wit. Its emblematic animal is the eagle, and its colours are blue and bronze.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/2/29/0.41_Ravenclaw_Crest_Transparent.png/revision/latest?cb=20161020182442", "color": 0x222f5b},
    {"name": "Hufflepuff", "desc":"Hufflepuff values hard work, dedication, patience, loyalty, and fair play. Its emblematic animal is the badger, and Yellow and Black are its colours.", "url": "https://vignette.wikia.nocookie.net/harrypotter/images/5/50/0.51_Hufflepuff_Crest_Transparent.png/revision/latest?cb=20161020182518", "color": 0xecb939}
    ]

sh_random = ["You should be in ", "You belong in ", "In my expert opinion, the best house for you would be ", "You could fit in well with the people in ", "The best house for you would be ", "It's a hard choice but probably ", "You might hate me for that but you belong in ", "Hmm... Hard choice... maybe "]


class Hp_api(commands.Cog, name='HP API'):
    def __init__(self, client):
        self.client = client

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