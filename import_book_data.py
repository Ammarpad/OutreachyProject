#!/usr/local/bin/python3

import re, os, io, sys
import common, pywikibot

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

def getPageNum(page):
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
def claimExists(page):
    """Checks the repo to find if
    the claim already exists"""
    try:
        item = page.data_item()
    except pywikibot.exceptions.NoPage:
        return False

    return PAGE_NUM_ID in item.get()['claims']

def getData(pages, limit):
    data = list()
    path = os.path.dirname(__file__) + '/__local__/P1104_titles.txt'
    count = 0

    with open(path, mode='a+') as file:
        file.seek(io.SEEK_SET)
        lines = file.readlines()
        titles = [t.strip() for t in lines]

        for page in pages:
            title = page.title()

            if title in titles:
                continue
            elif claimExists(page):
                file.write(title+'\n')
                continue
            else:
                page_num = getPageNum(page)
                file.write(title+'\n')
                if page_num:
                    data.append([page_num, page.data_item()])
                    count += 1

            if limit == count:
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
