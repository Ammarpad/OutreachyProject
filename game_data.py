#!/usr/local/bin/python3

import common
import pywikibot
import wikitextparser as parser
from pywikibot import pagegenerators

GAME_MODE_PROP_ID = 'P404'
TEMPLATE = 'Infobox video game'

def main():
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, TEMPLATE, ns=10)
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot $|Add maximum capacity]])'
    all_pages = page.getReferences(
        follow_redirects = False,
        only_template_inclusion=False,
        namespaces = [0],
        total = 100
    )
    backlinks = page.backlinks(filter_redirects=True)
    redirects = [link.title(with_ns=False).lower() for link in backlinks]



def extractMode(page):
    pass


if __name__ == '__main__':
    main()
