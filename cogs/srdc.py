import discord
from discord.ext import commands
import srcomapi, srcomapi.datatypes as dt
import json

with open('srdc.json', 'r') as f:
    speedgames = json.load(f)

games = list(speedgames.keys())
api = srcomapi.SpeedrunCom(); api.debug = 1

class Srdc(commands.Cog, name='SRDC'):
    def __init__(self, client):
        self.client = client

    #placeholder, inactive cog


def setup(client):
    client.add_cog(Srdc(client))