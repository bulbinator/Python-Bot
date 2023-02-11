import discord, asyncio
import re
import requests
import json
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
from functions import *
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from discord.ext import commands


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)





@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1072270741501907094))
    print("Ready!")


class Menu(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

  @discord.ui.button(label="Send Message", style=discord.ButtonStyle.grey)
  async def menu1(self, button: discord.ui.Button, interaction: discord.Interaction):
    await interaction.response.send_message("Hello you clicked me")


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
        view = Menu()
        await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")
      else:
        embed = asend(hadith)
        await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")



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
        await interaction.response.defer()
        await asyncio.sleep(4)
        await interaction.followup.send(embed=embed)
      else:
        embed = asend(hadith)
        await interaction.response.defer()
        await asyncio.sleep(4)
        await interaction.followup.send(embed=embed)
        


@tree.command(name = "search_in", description = "Search for a hadith in a specific book.", guild=discord.Object(id=1072270741501907094))
@app_commands.describe(keywords = "Enter the keywords of the hadith", book = "Enter book.",lang = "English or Arabic?")
@app_commands.choices(lang = [
  Choice(name = "English", value = "1"),
  Choice(name = "Arabic", value = "2")
])
@app_commands.choices(book = dict_choice(book_dict()))
async def search_in(interaction: discord.Interaction, keywords: str, book: str,lang: str):
    hadith = search_book(keywords, book)
    if hadith == 0:
      await interaction.response.send_message("404. Hadith not found. Make sure to be specific and enter exact keywords!")
    else:
      if lang == "1":
        embed = send(hadith)
        await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")
      else:
        embed = asend(hadith)
        await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")


@tree.command(name = "madad", description = "Returns the bot's functions.", guild=discord.Object(id=1072270741501907094))
async def madad(interaction: discord.Interaction):
  await interaction.response.send_message("'/hadith' function takes the name of a hadith book and the hadith number and returns the requested hadith from thaqalayn.\n'/search' function requires you enter the exact keywords of a hadith in english or arabic and returns the requested hadith from thaqalayn.\n'/search in' function lets you search for a query in a specific book\n/link' function requires you enter a valid link to a hadith on thaqalyn, and it returns that hadith.\n'/random' function just sends a random hadith lol")



client.run(TOKEN)
