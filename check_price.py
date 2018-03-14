from bs4 import BeautifulSoup
import time
import json
import requests
from selenium import webdriver
import regex
import pyautogui as gui
import webbrowser
import sys

class KittyFinder():
  def __init__(self, pricelimit):
    self.good_cats = ['Fast', 'Swift', 'Snappy', 'Brisk']
    self.good_limit = 0.024
    self.pricelimit = pricelimit
    self.url = "https://www.cryptokitties.co/marketplace/sale?orderBy=current_price&orderDirection=asc&sorting=cheap"


  def checkPrice(self):
    while True:
      try:
        browser = webdriver.PhantomJS()
        browser.get(self.url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        first_cat = soup.find("div", { "class" : "KittiesGrid" }).find("div", { "class" : "KittiesGrid-item" })

        price = str(first_cat.find("span", { "class" : "KittyStatus-note" }))
        price = regex.search('>(\.|\d)+<', price).group(0)
        price = float(price[1:-1])

        cooldown = str(first_cat.find("div", { "class" : "KittyCard-coldown" }))
        cooldown = regex.search('>(.)+<', cooldown).group(0)
        cooldown = cooldown[1:-1]

        catid = str(first_cat.find("a"))
        catid = regex.search('\/(\d)+"><', catid).group(0)
        catid = catid[1:-3]

        caturl = f"https://www.cryptokitties.co/kitty/{catid}/buy"
        print(price)

        if price < self.good_limit and cooldown in self.good_cats:
          return caturl

        if price < self.pricelimit and cooldown != "Sluggish" and cooldown != "Catatonic":
          return caturl

        delay = 2
        time.sleep(delay)

      except Exception as e:
        print(e)


pricelimit = 0.0003
finder = KittyFinder(pricelimit)
caturl = finder.checkPrice()

webbrowser.get('firefox').open_new_tab(caturl)
# gui.alert(text=f"I founda a kitten for {price} eth", title='Cheap Kitten!', button='OK')


