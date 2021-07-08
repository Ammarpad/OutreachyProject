#!/usr/local/bin/python3

import re

import pywikibot
from pywikibot import pagegenerators
import base_import_script as import_script


LEPINDEX_ID = 'P3064'


def main():
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, 'LepIndex ID not in Wikidata')
    repo = site.data_repository()
    data = list()

    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    found = 0
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print('Skipping %s, no data item found' % page.title())
            continue

        templates = page.raw_extracted_templates
        for t in templates:
            if t[0] in [ 'LepIndex' ]:
                for key, value in t[1].items():
                    if key.lower() == 'id':
                        print([key, value])

if __name__ == '__main__':
    main()
