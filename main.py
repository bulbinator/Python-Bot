import discord

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
  print('We have logged in')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$find'):
    await message.channel.send('hello')


client.run("MTA3MjI3MTA0NzI1ODI4MDAwNw.GElQD_.3PqLhbjEv1u9A7WOaU53aK_CFiIObiD0UcUpBE")
