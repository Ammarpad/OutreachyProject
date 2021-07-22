#!/usr/local/bin/python3

import re, sys
import common
import pywikibot
from pywikibot import pagegenerators

LEPINDEX_ID = 'P3064'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, 'LepIndex ID not in Wikidata')
    repo = site.data_repository()
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot 3|Adding LepIndex ID]])'
    args = {'summary': summary, 'check_value': False, 'add_ref': True}
    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    count = 0

    for page in pages:
        title = page.title()

        try:
            item = pywikibot.ItemPage.fromPage(page)
        except:
            print('Skipping %s, because no data item found.' %title)
            continue

        if LEPINDEX_ID in item.get()['claims']:
            print('Claim already exists for %s... skipping now.' %title)
            continue

        templates = page.raw_extracted_templates
        lepId = None

        for t in templates:
            if t[0].lower() == 'lepindex':
                for key, value in t[1].items():
                    if key.lower() == 'id':
                        if value.isdecimal():
                            lepId = str(value)
                            break
        if lepId:
            common.addSingleClaim(item, LEPINDEX_ID, lepId, **args)
            print('Updated %s. [ID: %s]' % (item.title(), lepId))
            count += 1

        if limit == count:
            break

    print('Finished. Updated %s items' %count)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Limit is required')

    main(int(sys.argv[1]))
