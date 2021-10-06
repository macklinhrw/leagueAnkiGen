import time

from bs4 import BeautifulSoup
from selenium import webdriver
import os
import requests

BASE_LINK = "https://www.mobafire.com"
ABILITY_LINK = "https://www.mobafire.com/league-of-legends/abilities"
CHAMPION_LINK = "https://www.mobafire.com/league-of-legends/champions"
FILE_NAME = "abilities.txt"
ANKI_COLLECTION_PATH = "C:\\Users\\Macklinrw\\AppData\\Roaming\\Anki2\\User 1\\collection.media\\"
CHROMEDRIVER_PATH = 'C:/Users/Macklinrw/Desktop/chromedriver'


class Ability:
    def __init__(self, champion, key, title, description, cooldown, cost, spell_range, img):
        self.champion = champion
        self.key = key
        self.title = title
        self.description = description
        self.cooldown = cooldown
        self.cost = cost
        self.spell_range = spell_range
        self.img = img


def main():
    browser = webdriver.Chrome(CHROMEDRIVER_PATH)
    browser.get(CHAMPION_LINK)

    champions_by_pick = []

    browser.find_element_by_xpath("//label[@for='st-pick']").click()
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for item in soup.find_all("div", {'class': 'champ-list__item__name'}):
        champion = str(item.contents[1]).replace("<b>", "").replace("</b>", "").replace("&amp;", "&")
        champions_by_pick.append(champion)

    browser.get(ABILITY_LINK)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    ability_links = []
    abilities = []

    for link in soup.find_all("a", {"class": "ability-list__item"}):
        ability_links.append(link["href"])

    for i in range(0, len(ability_links)):
        # progress indicator
        print(i+1, "/", len(ability_links), "...")

        link = ability_links[i]
        html = browser.get(BASE_LINK + link)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        headers = soup.find("h2", {'id': 'view-title'})
        title = headers.contents[0].strip()
        champion = headers.contents[1].text.strip()

        cost = ""
        cooldown = ""
        spell_range = ""

        spell_info = soup.find("div", {'class': 'spell-info'})
        for info in spell_info.find_all("div"):
            info_title = info.contents[0].strip()
            if "Range" in info_title:
                for span in info.find_all("span"):
                    spell_range = spell_range + " " + span.text
            elif "Cooldown" in info_title:
                for span in info.find_all("span"):
                    cooldown = cooldown + " " + span.text
            elif "Cost" in info_title:
                for span in info.find_all("span"):
                    cost = cost + " " + span.text

        cost = cost.strip()
        cooldown = cooldown.strip()
        spell_range = spell_range.strip()

        ability_info = soup.find("div", {'class': 'ability-info'})

        # description = ability_info.contents[2].strip() + " " + ability_info.contents[6].strip()
        description = ""
        for i, child in enumerate(ability_info.children):
            if i < 2:
                continue
            if ";" in child or "\"" in str(child):
                continue
            description = description + " " + str(child).strip()

        key_info = soup.find("div", {'class': 'ability-key'})
        key = key_info.text

        # download image here
        img_ability_title = "-".join(title.replace("/", "").replace(":", "").split())
        img_name = champion + "-" + key + "-" + img_ability_title + ".png"
        img_link = soup.find("div", {'id': 'view-ability__left'}).img['src']
        if not os.path.exists(ANKI_COLLECTION_PATH + img_name):
            print("Downloading <" + img_name + "> ...")
            img_req = requests.get(BASE_LINK + img_link)
            with open(ANKI_COLLECTION_PATH + img_name, 'wb') as f:
                f.write(img_req.content)

        img = "<img src=\"\"{}\"\">".format(img_name)

        ability = Ability(champion, key, title, description, cooldown, cost, spell_range, img)
        abilities.append(ability)
        # print(ability.champion, ability.key, ability.title, "\n" + ability.description, ability.cooldown,
        #   ability.cost, ability.spell_range, ability.img)
    abilities.sort(key=lambda sort_ability: champions_by_pick.index(sort_ability.champion))

    card_front = []
    card_back = []
    card_tag = []

    br = "<br>"

    for ability in abilities:
        pick_index = str(champions_by_pick.index(ability.champion))
        champion_coded = "-".join(ability.champion.split())

        # champion ability question
        card_front.append("What does " + ability.champion + "'s " + ability.key + " (" + ability.title + ") do?")
        card_back.append(ability.img + br + ability.description)
        card_tag.append(champion_coded + " " + pick_index + " ability")

        # passives have no cd, cost and range
        if "Passive" in ability.key:
            continue

        # ability cooldown question
        card_front.append(ability.img + br + "What is the cooldown on " + ability.champion + "'s " + ability.key +
                          " (" + ability.title + ")?")
        if len(ability.cooldown) != 0:
            card_back.append(ability.cooldown)
        else:
            card_back.append("No cooldown or conditional activation.")
        card_tag.append(champion_coded + " " + pick_index + " cooldown")

        # ability cast range and cost question

    with open(FILE_NAME, 'w', encoding='utf8') as f:
        for i in range(len(card_front)):
            f.write("\"{}\";\"{}\";\"{}\"\n".format(card_front[i], card_back[i], card_tag[i]))


if __name__ == '__main__':
    main()
