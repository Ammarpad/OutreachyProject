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
