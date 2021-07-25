#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from pywikibot import ( ItemPage, pagegenerators )

FAG_ID = 'P535'
FAG_NAME = 'findagrave'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, 'Find a Grave template with ID not in Wikidata')
    repo = site.data_repository()
    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot $|Adding Find A Grave ID]])'
    args = {'summary': summary, 'check_value': False, 'add_ref': True}
    count = 0

    for page in pages:
        title = page.title()

        try:
            item = ItemPage.fromPage(page)
        except:
            print('Skipping %s, because no data item found.' %title)
            continue

        if FAG_ID in item.get()['claims']:
            print('Claim already exists for %s... skipping now.' %title)
            continue

        count += processPage(page, item, summary)

        if count == limit:
            break

    print('Finished. Updated %s items' %count)

def processPage(page, item, summary):
    def getRelevantVal(templates):
        arguments = None

        while templates:
            # Start from the last templates because the template
            # we care about here is typically found at the end or
            # near the end of a page
            template, arguments = templates.pop()
            # normalize title for comparison
            title = template.title(with_ns=False).lower().replace(' ', '')

            if title == FAG_NAME:
                break

        return arguments

    print('Processing %s' %page.title())

    templates = page.templatesWithParams()
    args = getRelevantVal(templates)

    if args and args != []:
        value = args[0].strip()

        if re.match(r'^[0-9]*$', value):
            common.addSingleClaim(
                item, FAG_ID, value,
                summary=summary, check_value=False, add_ref=True)

            return 1

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        main(limit)
