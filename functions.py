import discord
import re
import requests
import json
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands



def book_dict():
  response = requests.get("https://www.thaqalayn-api.net/api/allbooks")
  books = response.json()
  book_dict = {}
  for i in range(len(books)):
    book_dict[books[i]["bookId"]] = books[i]["BookName"]
  book_dict["Al-Amali-Saduq"] = "Al-Amālī al Ṣaduq"
  book_dict["Al-Amali-Mufid"] = "Al-Amālī al Mufīd"
  book_dict["Kitab-al-Ghayba-Numani"] = "Kitāb al-Ghayba al-Nuʿmānī"
  book_dict["Kitab-al-Ghayba-Tusi"] = "Kitāb al-Ghayba al-Ṭūsī "
  return book_dict
    
    
  


def choices(book, num):
  try:
    response = requests.get(f"https://www.thaqalayn-api.net/api/{book}/{num}")
    hadith = response.json()
  
    if hadith[0]["author"] == "Shaykh Muḥammad Āṣif al-Muḥsinī":
      hadith[0]["majlisiGrading"] = hadith[0]["mohseniGrading"]
  
    majlisi = hadith[0]["majlisiGrading"].split()
    grading = []
      
    for i in majlisi:
      if "م" in i or "ي" in i or "ح" in i or "ع" in i or "ا" in i or "ل" in i or "ق" in i:
        grading.append(i)
    grading = " ".join(grading)
  
      
      
    return {
        "arabic": hadith[0]["arabicText"],
        "english": hadith[0]["englishText"],
        "author": hadith[0]["author"],
        "book": hadith[0]["book"],
        "URL": hadith[0]["URL"],
        "chapter": hadith[0]["chapter"],
        "grading": grading,
        "id": hadith[0]["id"]
      }
  except:
    return 0

def get_hadith(search):
  try:
    link = ""
    response = requests.get(f"https://www.thaqalayn-api.net/api/query?q={search}")
    hadith = response.json()
    if len(hadith) > 1:
      more = True
      link = f"https://thaqalayn.net/customsearch?book_id=all&query={search}&exactPhrase=true"
    else:
      more = False
    if hadith[0]["author"] == "Shaykh Muḥammad Āṣif al-Muḥsinī":
      hadith[0]["majlisiGrading"] = hadith[0]["mohseniGrading"]

    majlisi = hadith[0]["majlisiGrading"].split()
    grading = []
    
    for i in majlisi:
      if "م" in i or "ي" in i or "ح" in i or "ع" in i or "ا" in i or "ل" in i or "ق" in i:
        grading.append(i)
    grading = " ".join(grading)

    
    return {
        "arabic": hadith[0]["arabicText"],
        "english": hadith[0]["englishText"],
        "author": hadith[0]["author"],
        "book": hadith[0]["book"],
        "URL": hadith[0]["URL"],
        "chapter": hadith[0]["chapter"],
        "grading": grading,
        "id": hadith[0]["id"],
        "more": more,
        "link": link
    }
  except:
    return 0

def send(hadith):
    author = ""
    aut = hadith["author"].split()
    for i in aut:
      if 'al-Kulaynī' in i:
        author = "al Kulaynī"
      if "al-Mufīd" in i:
        author = "al Mufīd"
      if "al-Ṣaduq" in i:
        author = "al Ṣaduq"
      if "al-Nuʿmānī" in i:
        author = "al Nuʿmānī"
      if "al-Ṭūsī" in i:
        author = "al Ṭūsī"
      if "al-Ahwāzī" in i:
        author = "al-Ahwāzī"
      if "al-Qummī" in i:
        author = "Jaʿfar b. Muḥammad al Qummī"
      if "al-Muḥsinī" in i:
        author = "al Muḥsinī"
      if "al-Ghaḍā'irī" in i:
        author = "al Ghaḍā'irī"
      book = hadith['book']
      if "Al-Kāfi" in book:
        book = "al-Kāfi"
      if "akhbār" in book:
        book = "ʿUyūn akhbār al-Riḍā"
      if "Tawḥīd" in book:
        book = "al-Tawḥīd"
      if "Khiṣāl" in book:
        book = "al-Khiṣāl"
      if "Amālī" in book:
        book = "al-Amālī"
      book = book.replace('-', ' ')
    english = hadith["english"]
    english = hadith["english"].replace("(a.s.)", "(ع)")
    english = english.replace("(a.s.)", "(ع)")
    english = english.replace("(MGB)", "(ع)")
    english = english.replace("(AS)", "(ع)")
    english = english.replace("(SA)", "(ص)")
    english = english.replace("‘Alayhi al-Salam", "(ع)")
  
    embed = discord.Embed(title = hadith["chapter"], description = english, color = 0x4034eb)
    embed.set_author(name= f"{book} - {author}", icon_url="https://i.ibb.co/XZnVbG4/thaq-1.png")
    embed.add_field(name="Grading: ", value = hadith["grading"], inline=True)
    embed.add_field(name="Source: ", value= f"[{hadith['book']}: {hadith['id']}]({hadith['URL']})", inline=True)
    return embed



