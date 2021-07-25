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
    repo = site.data_repository()
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
            if isInUse(website, repo):
                continue
            data.append([website, data_item])
            found += 1
            print('Found %s for %s (%s):' %(website, page.title(), data_item.title()))
        else:
            print('Failed for %s' %page.title())

        if found == limit:
            break

    common.recordPages(no_data_item, 'missing-data-items-list')
    result = common.addMultipleClaims(data, OFFICIAL_WEBSITE_ID, check_value=False)

    print('Finished. Updated %s items, %s were skipped' %(result['added'], result['skipped']))

def isInUse(link, site):
    query = 'SELECT ?item WHERE '\
        '{ ?item wdt:' +str(OFFICIAL_WEBSITE_ID)+ ' ?id' \
        ' FILTER ($id = <' + link + '>) . } LIMIT 1'
    res = pagegenerators.WikidataSPARQLPageGenerator(query, site=site)

    return next(res, None) is not None

def extractWeblink(page):
    page_source = page.expand_text(True)
    html = BeautifulSoup(page_source, features='html.parser')
    items = html.findAll('span', {'class':'url', 'class':'official-website'})

    if not items or len(items) != 1:
        return None

    return re.findall(URL_REGEX, str(items))[0].rstrip('/')

if __name__ == '__main__':
    limit = int(sys.argv[1])
    doImport(limit)
