#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from pywikibot import ( ItemPage, pagegenerators )

CAPACITY_ID = 'P1083'
TEMP_NAME = 'infobox venue'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, TEMP_NAME, ns=10)
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot 6|Add maximum capacity]])'
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

        if processPage(page, redirects, summary):
            count =+ 1

    print('Updated %s items in total' %count)

def processPage(page, redirects, summary):
    # Affix the canonical name of the template at the beginning
    # since it will be matched more than the redirects
    temp_titles = redirects[:0] = [TEMP_NAME]

    templates = page.raw_extracted_templates
    # Operate on reversed list to get the infobox template faster
    templates.reverse()
    value = None

    while templates:
        temp = templates.pop()
        if temp[0].title().lower() in temp_titles:
            value = temp[1].get('seating_capacity', None) \
                or temp[1].get('capacity', None)
            break

    if value is not None:
        if not value.isdecimal():
            # Strip reference elements from the value.
            tval = value.split('<', 1)[0]

            if tval == value:
                value = value.replace(',','')
            else:
                value = tval.replace(',','')

            if not value:
                return False

        quantity = pywikibot.WbQuantity(value, site=common.REPO)
        res = updateRepo(page, quantity, summary)
        return res

    return False


def updateRepo(page, value, summary):
    title = page.title()
    item = common.getDataItem(page, verbose=True)

    if item == None:
        return False

    if CAPACITY_ID in item.get()['claims']:
        print('Claim already exists for %s... skipping now.' %title)
        return False

    args = {'summary':summary, 'check_value':False, 'add_ref':True}
    common.addSingleClaim(item, CAPACITY_ID, value, **args)

    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Limit is required')

    try:
        limit = int(sys.argv[1])
        main(limit)
    except KeyboardInterrupt:
        print('Quitted')
