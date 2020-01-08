import discord
from discord.ext import commands
import re

class Meta(commands.Cog, name='Meta'):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def roles(self, ctx):
        roles = ctx.message.author.roles
        output = ''
        for role in roles:
            output += role.name
            output += ' (id: '
            output += str(role.id)
            output += ')\n'
        output = re.sub('[@]', '', output)
        embed=discord.Embed(title="List of your roles:", description=output, color=0x6464db)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Meta(client))