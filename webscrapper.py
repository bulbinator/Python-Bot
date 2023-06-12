import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

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
  
  
def chain():

  book = "الکافي"
  
  pg = "۳۲"
  
  vol = "۵"
  
  search = f"site:hadith.inoor.ir \"نشانی :  {book}  ,  جلد{vol}  ,  صفحه{pg} \""
  print(search)
  
  url = 'https://www.google.com/search'
      
  headers = {
    'Accept' : '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
  }
  parameters = {'q': search}
      
  content = requests.get(url, headers = headers, params = parameters).text
  soup = BeautifulSoup(content, 'html.parser')
      
  search = soup.find(id = 'search')
  link = search.find('a')
  if link == None:
    print("none")
  link = link['href']
  if link:
    link = link.split('/')
    link[-1] = "same-toc"
    link = "/".join(link)
  
  
  
  
  
  
  driver = webdriver.Chrome(options=chrome_options)
  driver.get("https://proxyium.com/")
  
  
  input_box = driver.find_element(By.CLASS_NAME, "form-control")
  input_box.send_keys(link)
  
  
  #button = driver.find_element(By.CLASS_NAME, 'btn ')
  button = driver.find_element(By.CSS_SELECTOR, '.btn, .btn-blue')
  button.click()
  driver.implicitly_wait(5)
  driver.refresh()
  
  
  hadiths = driver.find_element(By.XPATH, "//*[@id='mat-tab-content-0-0']/div/div/div[1]/div").text
  hadiths = {}
  for i in range(10):
    try:
      text = driver.find_element(By.XPATH, f"//*[@id='mat-tab-content-1-2']/div/div/div[{i}]").text
      if "الکافي  ,  جلد۵  ,  صفحه۳۲" in text:
        hadith = driver.find_element(By.XPATH, f"//*[@id='mat-tab-content-{i + 1}-0']/div/div/a[1]").text
        link = driver.find_element(By.XPATH, f"//*[@id='mat-tab-content-{i + 1}-0']/div/div/a[1]").get_attribute("href")
        hadiths[f"{hadith}"] = link
    except:
      pass
  
  #for i in range(len(hadiths)):
    #hadiths[i] = f"{i}. " + hadiths[i]
      
  with open("hadiths.txt", 'w') as f:
    for key, value in hadiths.items():
      f.write('%s:%s\n' % (key, value))

  return hadiths


def chain_embed(hadiths):
  embed = discord.Embed(title = "sanad",)
  embed.add_field(name="مصدر: ", value= f"{hadiths.keys()[0]}", inline=False)
  embed.add_field(name="مصدر: ", value= f"{hadiths.keys()[0]}", inline=False)
  return embed

