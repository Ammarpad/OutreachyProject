#!/usr/local/bin/python3

import re
import common
import pywikibot
from pywikibot import pagegenerators

LEPINDEX_ID = 'P3064'

def main():
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, 'LepIndex ID not in Wikidata')
    repo = site.data_repository()
    count = 0

    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print('Skipping %s, no data item found' % page.title())
            continue

        templates = page.raw_extracted_templates
        lepId = None
        for t in templates:
            if t[0].lower() == 'lepindex':
                for key, value in t[1].items():
                    if key.lower() == 'id':
                        lepId = str(value)

        common.addSingleClaim(data_item, LEPINDEX_ID, lepId, check_value=False, add_ref=True)
        count += 1

    print('Finished. Updated %s items' %count)

if __name__ == '__main__':
    main()
