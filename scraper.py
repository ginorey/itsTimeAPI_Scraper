# Web Scraping
import requests as r
import json
from bs4 import BeautifulSoup as bs
# Data Manipulation
from collections import OrderedDict

i = open('links/links.json')
j = open('links/fighter_links.json')
k = open('extra/forbbiden.json')
l = open('extra/extra.json')
extra = json.load(l)
forbidden = json.load(k)
directory = json.load(i)
fighter_links = json.load(j)

class scraper:
        # get fighter profile links
        def fighter_links():
            # initializing list
            temp = []

            # iterate through each site and pull all fighter links
            for link in directory:
                # try to connect to site
                try:
                    page = r.get(link,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}, timeout=10)
                # if request fails, print URL and continue
                except r.exceptions.RequestException as i:
                    print(f'URL: {link}', i)
                    continue
                # read html
                s = bs(page.content, "html.parser")
                # locate all urls
                URLS = s.find_all('td', {'class': 'b-statistics__table-col'})

                # remove duplicate urls
                for link in URLS:
                    if(link.find('a')):
                        temp.append(link.find('a').get('href'))

            # convert to list
            links = list(OrderedDict.fromkeys(temp))
            # returns links list
            return links

        # gets all fighter info
        def fighters_info():
            # opening json file for links
            # getting and reading urls in links
            data = {"data" : []}
            id_counter = 1
            for url in fighter_links:

                # try to site html and read it
                try:
                    page = r.get(url, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}, timeout=10)
                # if request fails, print URL and continue
                except r.exceptions.RequestException as i:
                    print(f'URL: {url}', i)    
                    continue
                # read html
                s = bs(page.content, "html.parser") 

                # find all fighter info
                NAME = s.find('span', {'class': 'b-content__title-highlight'})
                RECORD = (s.find('span', {'class': 'b-content__title-record'})).text.strip()
                NICKNAME = s.find('p', {'class': 'b-content__Nickname'})
                DESCRIPTION = s.find_all('li', {'class': 'b-list__box-list-item b-list__box-list-item_type_block'})
                FIGHT_DETAILS = s.find_all('p', {'class': 'b-fight-details__table-text'})

                # dictionary format
                format = {'ID': id_counter, 
                                            'name': None, 
                                          'record': None, 
                                        'nickname': None, 
                                          'height': None,
                                          'weight': None,
                                           'reach': None,
                                          'stance': None,
                                  'date of birth' : None, 
           'significant strikes landed per minute': None,
                   'significant striking accuracy': None,
         'significant strikes absorbed per minute': None,
                      'significant strike defence': None,
        'average takedowns landed per 15 minutes' : None,
                              'takedown accuracy' : None,
                               'takedown defense' : None,
   'average submissions attempted per 15 minutes' : None,
                                         'fights' : []
                }

                # remove all white spaces and format
                text_only = []
                for info in DESCRIPTION:
                    # append to RAW, text only
                    text_only.append(info.text.strip())
                temp = [key_val.split(":")[-1].strip() for key_val in text_only]

                # append each fighter info to format
                format['name']= NAME.text.strip()
                format['record'] = RECORD[8:]
                format['nickname'] = NICKNAME.text.strip()
                format['height'] = temp[0]
                format['weight'] = temp[1]
                format['reach'] = temp[2]
                format['stance'] = temp[3]
                format['date of birth'] = temp[4]
                format['significant strikes landed per minute'] = temp[5]
                format['significant striking accuracy'] = temp[6]
                format['significant strikes absorbed per minute'] = temp[7]
                format['significant strike defence'] = temp[9]
                format['average takedowns landed per 15 minutes'] = temp[10]
                format['takedown accuracy'] = temp[11]
                format['takedown defense'] = temp[12]
                format['average submissions attempted per 15 minutes'] = temp[13]

                # add to id counter
                id_counter += 1

                

            ##### ORGANIZING EACH FIGHT ######

                # Organizes all Info to List
                fight_details_text = []
                for i in FIGHT_DETAILS:
                    fight_details_text.append(i.text.strip())
                for i in fight_details_text:
                    if i in forbidden:
                        fight_details_text.remove(i)
                    if i == 'next':
                        pointer = fight_details_text.index(i)
                        del fight_details_text[pointer:pointer+6]
                # Converts List to List of Lists                
                list_of_fights = [fight_details_text[i: i+16] for i in range(0, len(fight_details_text), 16)]
                if len(list_of_fights) == 0:
                    format['fights'] = None
                    continue
                
                # dictionary fight_formatting
                fight_counter = 1
                for fight in list_of_fights:
                    fight_format = {    'ID' : fight_counter,
                                              'win/loss': None, 
                                             'fighter 1': None, 
                                             'fighter 2': None, 
                                          'fighter 1 KD': None,
                                          'fighter 2 KD': None,
                                         'fighter 1 STR': None,
                                         'fighter 2 STR': None,
                                         'fighter 1 TD' : None,
                                          'fighter 2 TD': None,
                                         'fighter 1 SUB': None,
                                         'fighter 2 SUB': None,
                                                 'event': None,
                                                  'date': None,
                                                'method': None,
                                                 'round': None,
                                                  'time': None,
                }

                    fight_format['win/loss'] = fight[0]
                    fight_format['fighter 1'] = fight[1]
                    fight_format['fighter 2'] = fight[2]
                    fight_format['fighter 1 KD'] = fight[3]
                    fight_format['fighter 2 KD'] = fight[4]
                    fight_format['fighter 1 STR'] = fight[5]
                    fight_format['fighter 2 STR'] = fight[6]
                    fight_format['fighter 1 TD'] = fight[7]
                    fight_format['fighter 2 TD'] = fight[8]
                    fight_format['fighter 1 SUB'] = fight[9]
                    fight_format['fighter 2 SUB'] = fight[10]
                    fight_format['event'] = fight[11]
                    fight_format['date'] = fight[12]
                    fight_format['method'] = fight[13]
                    fight_format['round'] = fight[14]
                    fight_format['time'] = fight[14]
                    format['fights'].append(fight_format)
                    fight_counter += 1

                data["data"].append(format)
                    
            # return data
            return data
