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
    temp = pywikibot.Page(site, TEMPLATE, ns=10)
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot $|Add maximum capacity]])'
    all_pages = page.getReferences(
        follow_redirects = False,
        only_template_inclusion=False,
        namespaces = [0],
        total = 100
    )
    
    processPages(all_pages)


def processPages(pages):
    def getRedirects(p):
        backlinks = p.backlinks(filter_redirects=True)
        redirects = list()
        
        for link in backlinks:
            redirects.append(link.title(with_ns=False).lower())
        
        return redirects

    redr = getRedirects(templatePage)


    for page in pages:
        pass



def extractMode(page, templatePage):

    


if __name__ == '__main__':
    main()
