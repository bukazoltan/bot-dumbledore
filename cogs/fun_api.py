import discord
from discord.ext import commands
import requests
import json
import random
from pathlib import Path

text_folder = Path("assets/text/")

dices = ["https://upload.wikimedia.org/wikipedia/commons/2/2c/Alea_1.png",
        "https://upload.wikimedia.org/wikipedia/commons/b/b8/Alea_2.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/2f/Alea_3.png",
        "https://upload.wikimedia.org/wikipedia/commons/8/8d/Alea_4.png",
        "https://upload.wikimedia.org/wikipedia/commons/5/55/Alea_5.png",
        "https://upload.wikimedia.org/wikipedia/commons/f/f4/Alea_6.png"]

cat_root = "https://cat-fact.herokuapp.com/facts"

file = open(text_folder / 'nixxo_quotes.txt', 'r', encoding="latin-1")
nixxo_quotes = file.readlines()

with open(text_folder / 'hp1.txt', 'r', encoding="latin-1") as content_file:
    content = content_file.read()

hp1_book = content.split("\n\n")

'''cat_response = requests.get(cat_root).json()
cat_fact_list = cat_response["all"]'''

class Fun_api(commands.Cog, name='Fun API'):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hp1(self, ctx, id : str = None):
        quote_exists = False
        if id == None or id.isdigit():
            if id == None:
                quote = random.choice(hp1_book)
                quote_exists = True
            elif int(id) > (len(hp1_book)) or int(id) < 1:
                quote_exists = False
                await ctx.send("We don't have a quote with that ID yet.")
            else:
                quote = hp1_book[int(id)-1]
                quote_exists = True
        else:
            await ctx.send("That input doesn't make any sense, you dumbo.")
        if quote_exists:
            image = "https://m.media-amazon.com/images/I/61Nfa2cpWcL._SL500_.jpg"
            embed = discord.Embed(title="A quote from HP1 for you", description=quote)
            embed.set_thumbnail(url=image)
            await ctx.send(embed=embed)

    @commands.command()
    async def nixxoquote(self, ctx, id : str = None):
        quote_exists = False
        if id == None or id.isdigit():
            if id == None:
                quote = random.choice(nixxo_quotes)
                quote_exists = True
            elif int(id) > (len(nixxo_quotes)) or int(id) < 1:
                quote_exists = False
                await ctx.send("We don't have a quote with that ID yet.")
            else:
                quote = nixxo_quotes[int(id)-1]
                quote_exists = True
        else:
            await ctx.send("That input doesn't make any sense, you dumbo.")
        if quote_exists:
            image = "https://cdn.discordapp.com/attachments/534708305663098890/547809088013336576/emote.png"
            embed = discord.Embed(title="A great Nixxo quote", description=quote)
            embed.set_thumbnail(url=image)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def country(self, ctx, country):
        if len(country) < 4:
            base = "https://restcountries.eu/rest/v2/alpha/"
            search_by_name = False
        elif len(country) >= 4:
            search_by_name = True
            base = "https://restcountries.eu/rest/v2/name/"
        country_url = base + country
        country_data = requests.get(country_url).json()
        if search_by_name == True:
            country_data = country_data[0]
        name = country_data["name"]
        flag_url_base = "https://www.countryflags.io/"
        flag = flag_url_base + country_data["alpha2Code"] + "/shiny/64.png"
        print(flag)
        japanese = country_data["translations"]["ja"]
        population = "%i people" % (country_data["population"])
        area = "%i km2" % (country_data["area"])
        if len(country_data["borders"]) > 1:
            borders = ", ".join(country_data["borders"])
        elif len(country_data["borders"]) == 0:
            borders = "No bordering countries."
        else:
            borders = country_data["borders"][0]
        if len(country_data["timezones"]) > 1:
            timezones = ', '.join(country_data["timezones"])
        else:
            timezones = country_data["timezones"][0]

        embed=discord.Embed(title=name, color=0x6b93ed)
        embed.set_thumbnail(url=flag)
        embed.add_field(name="Population:", value=population, inline=True)
        embed.add_field(name="Area:", value=area, inline=True)
        embed.add_field(name="Timezones:", value=timezones, inline=True)
        embed.add_field(name="Japanese name:", value=japanese, inline=True)
        embed.add_field(name="Bordering countries:", value=borders, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def chuck(self, ctx):
        response = requests.get('https://api.chucknorris.io/jokes/random').json()
        joke = response["value"]
        image = response["url"]
        embed=discord.Embed(title="Here's a Chuck Norris joke for you.", color=0x6b93ed, description=joke)
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    async def number(self, ctx, number):
        if number.isnumeric():
            numbers_base_url = 'http://numbersapi.com/'
            response = requests.get(numbers_base_url + number)
            number_fact = response.text
            embed=discord.Embed(title="Here's a random number fact for you:", color=0x6b93ed, description=number_fact)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Are you sure that's a number?")


    @commands.command()
    async def beer(self, ctx):
        flag_url_base = "https://www.countryflags.io/"

        resp = requests.get('http://prost.herokuapp.com/api/v1/beer/rand').json()
        name = "Your random beer is: " + resp["title"]
        if resp["abv"]:
            abv = resp["abv"] + "%"
        else:
            abv = "No data"
        og = resp["og"]
        nation_code = resp["country"]["key"]
        if resp["brewery"]:
            brewery = resp["brewery"]["title"]
        else:
            brewery = "No data"
        country = resp["country"]["title"]
        flag = flag_url_base + nation_code + "/shiny/64.png"

        embed =discord.Embed(title=name, color=0x6b93ed)
        embed.set_thumbnail(url=flag)
        embed.add_field(name="Alcohol By Volume: ", value=abv, inline=True)
        embed.add_field(name="Original Gravity: ", value=og, inline=True)
        embed.add_field(name="Brewery: ", value=brewery, inline=True)
        embed.add_field(name="Nationality: ", value=country, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def dice(self, ctx, amount: int):
        for i in range(1, amount):
            value = random.randint(1, 6)
        img = dices[value-1]
        embed =discord.Embed(title="Your throw:", color=0x6b93ed)
        embed.set_thumbnail(url=img)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun_api(client))