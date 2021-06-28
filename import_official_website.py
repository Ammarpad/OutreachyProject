#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from bs4 import BeautifulSoup
from pywikibot import pagegenerators


OFFICIAL_WEBSITE_ID = 'P856'
URL_REGEX = r'https?://[^\s<>"]+|www\.[^\s<>"]+'

def doImport(limit):
    cat = 'Official_website_not_in_Wikidata'
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, cat)
    data = list()
    no_data_item = list()

    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    found = 0
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print('Skipping %s, no data item found' % page.title())
            no_data_item.append(page.title())
            continue

        website = extractWeblink(page)

        if website:
            data.append([website, data_item])
            found += 1
            print('Found %s for %s:' %(website, page.title()))
        else:
            print('Failed for %s' %page.title())

        if found == limit:
            break

    if len(no_data_item):
        common.recordPages(no_data_item, 'missing-data-items-list')

    result = common.addMultipleClaims(data, OFFICIAL_WEBSITE_ID, check_value=False)

    print('Finished. Updated %s items, %s were skipped' %(result['added'], result['skipped']))

def extractWeblink(page):
    page_source = page.expand_text(True)
    html = BeautifulSoup(page_source, features='html.parser')
    items = html.findAll('span', {'class':'url', 'class':'official-website'})

    if not items or len(items) != 1:
        return None

    return re.findall(URL_REGEX, str(items))[0]

if __name__ == '__main__':
    limit = int(sys.argv[1])
    doImport(limit)
