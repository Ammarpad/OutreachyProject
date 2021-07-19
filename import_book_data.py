#!/usr/local/bin/python3

import pywikibot
import re, os, io, sys
import common

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

    data = getData(pages, limit)

    # Push to repo
    result = common.addMultipleClaims(data, PAGE_NUM_ID, summary='')
    print(f"Finished. Updated {result['added']} items, {result['skipped']} were skipped")

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
                    # Multiple values, probably for different
                    # editions, it's hard to programmatically
                    # extract these from free-form string
                    return None
def claim_exists(page):
    """Checks the repo to find if
    the claim already exists"""

    item = page.data_item()
    data = item.get()

    return PAGE_NUM_ID in data['claims']

def getData(pages, limit):
    data = list()
    path = os.path.dirname(__file__) + '/__local__/P1104_titles.txt'

    with open(path, mode='a+') as file:
        file.seek(io.SEEK_SET)
        titles = file.readlines()
        titles = [t.strip() for t in titles]

        for page in pages:
            title = page.title()

            if claim_exists(page):
                file.write(title)
                continue
            elif title in titles:
                continue
            else:
                page_num = get_page_num(page)
                if page_num:
                    data.append((page_num, page.data_item()))
                    count += 1
                    if limit > count:
                        break
    return data

def sparql_query():
    """SPARQL query alternative"""
    return "SELECT ?item " \
    "WHERE " \
    "{" \
      "VALUES ?type {wd:Q571 wd:Q7725634} " \
      "?item wdt:P31 ?type " \
      "MINUS { ?item wdt:P1104 [] }"\
    "}"

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)
