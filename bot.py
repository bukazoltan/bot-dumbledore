import discord
import re
import random
import configparser
from discord.utils import get
from discord.ext import commands
import asyncio
from itertools import cycle
import json
import time
import os

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['LOGIN']['token']

client = commands.Bot(command_prefix = '%')
client.remove_command('help')
extensions = ['meta', 'hp_api', 'housecup', 'reaction', 'fun_api', 'mod']
extensions_route = "cogs."
bot_dir = os.path.dirname(__file__)
points_log_path = os.path.join(bot_dir, "assets/point_log.txt")
points_path = os.path.join(bot_dir, "assets/points.json")
points_2018_path = os.path.join(bot_dir, "assets/points2018.json")
points_2019_1 = os.path.join(bot_dir, "assets/points_2019_01.json")

status = ['with your minds', 'with your hearts', 'with your bodies', 'with your nerves']
hp_mod_commands = ['give', 'add', 'set', 'subtract', 'remove']
dumbledore_positive = ['Yes, you are the headmaster! Nice beard.', 'Yep. You are Dumbledore. A mirror would be much simpler though. I don\'t recommend the Mirror of Erised.', 'Yes, you are the headmaster but be careful, with great power come great memes.', 'Yeah, you are the headmaster, now let\'s go and give some random points.']
dumbledore_negative = ['No, *I* am Dumbledore.', 'You might be Spartacus, but you are not Dumbledore.', 'Stop checking this, you fool.', 'You might be Jude Law but that doesn\'t mean that you are Dumbledore.', 'Nah, you are not Dumbledore. Git gud.']

def point_mng(house, command, amount):
    if amount < 0:
        return "Don't play with negatives, boy!"
    elif amount == 0:
        return "Giving 0 points is a dick move, even by Dumbledore standards."
    with open(points_path, 'r') as f:
        points = json.load(f)
        if command in hp_mod_commands:
            if command == "give" or command == "add":
                points[house] += amount
                message = "%s has recieved %d point(s). They have %d point(s) now." % (house, amount, points[house])

            if command == "remove" or command == "subtract":
                points[house] -= amount
                message = "%s has %d point(s) less now. They have %d point(s) now." % (house, amount, points[house])
            if command == "set":
                points[house] = amount
                message = "%s has %d point(s) now." % (house, points[house])
        else:
            return "That's not how this works."
        with open(points_path, 'w') as outfile:
            json.dump(points, outfile)
        return message

def point_log(house, command, amount, reason, point_giver):
    reason_string = " ".join(reason)
    date = time.asctime( time.localtime(time.time()) )
    with open(points_log_path, "a") as myfile:
        myfile.write("House: %s | action: %s | %d points | Given by: %s | Reason: %s | %s \n" % (house, command, amount, point_giver, reason_string, date))

def find_winner_color(points):
    winner = max(zip(points.values(), points.keys()))
    if winner[1] == "Slytherin":
        return 0x00c400
    elif winner[1] == "Gryffindor":
        return 0xae0001
    elif winner[1] == "Ravenclaw":
        return 0x222f5b
    elif winner[1] == "Hufflepuff":
        return 0xecb939

@client.event
async def on_ready():
    print('The bot is ready to serve!')
    game = discord.Game("with your nerves")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.command()
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def load(ctx, extension):
    try:
        client.load_extension(extensions_route + extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def unload(ctx, extension):
    try:
        client.unload_extension(extensions_route + extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))

@client.command()
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def reload(ctx, extension):
    try:
        client.reload_extension(extensions_route + extension)
        print('Reloaded {}'.format(extension))
        await ctx.send('Reloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be reloaded. [{}]'.format(extension, error))
        await ctx.send('{} cannot be reloaded. [{}]'.format(extension, error))

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extensions_route + extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
async def points(ctx, year=None):
    if year is None:
        with open(points_path, 'r') as f:
            points = json.load(f)
    elif year == '2018':
        with open(points_2018_path, 'r') as f:
            points = json.load(f)
    elif year == '2019-1':
        with open(points_2019_1, 'r') as f:
            points = json.load(f)


    winner_color = find_winner_color(points)
    embed=discord.Embed(description="Current Standing of The House Cup", color=winner_color)
    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/model-hogwarts/images/d/dc/House_Cup.png/revision/latest?cb=20171021204608")
    embed.add_field(name="Gryffindor", value=points["Gryffindor"], inline=True)
    embed.add_field(name="Slytherin", value=points["Slytherin"], inline=True)
    embed.add_field(name="Hufflepuff", value=points["Hufflepuff"], inline=True)
    embed.add_field(name="Ravenclaw", value=points["Ravenclaw"], inline=True)

    await ctx.send(embed=embed)

