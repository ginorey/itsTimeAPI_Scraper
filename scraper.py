# Web Scraping
import requests as r
import json
from bs4 import BeautifulSoup as bs
from objects import Fighter, Event
# Data Manipulation
from collections import OrderedDict


def getFighterProfileLinks():
    i = open('links/links.json')
    directory = json.load(i)
    # initializing list
    temp = []

    # iterate through each site and pull all fighter links
    # directory consist of list of all of the links for fighter names A-Z
    # we will use this loop to iterate through all of the links
    # this will give us the links for each fighter profile
    for link in directory:
        # try to connect to the link
        html = url_reader(link)
        if html == None:
            continue

        # locate all urls
        URLS = html.find_all('td', {'class': 'b-statistics__table-col'})

        # remove duplicate urls
        for link in URLS:
            if(link.find('a')):
                temp.append(link.find('a').get('href'))

    # convert to list
    links = list(OrderedDict.fromkeys(temp))
    # returns links list
    return links

# reads URL for fighterLinkParser
def url_reader(url):
    try:
        page = r.get(url, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}, timeout=10)
    # if request fails:
        # we will print the url to be aware of it
        # we will skip that link and move on
    except r.exceptions.RequestException as i:
        print(f'URL: {url}', i)
        return None
    html = bs(page.content, "html.parser")
    return html

# returns fighterName string
def fighterName(html):
    name = html.find('span', {'class': 'b-content__title-highlight'}).text.strip()
    return name

# returns fighterRecord string
def fighterRecord(html):
    record = (html.find('span', {'class': 'b-content__title-record'})).text.strip()
    return record

# returns fighterNickname string
def fighterNickname(html):
    nickname = html.find('p', {'class': 'b-content__Nickname'}).text.strip()
    return nickname

# returns fighterName string
def fighterDescription(html):
    # removing all whitespaces in the raw html
    # then append to text_only
    # text_only is a list of all fighter information
    temp = html.find_all('li', {'class': 'b-list__box-list-item b-list__box-list-item_type_block'})
    text_only = []
    for info in temp:
        # append to text only
        text_only.append(info.text.strip())
        # thanks to stack over flow
    description = [key_val.split(":")[-1].strip() for key_val in text_only]
    return description

def fightDetails(html):
    fight_details = html.find_all('p', {'class': 'b-fight-details__table-text'})
    fight_details_text = []
    k = open('extra/forbbiden.json')
    forbidden = json.load(k)
    for i in fight_details:
        fight_details_text.append(i.text.strip())
    for i in fight_details_text:
        if i in forbidden:
            fight_details_text.remove(i)
        if i == 'next':
            pointer = fight_details_text.index(i)
            del fight_details_text[pointer:pointer+6]
                
    # Credit to StackOverflow for this Line
    fightDetails = [fight_details_text[i: i+16] for i in range(0, len(fight_details_text), 16)]
    return fightDetails

def fighterObjectMaker(id_counter, name, record, nickname, description, fights):
    fighter = Fighter(id_counter, name, record[8:], nickname, description[0], description[1], description[2], description[3], description[4],
                    description[5], description[6], description[7], description[9], description[10], description[11], description[12], description[13], fights)
    return fighter 

def eventObjectMaker(fightDetails):
    fights = []
    fight_counter = 1
    for fight in fightDetails:
        # make fight object
        fight = Event(fight_counter, fight[0], fight[1], fight[2], fight[3], fight[4], fight[5], fight[6],
                      fight[7], fight[8], fight[9], fight[10], fight[11], fight[12], fight[13], fight[14], fight[15])
        # append to fights list
        fights.append(fight)
        # increase counter by 1 
        fight_counter += 1
    return fights
    
def get_fighter_info():
    # pull up fighter profile links 
    j = open('links/fighter_links.json')
    fighter_links = json.load(j)

    data = {"data" : []} 
    id_counter = 1

    # iterate over fighter profile links
    for link in fighter_links:

        # collect and read html
        html = url_reader(link)
        if html == None:
            continue
        
        # collect data
        name         = fighterName(html)
        record       = fighterRecord(html)
        nickname     = fighterNickname(html)
        description  = fighterDescription(html)
        fightDetail  = fightDetails(html)

        # make objects
        fights = eventObjectMaker(fightDetail)
        fighter = fighterObjectMaker(id_counter, name, record, nickname, description, fights)
        data['data'].append(fighter)
        id_counter += 1
    
    return data 
