import discord
import random
from discord.ext import commands
from discord.utils import get

dumbledore_positive = ['Yes, you are the headmaster! Nice beard.', 'Yep. You are Dumbledore. A mirror would be much simpler though. I don\'t recommend the Mirror of Erised.', 'Yes, you are the headmaster but be careful, with great power come great memes.', 'Yeah, you are the headmaster, now let\'s go and give some random points.']
dumbledore_negative = ['No, *I* am Dumbledore.', 'You might be Spartacus, but you are not Dumbledore.', 'Stop checking this, you fool.', 'You might be Jude Law but that doesn\'t mean that you are Dumbledore.', 'Nah, you are not Dumbledore. Git gud.']


class Housecup(commands.Cog, name='Housecup'):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    async def dumbledore(self, ctx):
        user = ctx.message.author
        dumbledore = get(user.guild.roles, name="dumbledore")
        if dumbledore in user.roles:
            await ctx.send(random.choice(dumbledore_positive))
        else:
            if user.id == "137957034057269248":
                await self.client.say("Fragus, I thought you were better than this! :(")
            elif user.id == "394342606911438868":
                await self.client.say("NotDumbledoreLikeAJ")
            elif user.id == "139450873519669249":
                await self.client.say("Being Dumbledore is basically free, Nixxo!")
            elif user.id == "396022096720953344":
                await self.client.say("Cat... in your dreams.")
            await ctx.send(random.choice(dumbledore_negative))

def setup(client):
    client.add_cog(Housecup(client))