def asend(hadith):
    author = ""
    aut = hadith["author"].split()
    for i in aut:
      if 'al-Kulaynī' in i:
        author = "al Kulaynī"
      if "al-Mufīd" in i:
        author = "al Mufīd"
      if "al-Ṣaduq" in i:
        author = "al Ṣaduq"
      if "al-Nuʿmānī" in i:
        author = "al Nuʿmānī"
      if "al-Ṭūsī" in i:
        author = "al Ṭūsī"
      if "al-Ahwāzī" in i:
        author = "al-Ahwāzī"
      if "al-Qummī" in i:
        author = "Jaʿfar b. Muḥammad al Qummī"
      if "al-Muḥsinī" in i:
        author = "al Muḥsinī"
      if "al-Ghaḍā'irī" in i:
        author = "al Ghaḍā'irī"

        
      book = hadith['book']
      if "Al-Kāfi" in book:
        book = "al-Kāfi"
      if "akhbār" in book:
        book = "ʿUyūn akhbār al-Riḍā"
      if "Tawḥīd" in book:
        book = "al-Tawḥīd"
      if "Khiṣāl" in book:
        book = "al-Khiṣāl"
      if "Amālī" in book:
        book = "al-Amālī"
      book = book.replace('-', ' ')
        
    embed = discord.Embed(title = "باب", description = hadith["arabic"], color = 0x4034eb)
    embed.set_author(name= f"{book} - {author}", icon_url="https://i.ibb.co/XZnVbG4/thaq-1.png")
    embed.add_field(name="إسناد: ", value = hadith["grading"], inline=True)
    embed.add_field(name="كتاب: ", value= f"[{hadith['book']}: {hadith['id']}]({hadith['URL']})", inline=True)
    return embed


def randomh():
  response = requests.get("https://www.thaqalayn-api.net/api/random")
  hadith = response.json()


  if hadith["author"] == "Shaykh Muḥammad Āṣif al-Muḥsinī":
    hadith["majlisiGrading"] = hadith["mohseniGrading"]

  majlisi = hadith["majlisiGrading"].split()
  grading = []
    
  for i in majlisi:
    if "م" in i or "ي" in i or "ح" in i or "ع" in i or "ا" in i or "ل" in i or "ق" in i:
      grading.append(i)
  grading = " ".join(grading)

    
    
  return {
      "arabic": hadith["arabicText"],
      "english": hadith["englishText"],
      "author": hadith["author"],
      "book": hadith["book"],
      "URL": hadith["URL"],
      "chapter": hadith["chapter"],
      "grading": grading,
      "id": hadith["id"]
    }



def linked(link):
  try:
    link = link
    ls = link.split("/")
    for i in ls:
      if i.isdigit():
        booknum = i
        break
        
    
    URL = f"https://thaqalayn.net/book/{booknum}"

    r = requests.get(URL)
        
    soup = BeautifulSoup(r.content, "html.parser")
        
    book = soup.find("h1").get_text()

    response = requests.get("https://www.thaqalayn-api.net/api/allbooks")
    list_of_books = response.json()
    for i in range(len(list_of_books)):
      if list_of_books[i]["BookName"] == book:
        book = list_of_books[i]["bookId"]
        break

        
    response = requests.get(f"https://www.thaqalayn-api.net/api/{book}")
    book_cont = response.json()
    for i in range(len(book_cont)):
      if book_cont[i]["URL"] == link:
        id = book_cont[i]["id"]
        break

    response = requests.get(f"https://www.thaqalayn-api.net/api/{book}/{id}")
    hadith = response.json()
  
    if hadith[0]["author"] == "Shaykh Muḥammad Āṣif al-Muḥsinī":
      hadith[0]["majlisiGrading"] = hadith[0]["mohseniGrading"]
  
    majlisi = hadith[0]["majlisiGrading"].split()
    grading = []
      
    for i in majlisi:
      if "م" in i or "ي" in i or "ح" in i or "ع" in i or "ا" in i or "ل" in i or "ق" in i:
        grading.append(i)
    grading = " ".join(grading)
  
      
      
    return {
        "arabic": hadith[0]["arabicText"],
        "english": hadith[0]["englishText"],
        "author": hadith[0]["author"],
        "book": hadith[0]["book"],
        "URL": hadith[0]["URL"],
        "chapter": hadith[0]["chapter"],
        "grading": grading,
        "id": hadith[0]["id"]
      }
        
    
  except:
    return 0

#
def dict_choice(dictionary: dict):
  books = []
  for key in list(dictionary.keys())[0:40 - 1]:
    books.append(Choice(name=dictionary[key], value=key))
  return books


def search_book(search, book):
  try:
    link = ""
    response = requests.get(f"https://www.thaqalayn-api.net/api/query/{book}?q={search}")
    hadith = response.json()
    if len(hadith) > 1:
      more = True
      link = f"https://thaqalayn.net/customsearch?book_id={book}&query{search}&exactPhrase=true"
    else:
      more = False
    if hadith[0]["author"] == "Shaykh Muḥammad Āṣif al-Muḥsinī":
      hadith[0]["majlisiGrading"] = hadith[0]["mohseniGrading"]

    majlisi = hadith[0]["majlisiGrading"].split()
    grading = []
    
    for i in majlisi:
      if "م" in i or "ي" in i or "ح" in i or "ع" in i or "ا" in i or "ل" in i or "ق" in i:
        grading.append(i)
    grading = " ".join(grading)

    
    return {
        "arabic": hadith[0]["arabicText"],
        "english": hadith[0]["englishText"],
        "author": hadith[0]["author"],
        "book": hadith[0]["book"],
        "URL": hadith[0]["URL"],
        "chapter": hadith[0]["chapter"],
        "grading": grading,
        "id": hadith[0]["id"],
        "more": more,
        "link": link
    }
  except:
    return 0
