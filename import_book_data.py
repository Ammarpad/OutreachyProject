#!/usr/local/bin/python3

import re
import sys
import pywikibot
import base_import_script as import_script

PAGE_NUM_ID = 'P1104'
BOOK_TEMPLATE = 'Infobox book'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, BOOK_TEMPLATE, ns=10)
    pages = page.getReferences(follow_redirects=False,
                        only_template_inclusion=True,
                        namespaces=[0],
                        total=limit)
    data = list()
    for page in pages:
        page_num = get_page_num(page)
        if page_num:
            data.append((page_num, page.data_item()))

    # Push to repo
    result = import_script.add_claims_to_item(repo, data, PAGE_NUM_ID, summary='')
    print("Finished. Imported %s pages, %s were skipped" %(result['added'], result['skipped']))

def get_page_num(page):
    for t in page.raw_extracted_templates:
        if t[0] == BOOK_TEMPLATE:
            page_num = t[1].get('pages')

            if page_num is None:
                return None
            elif page_num.isdigit():
                return page_num
            else:
                num = re.findall(r'\d+', page_num)
                if len(num) == 1:
                    return num[0]
                else:
                    # Multiple numbers, probably for different
                    # editions, it's hard to programmatically
                    # extract these from free-form string
                    return None

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)
