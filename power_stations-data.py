#!/usr/local/bin/python3

import re
import os
import io
import sys
import common
import pywikibot

PS_TEMPLATE = 'Infobox power station'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, PS_TEMPLATE, ns=10)

    pages = page.getReferences(follow_redirects=False,
                        only_template_inclusion=True,
                        namespaces=[0],
                        total=limit)

    result = processPages(pages)
    print('Finished. Updated %s items, %s were skipped.' %({result['added']}{result['skipped']}))

def processPages(pages):
	pass

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)