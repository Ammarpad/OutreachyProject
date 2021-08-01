#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from pywikibot import ( ItemPage, pagegenerators )

CAPACITY_ID = 'P1083'
TEMP_NAME = 'infobox venue'

def main():
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, TEMP_NAME, ns=10)
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot $|Add maximum capacity]])'
    args = {
        'follow_redirects': False,
        'only_template_inclusion': True,
        'namespaces': [0], 'total': limit
    }
    count = 0
    pages = page.getReferences( **args )
    backlinks = page.backlinks(filter_redirects=True)
    redirects = [link.title(with_ns=False).lower() for link in backlinks]


    for page in pages:
        print('Processing %s' %page.title())

        res = processPage(page, redirects, summary)
        if res is True:
            count =+ 1

    print('Processed %s pages in total' %count)

def processPage(page, redirects, summary):
    # Affix the canonical name of the template at the beginning
    # since it will be matched more than the redirects
    temp_titles = redirects[:0] = [TEMP_NAME]

    templates = page.raw_extracted_templates
    # Operate on reversed list to get the infobox template faster
    templates.reverse()
    value = None

    while True:
        temp = templates.pop()
        if temp[0].title().lower() in temp_titles:
            value = temp[1].get('seating_capacity', None)
            break

    if value is not None:
        if not value.isdecimal():
            value = value.replace(',','')
            value = re.match(r'[\d,]+', value)
            if not value:
                return False

        quantity = pywikibot.WbQuantity(value[0], site=common.REPO)
        res = updateRepo(item, quantity, summary):
        return res

    return False


def updateRepo(page, value, summary):
    title = page.title()
    item = common.getDataItem(page)

    if item == None:
        print('Skipping %s, because no data item found.' %title)
        return False

    if CAPACITY_ID in item.get()['claims']:
        print('Claim already exists for %s... skipping now.' %title)
        return False

    args = {'summary':summary, 'check_value':False, 'add_ref':True}
    common.addSingleClaim(item, CAPACITY_ID, value, **args)

    return True

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt
        print('Quitted')
