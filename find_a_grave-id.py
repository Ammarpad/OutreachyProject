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
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot 5|Adding Find A Grave ID]])'

    count = 0
    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)

    for page in pages:
        title = page.title()

        item = common.getDataItem(page, verbose=True)
        if not item:
            continue

        claims = item.get()['claims']
        if FAG_ID in claims:
            print('Claim already exists for %s... skipping now.' %title)
            continue

        if not common.checkInstance('Q5', claims):
            continue

        res = processPage(page, item, summary)
        count += int(res)

        if limit == -1:
            continue
        elif count == limit:
            break

    print('Finished. Updated %s items' %count)

def processPage(page, item, summary):
    def getRelevantVal(templates):
        arguments = None

        while templates:
            # Start from the last template because the template
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
            
            permalink = page.permalink(with_protocol = True)
            common.addReference(item.title(), FAG_ID, 'P4656', permalink)

            return True

    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Limit is required. -1 means no limit')

    limit = int(sys.argv[1])
    main(limit)
