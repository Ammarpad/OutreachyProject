#!/usr/local/bin/python3

import re
import requests

import pywikibot
from bs4 import BeautifulSoup
from __local__ import credentials
from pywikibot import pagegenerators
import outreachyscript as main_script
import base_import_script as import_script

TWITTER_ID_PROP = 'P6552' 
TWITTER_USERNAME_PROP = 'P2002'
SESSION = requests.Session()

def do_import():
    cat = 'Twitter username not in Wikidata'
    en_wiki = pywikibot.Site('en', 'wikipedia')
    repo = en_wiki.data_repository()
    catObj = pywikibot.Category(en_wiki, cat)
    data = no_data_item = list()
   
    pages = pagegenerators.CategorizedPageGenerator(catObj, recurse=False)
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print("Skipping {}, no data item found", page.title())
            no_data_item.append(page.title())
            continue

        username = extract_username(page)

        if username:
            data.append([username, data_item])
            print("Found %s for %s:" %(username, page.title()))
        else:
            print("Cannot extract Twitter username for %s. Either there's none or there "
                + "are multiple and it's unclear which one is official" % page.title())

    if len(no_data_item):
        import_script.record_pages_without_items(no_data, 'missing-data-items-list-twitter')

    result = import_script.add_claims_to_item(repo, data, TWITTER_USERNAME_PROP, summary='')
    
    for u, d in data:
        if d.title() in result['items']:
            num_id = get_numeric_id(u)
            if num_id:
                main_script.add_qualifier(repo, d.title(), TWITTER_ID_PROP, TWITTER_USERNAME_PROP, num_id)

def extract_username(page):
    pass

def get_numeric_ids(usernames):
    params = headers = {}

    params['usernames'] = ','.join(usernames)
    params['user.fields'] = ','.join(['id'])
    headers['Authorization'] = 'Bearer {}'.format(credentials.twitter['bearer_token'])
    url = 'https://api.twitter.com/2/users/by?'

    response = SESSION.get(url, params=params, headers=headers)

    if response.status_code == 200:
        res = response.json()
        if 'data' in res:
            ret = dict()
            for r in res['data']:
                ret[r['id']] = r
            return ret
    else:
       return False

if __name__ == '__main__':
    do_import()