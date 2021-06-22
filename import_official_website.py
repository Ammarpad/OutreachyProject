#!/usr/local/bin/python3

import re

import pywikibot
from bs4 import BeautifulSoup
from pywikibot import pagegenerators
import base_import_script as import_script

OFFICIAL_WEBSITE_PROPERTY = 'P856'
URL_REGEX = r'https?://[^\s<>"]+|www\.[^\s<>"]+'

def do_import():
    cat = 'Official_website_not_in_Wikidata'
    en_wiki = pywikibot.Site('en', 'wikipedia')
    repo = en_wiki.data_repository()
    catObj = pywikibot.Category(en_wiki, cat)
    data = no_data_item = list()

    pages = pagegenerators.CategorizedPageGenerator(catObj, recurse=False)
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print("Skipping %s, no data item found" % page.title())
            no_data_item.append(page.title())
            continue

        website = extract_weblink(page)

        if website:
            data.append([website, data_item])
            print("Found %s for %s:" %(website, page.title()))
        else:
            print("Failed for %s" %page.title())

    if len(no_data_item):
        import_script.record_pages_without_items(no_data, 'missing-data-items-list')

    result = import_script.add_claims_to_item(repo, data, OFFICIAL_WEBSITE_PROPERTY, summary='')

    print("Finished. Updated %s items, %s were skipped" %(result['added'], result['skipped']))

def extract_weblink(page):
    page_source = page.expand_text(True)
    html = BeautifulSoup(page_source, features='html.parser')
    items = html.findAll('span', {'class':'url', 'class':'official-website'})

    if not items or len(items) != 1:
        return None

    return re.findall(URL_REGEX, str(items))[0]

if __name__ == '__main__':
    do_import()
