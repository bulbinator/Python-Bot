import discord
import re
import requests
import json
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
from functions import *
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)





@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1072270741501907094))
    print("Ready!")

@tree.command(name = "search", description = "Search for a hadith.", guild=discord.Object(id=1072270741501907094))
@app_commands.describe(keywords = "Enter the keywords of the hadith", lang = "English or Arabic?")
@app_commands.choices(lang = [
  Choice(name = "English", value = "1"),
  Choice(name = "Arabic", value = "2")
])
async def search(interaction: discord.Interaction, keywords: str, lang: str):
    hadith = get_hadith(keywords)
    if hadith == 0:
      await interaction.response.send_message("404. Hadith not found. Make sure to be specific and enter exact keywords!")
    else:
      if lang == "1":
        embed = send(hadith)
        await interaction.response.send_message(embed=embed)
      else:
        embed = asend(hadith)
        await interaction.response.send_message(embed=embed)



@tree.command(name = "hadith", description = "Find a hadith.", guild=discord.Object(id=1072270741501907094))
@app_commands.describe(lang = "English or Arabic?", book = "Enter book.", hadith_number = "Enter hadith number")
@app_commands.choices(book = dict_choice(book_dict()))
@app_commands.choices(lang = [
  Choice(name = "English", value = "1"),
  Choice(name = "Arabic", value = "2")
])
async def hadith(interaction: discord.Interaction, lang: str, book: str, hadith_number: str):
  hadith = choices(book, hadith_number)
  if hadith == 0:
    await interaction.response.send_message("404. Hadith not found. Make sure you enetered the correct information!")
  else:
    if lang == "1":
      embed = send(hadith)
      await interaction.response.send_message(embed=embed)
    else:
      embed = asend(hadith)
      await interaction.response.send_message(embed=embed)



@tree.command(name = "random", description = "Sends a random hadith.", guild=discord.Object(id=1072270741501907094))
async def random(interaction: discord.Interaction):
  hadith = randomh()
  embed = send(hadith)
  await interaction.response.send_message(embed=embed)
  

@tree.command(name = "link", description = "Returns the linked hadith.", guild=discord.Object(id=1072270741501907094))
@app_commands.describe(link = "Enter link.", lang = "English or Arabic?")
@app_commands.choices(lang = [
  Choice(name = "English", value = "1"),
  Choice(name = "Arabic", value = "2")
])
async def link(interaction: discord.Interaction, link: str, lang: str):
    hadith = linked(link)
    if hadith == 0:
      await interaction.response.send_message("Enter a valid url!")
    else:
      if lang == "1":
        embed = send(hadith)
        await interaction.response.send_message(embed=embed)
      else:
        embed = asend(hadith)
        await interaction.response.send_message(embed=embed)


@tree.command(name = "status", description = "Returns the status of the bot.", guild=discord.Object(id=1072270741501907094))
async def link(interaction: discord.Interaction):
  await interaction.response.send_message("الحمد لله على كل حال!")



client.run(TOKEN)
