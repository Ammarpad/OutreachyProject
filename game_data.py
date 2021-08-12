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
    all_pages = temp.getReferences(
        follow_redirects = False,
        only_template_inclusion=False,
        namespaces = [0],
        total = 100
    )
    
    processPages(all_pages, temp)


def processPages(pages, temp):
    def getRedirects(p):
        backlinks = p.backlinks(filter_redirects=True)
        redirects = list()
        
        for link in backlinks:
            redirects.append(link.title(with_ns=False).lower())
        
        return redirects

    redirects = getRedirects(temp)


    for page in pages:
        extractMode(page, redirects)



def extractMode(page, redirects):
    templates = page.raw_extracted_templates
    for (template, values) in templates:
        if template.title() == TEMPLATE or template.title() in redirects:
            print(values.get('game_mode'))

if __name__ == '__main__':
    main()
