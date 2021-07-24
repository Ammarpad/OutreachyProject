#!/usr/local/bin/python3

import common
import pywikibot
from pywikibot import pagegenerators

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, 'Find a Grave template with ID not in Wikidata')
    repo = site.data_repository()
    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    count = 0

    for page in pages:
    	title = page.title()

        try:
            item = pywikibot.ItemPage.fromPage(page)
        except:
            print('Skipping %s, because no data item found.' %title)
            continue

        if FAG_ID in item.get()['claims']:
            print('Claim already exists for %s... skipping now.' %title)
            continue

    	count += processPage(page, item)


def processPage(page):
	templates = page.templatesWithParams()
	pass



