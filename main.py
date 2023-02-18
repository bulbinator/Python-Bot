import discord, asyncio
import re
import requests
import json
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
from functions import *
from webscrapper import *
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from discord.ext import commands
from keep_alive import keep_alive


intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)





@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@client.event
async def on_message(message):
  if 'https://thaqalayn.net/hadith' in message.content:
    link = message.content.split()
    for i in link:
      if 'https://thaqalayn.net/hadith' in i:
        hadith = linked(i)
        embed = send(hadith)
        view = linked_menu(0, hadith["pages"], embed)
        if len(hadith["pages"]) > 1:
          await message.channel.send(embed=embed,view=view, reference=message, mention_author=False)
        else:
          await message.channel.send(embed=embed, reference=message, mention_author=False)
        
  if "http://shiaonlinelibrary.com/" in message.content:
    link = message.content.split()
    for i in link:
      if 'http://shiaonlinelibrary.com/' in i:
        hadith = sol(i)
        embed = sol_send(hadith)
        await message.channel.send(embed=embed,reference=message, mention_author=False)


class Menu(discord.ui.View):
  def __init__(self, page, pages: list[str], embed: discord.Embed, interaction: discord.Interaction):
    super().__init__(timeout=None)
    self.value = None
    self.page = page
    self.pages = pages
    self.embed = embed
    self.num_pages = len(pages)
    self.original_interaction = interaction

      
  @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.secondary)
  async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
      if self.page == 0:
        self.page = 1
      self.embed.description = self.pages[self.page - 1]
      self.page -= 1
      self.embed.set_footer(text=f'Page {self.page + 1} of {self.num_pages}')
      await interaction.response.edit_message(embed=self.embed)


  

  @discord.ui.button(label="Next Page", style=discord.ButtonStyle.primary)
  async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
    try:
      self.embed.description = self.pages[self.page + 1]
      self.page += 1
      self.embed.set_footer(text=f'Page {self.page + 1} of {self.num_pages}')
      
      await interaction.response.edit_message(embed=self.embed)
    except IndexError:
      self.embed.set_footer(text=f'Page {self.page + 1} of {self.num_pages}')
      await interaction.response.edit_message(embed=self.embed)





class linked_menu(discord.ui.View):
  def __init__(self, page, pages: list[str], embed: discord.Embed):
    super().__init__(timeout=None)
    self.value = None
    self.page = page
    self.pages = pages
    self.embed = embed
    self.num_pages = len(pages)

      
  @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.secondary)
  async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
    
    if self.page == 0:
      self.page = 1
    self.embed.description = self.pages[self.page - 1]
    self.page -= 1
    self.embed.set_footer(text=f'Page {self.page + 1} of {self.num_pages}')
    await interaction.response.edit_message(embed=self.embed)


  

  @discord.ui.button(label="Next Page", style=discord.ButtonStyle.primary)
  async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.num_pages > 1:
      button.disabled = False
    try:
      self.embed.description = self.pages[self.page + 1]
      self.page += 1
      self.embed.set_footer(text=f'Page {self.page + 1} of {self.num_pages}')
      
      await interaction.response.edit_message(embed=self.embed)
    except IndexError:
      self.embed.set_footer(text=f'Page {self.page + 1} of {self.num_pages}')
      await interaction.response.edit_message(embed=self.embed)




@tree.command(name = "search", description = "Search for a hadith.")
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
        view = Menu(0, hadith["pages"], embed, interaction)
        if len(hadith["pages"]) > 1:
          await interaction.response.send_message(embed=embed, view=view)
        else:
          await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")
      else:
        embed = asend(hadith)
        view = Menu(0, hadith["ara_pages"], embed, interaction)
        if len(hadith["ara_pages"]) > 1:
          await interaction.response.send_message(embed=embed, view=view)
        else:
          await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")



@tree.command(name = "hadith", description = "Find a hadith.")
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
      view = Menu(0, hadith["pages"], embed, interaction)
      if len(hadith["pages"]) > 1:
        await interaction.response.send_message(embed=embed, view=view)
      else:
        await interaction.response.send_message(embed=embed)
    else:
      embed = asend(hadith)
      view = Menu(0, hadith["ara_pages"], embed, interaction)
      if len(hadith["ara_pages"]) > 1:
        await interaction.response.send_message(embed=embed, view=view)
      else:
        await interaction.response.send_message(embed=embed)



@tree.command(name = "random", description = "Sends a random hadith.")
async def random(interaction: discord.Interaction):
  hadith = randomh()
  embed = send(hadith)
  view = Menu(0, hadith["pages"], embed, interaction)
  if len(hadith["pages"]) > 1:
    await interaction.response.send_message(embed=embed, view=view)
  else:
    await interaction.response.send_message(embed=embed)
  

@tree.command(name = "salawat", description = "Recites salawat.")
async def link(interaction: discord.Interaction):
  await interaction.response.send_message("اللهم صل علی محمد و آل محمد و عجل فرجهم")
        


@tree.command(name = "search_in", description = "Search for a hadith in a specific book.")
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
        view = Menu(0, hadith["pages"], embed, interaction)
        if len(hadith["pages"]) > 1:
          await interaction.response.send_message(embed=embed, view=view)
        else:
          await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")
      else:
        embed = asend(hadith)
        view = Menu(0, hadith["ara_pages"], embed, interaction)
        if len(hadith["ara_pages"]) > 1:
          await interaction.response.send_message(embed=embed, view=view)
        else:
          await interaction.response.send_message(embed=embed)
        if hadith["more"] == True:
          await interaction.followup.send(f"I found more than one narrations with those keywords, [click here]({hadith['link']}) to view them.")


@tree.command(name = "madad", description = "Returns the bot's functions.")
async def madad(interaction: discord.Interaction):
  await interaction.response.send_message("'/hadith' function takes the name of a hadith book and the hadith number and returns the requested hadith from thaqalayn.\n'/search' function requires you enter the exact keywords of a hadith in english or arabic and returns the requested hadith from thaqalayn.\n'/search in' function lets you search for a query in a specific book\n/link' function requires you enter a valid link to a hadith on thaqalyn, and it returns that hadith.\n'/random' function just sends a random hadith lol")





keep_alive()
client.run("MTA3MjI3MTA0NzI1ODI4MDAwNw.Gk6ZWS.S5dz4I0YgaZfYVe5NjLS6XBIhxhFifqe5g6oOM")