@client.command(name="gryffindor", pass_context=True, aliases=['g'])
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def gryffindor(ctx, command: str, amount: int, *reason):
    point_log("Gryffindor", command, amount, reason, ctx.message.author.name)
    await ctx.send(point_mng("Gryffindor", command, amount))

@client.command(name="slytherin", pass_context=True, aliases=['s'])
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def gryffindor(ctx, command: str, amount: int, *reason):
    point_log("Slytherin", command, amount, reason, ctx.message.author.name)
    await ctx.send(point_mng("Slytherin", command, amount))

@client.command(name="hufflepuff", pass_context=True, aliases=['h'])
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def gryffindor(ctx, command: str, amount: int, *reason):
    point_log("Hufflepuff", command, amount, reason, ctx.message.author.name)
    await ctx.send(point_mng("Hufflepuff", command, amount))

@client.command(name="ravenclaw", pass_context=True, aliases=['r'])
@commands.has_any_role("🏰Headmaster", "⚗️Professor")
async def gryffindor(ctx, command: str, amount: int, *reason):
    point_log("Ravenclaw", command, amount, reason, ctx.message.author.name)
    await ctx.send(point_mng("Ravenclaw", command, amount))

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    generic=discord.Embed(color=0x6464db)
    generic.set_author(name="Generic server commands")
    generic.add_field(name='/ping', value='Ping the bot to see if it\'s alive.', inline=False)
    generic.add_field(name='/roles', value='List your roles on the server', inline=False)

    house=discord.Embed(color=0x6464db)
    house.set_author(name="House Cup Commands")
    house.add_field(name='/sortinghat', value='The Sorting Hat recommends a house for you if you can\'t make up your mind.', inline=False)
    house.add_field(name='/points', value='Check the standing of the House Cup.', inline=False)
    house.add_field(name='/dumbledore', value='Check whether you have the rights to manage points or not.', inline=False)

    house_mng=discord.Embed(color=0x6464db)
    house_mng.set_author(name="House Cup Management Commands (Dumbledore only!)")
    house_mng.add_field(name='/gryffindor or /g', value='Manage the points of Gryffindor. Usage: /g give|add|set|subtract|remove [points]', inline=False)
    house_mng.add_field(name='/slytherin or /s', value='Manage the points of Syltherin. Usage: /g give|add|set|subtract|remove [points]', inline=False)
    house_mng.add_field(name='/hufflepuff or /h', value='Manage the points of Hufflepuff. Usage: /g give|add|set|subtract|remove [points]', inline=False)
    house_mng.add_field(name='/ravenclaw or /r', value='Manage the points of Ravenclaw. Usage: /g give|add|set|subtract|remove [points]', inline=False)

    hp=discord.Embed(color=0x6464db)
    hp.set_author(name="Harry Potter related commands")
    hp.add_field(name='/spells', value='List all the available spells.', inline=False)
    hp.add_field(name='/spell [spell name]', value='Get information about a specific spell from the spell list.', inline=False)
    hp.add_field(name='/hpwikia [search term]', value='Search the Harry Potter wikia for a specific search term.', inline=False)
    hp.add_field(name='/quote', value='Get a great Dumbledore quote.', inline=False)

    fun=discord.Embed(color=0x6464db)
    fun.set_author(name="Fun API commands")
    fun.add_field(name='/beer', value='Get a random beer.', inline=False)
    fun.add_field(name='/chuck', value='Get a random Chuck Norris joke.', inline=False)
    fun.add_field(name='/number [search term]', value='Get a random fact about a number', inline=False)
    fun.add_field(name='/country [search term]', value='Get information about a country. Use a country code e.g. DE/DEU or Germany', inline=False)
    fun.add_field(name='/nixxoquote [optional: quote id]', value='Get a great Nixxo quote.', inline=False)

    await ctx.send("I've sent you a DM with some guidance, my friend!")
    await author.send(embed=generic)
    await author.send(embed=house)
    await author.send(embed=house_mng)
    await author.send(embed=hp)
    await author.send(embed=fun)


client.run(TOKEN, bot=True, reconnect=True)