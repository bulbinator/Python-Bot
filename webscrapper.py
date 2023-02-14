import discord
import re
import requests
import json
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
import textwrap
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

def sol(link):
  r = requests.get(link)
        
  soup = BeautifulSoup(r.content, "html.parser")

  title = soup.find("td", {"class": "block_title"})
  title = title.get_text()
  title = title.split("-")
  book = title[0]
  author = title[1]
  volume = title[2]
  pagenum = title[-1]

  text = soup.find("div", {"class": "text"})
  text = text.get_text()

  footnote = ""

  if soup.find("div", {"class": "footnote"}):     
    footnote = soup.find("div", {"class": "footnote"})
    footnote = footnote.get_text()
    


  engnum = soup.find("span", {"class": "currentpage"})
  engnum = engnum.get_text()


  num = ""
  
  chaptert = soup.find_all("tbody")
  chapter = ""
  for i in chaptert:
    tbody = i.get_text()
    tbody = tbody.split()
    if engnum == tbody[-1]:
      #print("found")
      #print(tbody)
      num = tbody[-1]
      for j in tbody:
        if j.isdigit():
          tbody.remove(j)
      chapter = " ".join(tbody)
      break

  if num == "":
      chaptert.reverse()
      for i in chaptert:
        tbody = i.get_text()
        tbody = tbody.split()
        num = int(tbody[-1])
        if num < int(engnum):
          #print("another chapter found")
          #print(tbody)
          num = tbody[-1]
          for j in tbody:
            if j.isdigit():
              tbody.remove(j)
          chapter = " ".join(tbody)
          break


        
      
  return {
      "book": book,
      "author": author,
      "volume": volume,
      "pagenum": pagenum,
      "text": text,
      "footnote": footnote,
      "chapter": chapter,
      }


def sol_send(hadith):
    #page = 1
    #pages = textwrap.wrap(english, 1200)
    #page = pages[page - 1]
    #num_pages = len(pages)
  
    embed = discord.Embed(title = hadith["chapter"], description = hadith["text"], color = 0xe0ebed)
    embed.set_author(name= f"{hadith['book']} - {hadith['author']}", icon_url="https://i.ibb.co/d2dHnvG/sol.png")
    embed.add_field(name="مصدر: ", value= f"{hadith['volume']} - {hadith['pagenum']}", inline=False)
    return embed
  
