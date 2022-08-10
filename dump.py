import json
from scraper import scraper

class dump:
    # dumps all fighter links into fighter_links.son
    def fighter_links(links):
        with open('links/fighter_links.json', 'w', encoding='utf-8') as f:
            json.dump(scraper.get_fighter_profile_links(), f, ensure_ascii=False, indent=4)

    # dumps all fighter info into fighter_info.json
    def fighter_info(data):
        with open('data/data.json', 'w', encoding='utf-8') as f:
            json.dump(scraper.get_fighter_info(), f, ensure_ascii=False, indent=4)