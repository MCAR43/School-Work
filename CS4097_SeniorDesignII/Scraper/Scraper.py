#!/usr/bin/env python3
from selenium import webdriver
from pyautogui import press, click
import time
import os
URL = "https://sf.vods.co/ultimate/character/"
CHARACTERS = [
    "Bowser",
    "Bowser Jr.",
    "Captain Falcon",
    "Chrom",
    "Cloud",
    "Corrin",
    "Daisy",
    "Dark Pit",
    "Dark Samus",
    "Diddy Kong",
    "Donkey Kong",
    "Dr. Mario",
    "Duck Hunt",
    "Falco",
    "Fox",
    "Ganondorf",
    "Greninja",
    "Hero",
    "Ice Climbers",
    "Ike",
    "Incineroar",
    "Inkling",
    "Isabelle",
    "Jigglypuff",
    "Joker",
    "Ken",
    "King Dedede",
    "King K. Rool",
    "Kirby",
    "Link",
    "Little Mac",
    "Lucario",
    "Lucas",
    "Lucina",
    "Luigi",
    "Mario",
    "Marth",
    "Mega Man",
    "Meta Knight",
    "Mewtwo",
    "Ness",
    "Olimar",
    "Pac-Man",
    "Palutena",
    "Peach",
    "Pichu",
    "Pikachu",
    "Pirahna Plant",
    "Pit",
    "Pkemon Trainer",
    #"Rob",
    "Richter",
    "Ridley",
    "Robin",
    #"Rosalina",
    "Roy",
    "Ryu",
    "Samus",
    "Sheik",
    "Shulk",
    "Simon",
    "Snake",
    "Sonic",
    "Toon Link",
    "Villager",
    "Wario",
    "Wolf",
    "Yoshi",
    "Young Link",
    "Zelda",
    "Zero Suit Samus"
]

class VideoLink:
    def __init__(self, charA, charB):
        self.charA = charA
        self.charB = charB
        self.links = []
    
    def addLink(self, link):
        self.links.append(link)

    def getLinks(self):
        return self.links

    def display(self):
        print("%s vs %s:" % (self.charA, self.charB))
        for link in self.links:
            print(link, sep=", ", end="")

#Fill this out
def getScrotFromVideo(browser, videoLinks):
    newDir = "img/" + videoLinks.charA + videoLinks.charB
    os.mkdir(newDir)
    for vidNum, link in enumerate(videoLinks.getLinks()[0:2]):
        browser.get(link)
        youtubeExt = browser.find_element_by_xpath('//*[@id="g1"]').get_attribute('data-vod')
        browser.get('https://www.youtube.com/watch_popup?v=' + youtubeExt[:-1])
        click()
        press('f')
        time.sleep(1)
        for i in range(5):
            for k in range(10):
                press('l')

            time.sleep(0.5)
            browser.save_screenshot(newDir + "/" + videoLinks.charA + videoLinks.charB + str(vidNum) + str(i) + ".png")

def getVideoLinks(browser, charA, charB):
    temp = VideoLink(charA, charB)
    browser.get(URL + charA + "/character2/" + charB)
    vodTableList = browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[1]/div/section/div/div/div/div')
    for tR in vodTableList.find_elements_by_css_selector('tr'):
        linkElement = tR.find_elements_by_css_selector('td')[2]
        smashVodsLink = linkElement.find_element_by_css_selector('a').get_attribute('href')
        print("%s vs %s --> %s" % (charA, charB, smashVodsLink))
        temp.addLink(smashVodsLink)

    return temp

def main():
    #folder clean-up
    if os.path.exists('img/'):
        os.system('rm -r img/')
    os.mkdir('img/')
    
    browser = webdriver.Chrome()
    relevantLinks = []
    for charA in CHARACTERS[10:15]:
        for charB in CHARACTERS[15:20]:
            relevantLinks = getVideoLinks(browser, charA, charB)
            relevantLinks.display()
            getScrotFromVideo(browser, relevantLinks)

    browser.quit()

if __name__ == "__main__":
    main()
